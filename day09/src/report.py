import csv
from pathlib import Path
from typing import List, Dict
from datetime import timedelta
import statistics

from .models import ReportStats, LateSubmission

def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{days}d {hours}h {minutes}m"

def generate_markdown_report(stats: ReportStats, out_path: Path):
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("# Submission Analysis Report\n\n")
        
        # Overview
        f.write("## Overview\n")
        total_late = len(stats.late_submissions)
        f.write(f"- Total Late Submissions: {total_late}\n")
        f.write(f"- Total Anomalies: {len(stats.anomalies)}\n\n")
        
        # Missing
        f.write("## Missing Assignments\n")
        if not stats.missing_by_assignment:
            f.write("No missing assignments found (or all students submitted everything!).\n")
        else:
            f.write("| Assignment | Missing Students |\n")
            f.write("|---|---|\n")
            for assign, students in sorted(stats.missing_by_assignment.items()):
                if students:
                    f.write(f"| {assign} | {', '.join(sorted(students))} |\n")
        f.write("\n")
        
        # Late Submissions
        f.write("## Late Submissions\n")
        if not stats.late_submissions:
            f.write("No late submissions.\n")
        else:
            f.write("| Student | Assignment | Due | Submitted | Delay |\n")
            f.write("|---|---|---|---|---|\n")
            for late in stats.late_submissions:
                delay = format_timedelta(late.delta)
                # Show dates in ISO simplified
                due_str = late.due_at.strftime("%Y-%m-%d %H:%M")
                sub_str = late.submitted_at.strftime("%Y-%m-%d %H:%M")
                f.write(f"| {late.student} | {late.assignment} | {due_str} | {sub_str} | {delay} |\n")
        f.write("\n")
        
        # Stats per assignment
        f.write("## Statistics by Assignment\n")
        f.write("| Assignment | Mean Delay | Median Delay | Max Delay |\n")
        f.write("|---|---|---|---|\n")
        for assign, deltas in sorted(stats.deltas_by_assignment.items()):
            if not deltas:
                continue
            secs = [d.total_seconds() for d in deltas]
            mean_d = timedelta(seconds=statistics.mean(secs))
            median_d = timedelta(seconds=statistics.median(secs))
            max_d = timedelta(seconds=max(secs))
            f.write(f"| {assign} | {format_timedelta(mean_d)} | {format_timedelta(median_d)} | {format_timedelta(max_d)} |\n")
        f.write("\n")
        
        # Popularity
        f.write("## Popularity (Submission Count)\n")
        f.write("| Assignment | Count |\n")
        f.write("|---|---|\n")
        sorted_pop = sorted(stats.popularity.items(), key=lambda x: x[1], reverse=True)
        for assign, count in sorted_pop:
            f.write(f"| {assign} | {count} |\n")
        f.write("\n")
        
        # Anomalies
        if stats.anomalies:
            f.write("## Anomalies\n")
            for anomaly in stats.anomalies:
                f.write(f"- {anomaly}\n")

def generate_csv_files(stats: ReportStats, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Missing
    with open(out_dir / "missing.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Assignment", "Student"])
        for assign, students in stats.missing_by_assignment.items():
            for student in students:
                writer.writerow([assign, student])
                
    # Late
    with open(out_dir / "late.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Student", "Assignment", "Due At", "Submitted At", "Delay Seconds"])
        for late in stats.late_submissions:
            writer.writerow([
                late.student, 
                late.assignment, 
                late.due_at.isoformat(), 
                late.submitted_at.isoformat(), 
                late.delta.total_seconds()
            ])
            
    # Popularity
    with open(out_dir / "popularity.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Assignment", "Count"])
        for assign, count in stats.popularity.items():
            writer.writerow([assign, count])
