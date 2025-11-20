# scripts/run_batch.py
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from datetime import datetime

# Allow "python scripts/run_batch.py" to import src/*
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rdkit_utils import validate_smiles
from src.pubchem import resolve
from src.io_utils import write_outputs
from src.models import Result

def process_csv(input_csv: Path, results_dir: Path) -> Path:
    results_dir.mkdir(parents=True, exist_ok=True)
    summary_path = results_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    smiles_column_candidates = ("smiles", "SMILES")
    rows = list(csv.DictReader(input_csv.open("r", newline="", encoding="utf-8")))
    if not rows:
        raise ValueError("Input CSV is empty.")

    # Detect column
    header = rows[0].keys()
    col = None
    for c in smiles_column_candidates:
        if c in header:
            col = c
            break
    if col is None:
        raise ValueError(f"CSV must contain one of these columns: {smiles_column_candidates}")

    with summary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["input_smiles", "valid", "cid", "iupac_name", "output_dir", "error"]
        )
        writer.writeheader()

        for i, row in enumerate(rows, start=1):
            raw = (row.get(col) or "").strip()
            record = {
                "input_smiles": raw,
                "valid": False,
                "cid": "",
                "iupac_name": "",
                "output_dir": "",
                "error": ""
            }
            if not raw:
                record["error"] = "Empty SMILES cell"
                writer.writerow(record)
                continue

            try:
                record["valid"] = bool(validate_smiles(raw))
                if not record["valid"]:
                    record["error"] = "Invalid SMILES"
                    writer.writerow(record)
                    continue

                res: Result = resolve(raw)
                record["cid"] = str(res.cid or "")
                record["iupac_name"] = res.iupac_name or ""

                out_dir = write_outputs(res, base_dir=str(results_dir))
                record["output_dir"] = str(out_dir)

                writer.writerow(record)
                print(f"[{i}] OK: {raw} → CID={record['cid']}")
            except Exception as e:
                record["error"] = str(e)
                writer.writerow(record)
                print(f"[{i}] ERROR: {raw} → {e}")

    return summary_path

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch process a CSV of SMILES and write Chem-Reporter outputs."
    )
    parser.add_argument("csv", type=Path, help="Path to input CSV containing a 'smiles' column.")
    parser.add_argument("--results", type=Path, default=Path("results"),
                        help="Base output directory (default: ./results)")
    args = parser.parse_args()

    summary = process_csv(args.csv, args.results)
    print(f"\nSummary written to: {summary}")

if __name__ == "__main__":
    main()
