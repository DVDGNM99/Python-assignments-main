# src/app_gui.py
from __future__ import annotations

import traceback
import PySimpleGUI as sg
from datetime import datetime

from .rdkit_utils import validate_smiles, smiles_to_sdf
from .pubchem import resolve
from .io_utils import write_outputs
from .config import HTTP_TIMEOUT, USER_AGENT

LOGO = "Chem-Reporter"
HELP_TEXT = (
    "Enter a SMILES string and click Search.\n"
    "Example: CC(=O)OC1=CC=CC=C1C(=O)O (aspirin)\n"
)

def main() -> None:
    sg.theme("SystemDefault")

    layout = [
        [sg.Text(LOGO, font=("Segoe UI", 16, "bold"))],
        [sg.Multiline(HELP_TEXT, size=(60, 3), disabled=True, no_scrollbar=True)],
        [sg.Text("SMILES"), sg.Input(key="-SMILES-", size=(60, 1))],
        [sg.Button("Search", key="-SEARCH-", bind_return_key=True),
         sg.Button("Clear"), sg.Button("Exit")],
        [sg.HorizontalSeparator()],
        [sg.Multiline(key="-LOG-", size=(80, 20), autoscroll=True, disabled=True)]
    ]

    window = sg.Window("Chem-Reporter — PubChem (MVP)", layout)

    def log(message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        window["-LOG-"].update(f"[{ts}] {message}\n", append=True)

    log(f"HTTP_TIMEOUT={HTTP_TIMEOUT}s | USER_AGENT={USER_AGENT}")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Clear":
            window["-SMILES-"].update("")
            window["-LOG-"].update("")
            continue

        if event == "-SEARCH-":
            smiles = (values.get("-SMILES-") or "").strip()
            if not smiles:
                log("Please enter a SMILES string.")
                continue

            log(f"Validating SMILES: {smiles}")
            if not validate_smiles(smiles):
                log("Invalid SMILES. Please check the input.")
                continue

            try:
                log("Querying PubChem…")
                result = resolve(smiles)
                log(f"Resolved CID={result.cid} | IUPAC={result.iupac_name or 'N/A'}")

                out_dir = write_outputs(result, base_dir="results")
                log(f"Wrote outputs to: {out_dir}")

                log("Done ✅")
                sg.popup_ok("Success! Outputs written to:\n" + str(out_dir),
                            title="Chem-Reporter", keep_on_top=True)
            except Exception as e:
                log("An error occurred. See details below.")
                log("".join(traceback.format_exception(e)))
                sg.popup_error("Error during processing:\n" + str(e),
                               title="Chem-Reporter", keep_on_top=True)

    window.close()

if __name__ == "__main__":
    main()
