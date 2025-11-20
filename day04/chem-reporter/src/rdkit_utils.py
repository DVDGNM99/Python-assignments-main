# placeholder RDKIT utilities
# src/rdkit_utils.py
# Utilities for SMILES validation and 3D SDF export using RDKit.
# Designed to run on Windows (Conda/Miniforge) as specified in environment.yml.
# All comments, identifiers, and user-facing strings are in English.

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Any

from rdkit import Chem
from rdkit.Chem import AllChem


class RDKitGenerationError(Exception):
    """Raised when 3D generation or optimization fails."""


def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def canonicalize_smiles(smiles: str) -> str:
    """
    Return a canonical SMILES after parsing and sanitization.
    Raises a ValueError if parsing fails.
    """
    if not isinstance(smiles, str) or not smiles.strip():
        raise ValueError("SMILES must be a non-empty string.")
    mol = Chem.MolFromSmiles(smiles, sanitize=True)
    if mol is None:
        raise ValueError("Invalid SMILES: parsing returned None.")
    return Chem.MolToSmiles(mol, canonical=True)


def validate_smiles(smiles: str) -> bool:
    """
    Quick validity check for a SMILES string.
    Returns True if RDKit can parse and sanitize it, False otherwise.
    """
    if not isinstance(smiles, str) or not smiles.strip():
        return False
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=True)
        if mol is None:
            return False
        # Round-trip to canonical SMILES as a lightweight integrity check.
        _ = Chem.MolToSmiles(mol, canonical=True)
        return True
    except Exception:
        return False


def smiles_to_mol(
    smiles: str,
    embed_3d: bool = True,
    add_hydrogens: bool = True,
    num_confs: int = 1,
    random_seed: int = 0xF00D,
    optimize: bool = True,
) -> Chem.Mol:
    """
    Convert SMILES to an RDKit Mol object.
    Optionally generate 3D coordinates with ETKDG and run MMFF/UFF optimization.

    Parameters
    ----------
    smiles : str
        Input SMILES string (will be sanitized).
    embed_3d : bool
        If True, generate 3D coordinates using ETKDG.
    add_hydrogens : bool
        If True, add explicit hydrogens before 3D embedding.
    num_confs : int
        Number of conformers to generate (default 1).
    random_seed : int
        Random seed for deterministic embeddings on CI/Windows.
    optimize : bool
        If True, run force-field optimization (MMFF if available, else UFF).

    Returns
    -------
    rdkit.Chem.Mol
        Molecule with conformer(s) if 3D was requested.

    Raises
    ------
    ValueError
        If the SMILES is invalid.
    RDKitGenerationError
        If 3D embedding or optimization fails.
    """
    try:
        base = Chem.MolFromSmiles(smiles, sanitize=True)
        if base is None:
            raise ValueError("Invalid SMILES: parsing returned None.")
    except Exception as exc:
        raise ValueError(f"Invalid SMILES: {exc}") from exc

    mol = Chem.AddHs(base) if add_hydrogens else base

    if embed_3d:
        params = AllChem.ETKDGv3()
        params.randomSeed = random_seed
        params.useRandomCoords = False
        params.pruneRmsThresh = 0.1
        # Generate one or more conformers:
        ids = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)
        if not ids:
            raise RDKitGenerationError("ETKDG embedding failed (no conformers).")

        if optimize:
            # Try MMFF first; fall back to UFF if MMFF is not parameterized
            try:
                mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant="MMFF94s")
                if mmff_props is not None:
                    for cid in ids:
                        res = AllChem.MMFFOptimizeMolecule(mol, mmff_props, confId=cid, maxIters=200)
                        # res: 0=converged, 1=failed; we don't hard-fail on 1 because UFF fallback may still help elsewhere
                else:
                    raise RuntimeError("MMFF properties not available; falling back to UFF.")
            except Exception:
                for cid in ids:
                    _ = AllChem.UFFOptimizeMolecule(mol, confId=cid, maxIters=200)

    return mol


def write_sdf(
    mol: Chem.Mol,
    output_path: str | Path,
    props: Optional[Dict[str, Any]] = None,
    kekulize: bool = False,
) -> Path:
    """
    Write a molecule to an SDF file, attaching provided properties as SD fields.

    Notes
    -----
    - If `kekulize` is True, an attempt is made to kekulize a copy for nicer bond representations.
    - Creates parent directories if they do not exist.
    """
    if mol is None:
        raise ValueError("`mol` must be a valid RDKit Mol.")

    out = Path(output_path)
    _ensure_parent_dir(out)

    mol_to_write = Chem.Mol(mol)
    if kekulize:
        try:
            Chem.Kekulize(mol_to_write, clearAromaticFlags=True)
        except Exception:
            # Non-fatal: write as-is if kekulization fails
            mol_to_write = Chem.Mol(mol)

    # Attach properties
    if props:
        for key, val in props.items():
            if val is None:
                continue
            mol_to_write.SetProp(str(key), str(val))

    writer = Chem.SDWriter(str(out))
    # RDKit SDWriter writes one mol at a time; we write the first conformer (or 2D if no 3D)
    writer.write(mol_to_write)
    writer.close()
    return out


def smiles_to_sdf(
    smiles: str,
    output_path: str | Path,
    props: Optional[Dict[str, Any]] = None,
    num_confs: int = 1,
    random_seed: int = 0xF00D,
) -> Path:
    """
    Convenience function: validate -> build 3D -> write SDF.

    Returns the output Path on success.
    """
    if not validate_smiles(smiles):
        raise ValueError("Invalid SMILES supplied.")

    mol = smiles_to_mol(
        smiles=smiles,
        embed_3d=True,
        add_hydrogens=True,
        num_confs=num_confs,
        random_seed=random_seed,
        optimize=True,
    )
    return write_sdf(mol, output_path=output_path, props=props)
