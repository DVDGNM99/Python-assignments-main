import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
import logging

from .models import Submission, Deadline

logger = logging.getLogger(__name__)

def normalize_student_name(name: str) -> str:
    if not name:
        return ""
    # Remove extra spaces and title case
    clean = " ".join(name.split()).title()
    # Ensure hyphens have valid spacing or casing if needed, but for now simple title case
    # "Rachel Steinitz-Eliyahu" -> "Rachel Steinitz-Eliyahu" (Title checks this)
    return clean

def canonicalize_assignment(title: str) -> Tuple[Optional[str], Set[str]]:
    """
    Returns (primary_assignment_norm, set_of_tags)
    """
    if not title:
        return None, set()
    
    lower_title = title.lower()
    tags = set()
    primary = None

    # Detect Day XX
    days = re.findall(r"day\s*0?(\d+)", lower_title)
    for day in days:
        tag = f"day{int(day):02d}"
        tags.add(tag)
        if primary is None: # Use first as primary if not set
            primary = tag
    
    if len(days) > 1:
        # If multiple days, primary could be combo or just first. 
        # Roadmap says: "Combinations: Day 05 and 06 => tags {day05, day06}"
        # logic: primary could be "day05+day06" or just use tags.
        # simpler to just let primary be the first one found for "assignment" field, 
        # but analysis might want to use tags.
        # Let's construct primary from sorted tags to be unique
        primary = "+".join(sorted(tags))
    
    # Detect Project
    if "final project" in lower_title or "proposal" in lower_title:
        tag = "final_project_proposal"
        tags.add(tag)
        # If it's the only thing or explicit, make it primary
        if not days: 
            primary = tag
        elif "final project" in lower_title: # precedence?
             # If "Day 08 and proposal...", usually implies both.
             pass

    if not primary and tags:
        primary = list(tags)[0]

    return primary, tags

def parse_student_and_assignment(title: str) -> Tuple[Optional[str], Optional[str], Optional[str], Set[str]]:
    """
    Parses raw title to extract student name and assignment details.
    Returns: (student_name_norm, assignment_raw, assignment_norm, assignment_tags)
    """
    title = title.strip()
    student_raw = None
    assignment_part = title
    
    # 1. Try explicit separators: " by ", " - "
    # We prioritize " by " because " - " could be in a name (though rare for student names here, more like hyphenated)
    # But "day 03-Name" is common.
    
    # Check for " by " (case insensitive)
    match = re.search(r"\s+by\s+(.+)$", title, re.IGNORECASE)
    if match:
        student_raw = match.group(1)
        assignment_part = title[:match.start()]
    else:
        # Check for " - " or "-" preceded by assignment-like pattern? 
        # "day 03-Rachel" -> dash no space
        # "day 08 ... -Rachel"
        # Let's try splitting by last dash if it looks like a separator
        # But names can have dashes. "Rachel Steinitz-Eliyahu"
        # We should iterate separators.
        
        # Regex for "Day XX" or "Final Project..." at START
        # followed by optional separator, then Name.
        
        # Patterns to separate assignment from name
        # A) Start with assignment (Day XX or Final Project Proposal)
        # B) Separator (space, dash, 'by')
        # C) Name (rest)
        
        # We construct a regex that captures assignment part commonly seen
        # ORDER MATTERS: Put longer/specific matches first!
        assign_pattern = r"^(day\s*\d+\s+and\s+proposal\s+for\s+final\s+project|day\s*\d+(\s+and\s+day\s*\d+)?|final\s*project\s*proposal(\s+by)?)"
        
        match_start = re.match(assign_pattern, title, re.IGNORECASE)
        if match_start:
            # We found something that looks like assignment at start.
            # Now extract the rest as name, stripping separators.
            raw_assign = match_start.group(0)
            potential_name = title[match_start.end():]
            
            # Clean up potential name (remove leading " -", " ", "by ")
            # Use regex to remove specific separators at start of name
            clean_name_match = re.match(r"^[\s\-]+(?:by\s+)?(.+)$", potential_name, re.IGNORECASE)
            if clean_name_match:
                student_raw = clean_name_match.group(1)
                assignment_part = raw_assign
            else:
                # Maybe it was just "Day 06" with no name?
                if potential_name.strip() == "":
                   student_raw = None # No name
                   assignment_part = raw_assign
                else:
                    # Fallback: maybe just space?
                    student_raw = potential_name.strip()
                    assignment_part = raw_assign
        else:
            # Fallback for "DayXXName" no space? Unlikely.
            pass

    norm_name = normalize_student_name(student_raw) if student_raw else None
    
    primary_norm, tags = canonicalize_assignment(assignment_part)
    
    return norm_name, assignment_part, primary_norm, tags

