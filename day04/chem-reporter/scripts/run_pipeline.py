# scripts/run_pipeline.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# scripts/run_pipeline.py
# Windows-friendly CLI entry point for end-to-end runs.
# scripts/run_pipeline.py
# Windows-friendly CLI entry point for end-to-end runs.

import argparse
import json
import logging
from pathlib import Path
from datetime import datetime

from src.io_utils import build_outputs
from src.config import HTTP_TIMEOUT, USER_AGENT  

def _setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s | %(name)s | %(message)s")

def parse_args():
    p = argparse.ArgumentParser(
        description="Chem-Reporter pipeline (PubChem → RDKit → outputs)"
    )
    p.add_argument("--smiles", required=True, help="Input SMILES string.")
    p.add_argument("--name", required=True, help="Folder/name for results.")
    p.add_argument("--num-confs", type=int, default=10, help="RDKit conformers.")
    p.add_argument("--random-seed", type=int, default=0, help="Random seed.")
    p.add_argument("--verbose", action="store_true", help="Verbose logging.")
    return p.parse_args()

def main():
    args = parse_args()
    _setup_logging(args.verbose)

    logging.info("Starting pipeline…")
    logging.debug(f"HTTP_TIMEOUT={HTTP_TIMEOUT}, USER_AGENT={USER_AGENT}")

    # 🔧 Mappatura corretta dei parametri richiesti da io_utils.build_outputs
    out = build_outputs(
        smiles=args.smiles,
        results_dir=Path("results"),
        preferred_name=args.name,
        num_confs=args.num_confs,
        random_seed=args.random_seed,
    )

    print(json.dumps({
        "name": args.name,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "results_dir": str(Path("results") / args.name),
        "status": "ok",
    }, indent=2))

if __name__ == "__main__":
    main()
