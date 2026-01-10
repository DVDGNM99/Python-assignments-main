import pytest
from datetime import datetime, timezone
from pathlib import Path
from day09.src.parsers import parse_student_and_assignment, canonicalize_assignment, normalize_student_name, parse_subjects_file
from day09.src.models import Submission

def test_normalize_student_name():
    assert normalize_student_name("  adi   moses  ") == "Adi Moses"
    assert normalize_student_name("rachel steinitz-eliyahu") == "Rachel Steinitz-Eliyahu"
    assert normalize_student_name(None) == ""

def test_canonicalize_assignment():
    # Simple Day
    assert canonicalize_assignment("Day 01") == ("day01", {"day01"})
    assert canonicalize_assignment("day08") == ("day08", {"day08"})
    
    # Project
    assert canonicalize_assignment("Final Project proposal") == ("final_project_proposal", {"final_project_proposal"})
    
    # Complex
    primary, tags = canonicalize_assignment("Day 05 and 06")
    assert primary in ["day05", "day06", "day05+day06"] # Logic builds +join sorted
    assert tags == {"day05", "day06"}
    
    # Weird
    primary, tags = canonicalize_assignment("day 08 and proposal for final project")
    assert "day08" in tags
    assert "final_project_proposal" in tags

def test_parse_student_and_assignment_formats():
    # 1. Standard "by"
    norm, raw_a, norm_a, tags = parse_student_and_assignment("Day08 by Shoshana Sernik")
    assert norm == "Shoshana Sernik"
    assert norm_a == "day08"
    
    # 2. " - "
    norm, raw_a, norm_a, tags = parse_student_and_assignment("day 03-Rachel Steinitz Eliyahu")
    assert norm == "Rachel Steinitz Eliyahu"
    assert norm_a == "day03"

    # 3. No separator (space?)
    # "day06 Lior Batat"
    norm, raw_a, norm_a, tags = parse_student_and_assignment("day06 Lior Batat")
    assert norm == "Lior Batat"
    assert norm_a == "day06"
    
    # 4. Complex: The bug reported
    # "day 08 and proposal for final project-Rachel Steinitz Eliyahu"
    norm, raw_a, norm_a, tags = parse_student_and_assignment("day 08 and proposal for final project-Rachel Steinitz Eliyahu")
    assert norm == "Rachel Steinitz Eliyahu"
    assert "day08" in tags
    assert "final_project_proposal" in tags

def test_parse_broken_lines(tmp_path):
    # Create dummy subject.txt
    f = tmp_path / "subjects.txt"
    content = """
1\tOPEN\tDay01 by Bob\t\t2025-01-01T12:00:00Z
2\tOPEN\tBadLine
3\tOPEN\tDay02 by Alice\t\tInvalidDate
4\tOPEN\tDay03 by Charlie\t\t2025-01-01T12:00:00Z
    """.strip()
    f.write_text(content, encoding='utf-8')
    
    subs = parse_subjects_file(f)
    assert len(subs) == 2 # Only valid ones: 1 and 4. Line 2 has few fields, Line 3 invalid date.
    
    assert subs[0].student_name_norm == "Bob"
    assert subs[0].id == 1
    assert subs[1].student_name_norm == "Charlie"
    assert subs[1].id == 4