def parse_subjects_file(file_path: Path) -> List[Submission]:
    submissions = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            # Expect: id, status, title, (empty), timestamp
            # Sometimes empty field is missing?
            
            if len(parts) < 3:
                # Malformed
                logger.warning(f"Line {line_num} has too few fields: {parts}")
                continue
                
            try:
                sub_id = int(parts[0])
                status = parts[1]
                title = parts[2]
                
                # Timestamp usually last
                timestamp_str = parts[-1]
                # Validate timestamp looks like a timestamp
                if 'T' not in timestamp_str or 'Z' not in timestamp_str:
                     # Maybe the 4th field was empty and split ate it?
                     # Let's try parts[4] if exists
                     if len(parts) >= 5:
                         timestamp_str = parts[4]
                
                try:
                    # ISO format: 2026-01-04T09:10:31Z
                    # python 3.11 fromisoformat handles 'Z' usually, but safe to replace Z with +00:00
                    ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except ValueError:
                    logger.warning(f"Line {line_num}: Invalid timestamp {timestamp_str}")
                    # Skip or keep with None? Plan says 'submitted_at' is datetime.
                    # If we can't parse time, we can't do stats. Skip.
                    continue
                
                norm_name, assign_raw, assign_norm, tags = parse_student_and_assignment(title)
                
                warnings = []
                if not norm_name:
                    warnings.append("Could not extract student name")
                if not assign_norm:
                    warnings.append("Could not extract assignment")

                sub = Submission(
                    id=sub_id,
                    status=status,
                    raw_title=title,
                    submitted_at=ts,
                    student_name_raw=parts[2], # Wait, raw student? The title is mixed.
                    student_name_norm=norm_name,
                    assignment_raw=assign_raw,
                    assignment_norm=assign_norm,
                    assignment_tags=tags,
                    parse_warnings=warnings
                )
                submissions.append(sub)

            except Exception as e:
                logger.error(f"Line {line_num}: Error parsing - {e}")
                continue
                
    return submissions

def parse_deadlines(readme_path: Path, json_path: Optional[Path] = None) -> Dict[str, Deadline]:
    deadlines = {}
    
    # 1. Try README / Deadlines file
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex for "Day X: YYYY.MM.DD HH:MM"
        # Example: "Day 1: 2025.11.01 22:00"
        # New format: "day 9:  2026.01.10 22:00"
        # New format: "Project proposal dead-line: 2026.01.11 22:00"
        
        # We can look for lines that contain a date pattern and extract the key from before matches.
        # Pattern: (Key) ... (YYYY.MM.DD HH:MM)
        
        # Let's iterate line by line to be safer, or use broader regex.
        # "Day \d+"
        # "Project .* dead-line"
        
        # Regex:
        # Group 1: Assignment Name (Variable)
        # Group 2: Date (YYYY.MM.DD HH:MM)
        
        # Supported keys logic:
        # "Day \d+" -> Day XX
        # "day \d+" -> Day XX
        # "Project proposal dead-line" -> final_project_proposal
        # "Project submission dead-line" -> final_project?
        
        # Let's use a list of regex patterns
        patterns = [
            (r"(day\s*\d+):\s*(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})", None), # Explicit "day X:"
            (r"(Project\s+proposal\s+dead-line):\s*(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})", "final_project_proposal"),
            (r"(Project\s+submission\s+dead-line):\s*(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})", "final_project_submission") # assuming logical name
        ]
        
        # Case insensitive find
        for pat, forced_norm in patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            for name_str, time_str in matches:
                if forced_norm:
                    primary = forced_norm
                else:
                    primary, _ = canonicalize_assignment(name_str)
                
                if primary:
                    try:
                        dt = datetime.strptime(time_str, "%Y.%m.%d %H:%M")
                        # Naive
                        deadlines[primary] = Deadline(
                            assignment_norm=primary,
                            due_at=dt,
                            raw_line=f"{name_str}: {time_str}"
                        )
                    except ValueError as e:
                        logger.warning(f"Failed to parse date {time_str}: {e}")

    # 2. JSON Fallback
    if json_path and json_path.exists():
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    # k=assignment, v=iso date string
                    norm, _ = canonicalize_assignment(k)
                    if norm and norm not in deadlines:
                         dt = datetime.fromisoformat(v)
                         deadlines[norm] = Deadline(norm, dt, "JSON")
        except Exception as e:
            logger.error(f"Failed to load JSON deadlines: {e}")

    return deadlines
