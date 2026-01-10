# Submission Tracking Tool

This tool analyzes student submissions from `subjects.txt` and compares them against deadlines defined in `README.md`.

## Installation

1. Ensure Python 3.11+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: `matplotlib` is listed but plotting is optional and currently not enabled by default CLI).

## Step-by-Step Guide

1. **Prepare Data**:
   - Ensure `subjects.txt` is in the `day09` folder (or specify path).
   - Ensure `Deadlines.md` (or README) contains the deadlines in format "Day X: YYYY.MM.DD HH:MM" or "Project ...: YYYY...".

2. **Run the Script**:
   Open a terminal in the project root and run:
   ```bash
   python -m day09.src.main --subjects day09/subjects.txt --readme day09/Deadlines.md --out day09/report.md --out-dir day09/out --plots
   ```
   
   - The script will parse the files.
   - It will identify student names and assignments.
   - It will check for missing or late submissions.
   - It will generate a report, CSV files, and plots.

3. **Check Results**:
   - Open `day09/report.md` to see the summary.
   - Check `day09/out/` for CSVs and PNG plots (e.g., `deltas_boxplot.png`).

## File Descriptions

- **`src/models.py`**: Defines the data structures (DataClasses) used throughout the app, such as `Submission` (student data), `Deadline` (due dates), and `ReportStats` (analysis results).
- **`src/parsers.py`**: Contains logic to read the `subjects.txt` TSV file (handling broken lines) and the `Deadlines.md` file (extracting dates with regex). Includes regex for normalizing student names.
- **`src/analyzer.py`**: The core logic engine. It takes parsed submissions and deadlines, deduplicates them (if requested), calculates who is missing assignments, and computes time deltas (how late/early) for submissions.
- **`src/report.py`**: formatting logic to generate the readable Markdown report and the CSV export files.
- **`src/plotting.py`**: Uses `matplotlib` to generate visualizations, such as the Boxplot of submission deltas.
- **`src/main.py`**: The entry point. Handles command line arguments (`--out`, `--plots`, etc.), orchestrates the flow (Parse -> Analyze -> Report -> Plot), and sets up logging.
- **`tests/`**: Contains unit tests to verify the logic (parsing, etc.) works correctly.

## Outputs

The tool generates both a summary report and raw data files.

### 1. Markdown Report (`report.md`)
A human-readable summary containing:
  - **Overview**: Total late submissions and anomalies.
  - **Missing Assignments**: List of students who haven't submitted specific assignments.
  - **Late Submissions**: Tables showing who submitted late and by how much.
  - **Statistics**: Mean, median, and max delays per assignment.
  - **Popularity**: Count of submissions per assignment type.
  - **Anomalies**: Warnings about parsing issues or missing deadlines.

### 2. Output Directory (`out/`)
This folder contains raw data CSVs and visualization plots.

- **CSV Files** (for spreadsheet analysis):
  - `missing.csv`: Columns [Assignment, Student]. Lists every missing submission.
  - `late.csv`: Columns [Student, Assignment, Due, Submitted, Delay]. Full list of late items.
  - `popularity.csv`: Columns [Assignment, Count]. Submission counts.

- **Plots** (generated with `--plots`):
  - `deltas_boxplot.png`: A boxplot visualizing the distribution of submission times relative to the deadline (0 line). Positive values are late. Points beyond whiskers are outliers.
  - `deltas_violin.png`: A violin plot showing the probability density of the data at different values, useful for seeing the shape of the distribution.

## Troubleshooting

- **Anomalies**: If you see "Assignment found but no deadline defined", it means a submission title contained an assignment (like "Final Project Proposal") that wasn't found in the README deadlines list. This is normal if the README doesn't specify it.
