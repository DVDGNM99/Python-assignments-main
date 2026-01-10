from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Set, List, Dict

@dataclass
class Submission:
    id: int
    status: str
    raw_title: str
    submitted_at: datetime
    student_name_raw: Optional[str] = None
    student_name_norm: Optional[str] = None
    assignment_raw: Optional[str] = None
    assignment_norm: Optional[str] = None
    assignment_tags: Set[str] = field(default_factory=set)
    parse_warnings: List[str] = field(default_factory=list)

@dataclass
class Deadline:
    assignment_norm: str
    due_at: datetime
    raw_line: str

@dataclass
class LateSubmission:
    student: str
    assignment: str
    submitted_at: datetime
    due_at: datetime
    delta: timedelta

@dataclass
class ReportStats:
    missing_by_assignment: Dict[str, List[str]] = field(default_factory=dict)
    late_submissions: List[LateSubmission] = field(default_factory=list)
    deltas_by_assignment: Dict[str, List[timedelta]] = field(default_factory=dict)
    popularity: Dict[str, int] = field(default_factory=dict)
    anomalies: List[str] = field(default_factory=list)
