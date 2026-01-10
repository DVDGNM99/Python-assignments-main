from datetime import datetime, timedelta, timezone
import logging
from typing import List, Dict, Set, Optional, Literal
import zoneinfo

from .models import Submission, Deadline, ReportStats, LateSubmission

logger = logging.getLogger(__name__)

def get_latest_submissions(submissions: List[Submission], dedupe_mode: Literal['latest', 'earliest', 'all']) -> List[Submission]:
    if dedupe_mode == 'all':
        return submissions
    
    # Group by student + assignment
    grouped = {}
    for sub in submissions:
        if not sub.student_name_norm or not sub.assignment_norm:
            continue
        
        # Use primary assignment for grouping
        key = (sub.student_name_norm, sub.assignment_norm)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(sub)
    
    result = []
    for subs in grouped.values():
        # Sort by date
        subs.sort(key=lambda s: s.submitted_at)
        
        if dedupe_mode == 'latest':
            result.append(subs[-1])
        elif dedupe_mode == 'earliest':
            result.append(subs[0])
            
    # Also add submissions that failed grouping (anomalies) if we want to keep them?
    # No, analysis usually focuses on valid ones.
    return result

def analyze_submissions(
    submissions: List[Submission], 
    deadlines: Dict[str, Deadline],
    tz: zoneinfo.ZoneInfo,
    dedupe_mode: Literal['latest', 'earliest', 'all'] = 'latest'
) -> ReportStats:
    
    stats = ReportStats()
    
    # Identify anomalies
    for sub in submissions:
        if not sub.student_name_norm:
           stats.anomalies.append(f"Submission {sub.id}: No student name parsed from '{sub.raw_title}'")
        if not sub.assignment_norm:
           stats.anomalies.append(f"Submission {sub.id}: No assignment parsed from '{sub.raw_title}'")
        if not sub.student_name_norm or not sub.assignment_norm:
            continue
            
    # Dedupe
    valid_subs = [s for s in submissions if s.student_name_norm and s.assignment_norm]
    clean_subs = get_latest_submissions(valid_subs, dedupe_mode)
    
    # 1. Missing Submissions
    # Build list of all students seen
    all_students = set(s.student_name_norm for s in valid_subs)
    
    # Check each known assignment in deadlines against students
    # Group submissions by assignment
    subs_by_assign_student = {} # {assignment: {student}}
    for sub in clean_subs:
        if sub.assignment_norm not in subs_by_assign_student:
             subs_by_assign_student[sub.assignment_norm] = set()
        subs_by_assign_student[sub.assignment_norm].add(sub.student_name_norm)
        
    for assign_norm, deadline in deadlines.items():
        if assign_norm not in stats.missing_by_assignment:
            stats.missing_by_assignment[assign_norm] = []
            
        submitted_students = subs_by_assign_student.get(assign_norm, set())
        for student in sorted(all_students):
            if student not in submitted_students:
                stats.missing_by_assignment[assign_norm].append(student)
                
    # 2. Late Submissions & Delta Stats
    for sub in clean_subs:
        if sub.assignment_norm in deadlines:
            deadline = deadlines[sub.assignment_norm]
            
            # Deadline is naive from README (as parsed), we need to localize it to the requested TZ
            # then convert to UTC to compare with submission which is UTC
            
            if deadline.due_at.tzinfo is None:
                # Localize to provided tz
                due_local = deadline.due_at.replace(tzinfo=tz)
                # To compare with submitted_at (UTC), convert due to UTC
                due_utc = due_local.astimezone(timezone.utc)
            else:
                due_utc = deadline.due_at.astimezone(timezone.utc)
            
            delta = sub.submitted_at - due_utc
            
            # Store delta
            if sub.assignment_norm not in stats.deltas_by_assignment:
                stats.deltas_by_assignment[sub.assignment_norm] = []
            stats.deltas_by_assignment[sub.assignment_norm].append(delta)
            
            # Check Late
            if delta > timedelta(0):
                stats.late_submissions.append(LateSubmission(
                    student=sub.student_name_norm,
                    assignment=sub.assignment_norm,
                    submitted_at=sub.submitted_at,
                    due_at=due_utc,
                    delta=delta
                ))
        else:
            # Assignment without deadline?
            # Maybe add to anomalies if strict?
            # Roadmap says: "Assignment in file but not in deadlines -> anomalies"
            stats.anomalies.append(f"Assignment '{sub.assignment_norm}' found but no deadline defined.")
            
    # 3. Popularity
    # Using clean_subs (deduped or not based on user pref)
    for sub in clean_subs:
        stats.popularity[sub.assignment_norm] = stats.popularity.get(sub.assignment_norm, 0) + 1
        
    # Sort late_submissions desc by delta
    stats.late_submissions.sort(key=lambda x: x.delta, reverse=True)
    
    return stats
