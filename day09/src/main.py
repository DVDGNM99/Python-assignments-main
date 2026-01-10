import argparse
import logging
import sys
from pathlib import Path
import zoneinfo

from .parsers import parse_subjects_file, parse_deadlines
from .analyzer import analyze_submissions
from .report import generate_markdown_report, generate_csv_files
from .plotting import generate_plots

def main():
    parser = argparse.ArgumentParser(description="Submission Tracking System")
    parser.add_argument("--subjects", type=Path, default=Path("day09/subjects.txt"), help="Path to subjects.txt")
    parser.add_argument("--readme", type=Path, default=Path("day09/Deadlines.md"), help="Path to Deadlines.md")
    parser.add_argument("--deadlines-json", type=Path, help="Path to deadlines.json fallback")
    parser.add_argument("--out", type=Path, default=Path("report.md"), help="Output markdown report")
    parser.add_argument("--out-dir", type=Path, default=Path("out"), help="Output directory for CSVs")
    parser.add_argument("--tz", type=str, default="Asia/Jerusalem", help="Timezone for deadlines (e.g. Asia/Jerusalem)")
    parser.add_argument("--dedupe", type=str, choices=['latest', 'earliest', 'all'], default='latest', help="Deduplication strategy")
    parser.add_argument("--plots", action="store_true", help="Generate plots")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)
    
    # Validate paths
    if not args.subjects.exists():
        logger.error(f"Subjects file not found: {args.subjects}")
        sys.exit(1)
        
    if not args.readme.exists() and not args.deadlines_json:
        logger.warning(f"README not found: {args.readme}. Please provide --deadlines-json if README is missing.")
    
    # 1. Parse Submissions
    logger.info(f"Parsing submissions from {args.subjects}...")
    submissions = parse_subjects_file(args.subjects)
    logger.info(f"Found {len(submissions)} raw submissions.")
    
    # 2. Parse Deadlines
    logger.info(f"Parsing deadlines from {args.readme}...")
    deadlines = parse_deadlines(args.readme, args.deadlines_json)
    logger.info(f"Found {len(deadlines)} deadlines.")
    
    # 3. Analyze
    try:
        tz = zoneinfo.ZoneInfo(args.tz)
    except Exception as e:
        logger.error(f"Invalid timezone: {args.tz}")
        sys.exit(1)
        
    logger.info("Analyzing submissions...")
    stats = analyze_submissions(submissions, deadlines, tz, args.dedupe)
    
    # 4. Report
    logger.info(f"Generating report to {args.out}...")
    generate_markdown_report(stats, args.out)
    
    logger.info(f"Generating CSVs to {args.out_dir}...")
    generate_csv_files(stats, args.out_dir)
    
    if args.plots:
        logger.info(f"Generating plots to {args.out_dir}...")
        generate_plots(stats, args.out_dir)
    
    logger.info("Done.")

if __name__ == "__main__":
    main()
