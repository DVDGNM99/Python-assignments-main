# src/app_gui_tk.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import traceback

from src.pubchem import resolve
from src.io_utils import write_outputs


HELP_TEXT = (
    "Enter a SMILES string and click Search.\n"
    "Example: CC(=O)OC1=CC=CC=C1C(=O)O  (aspirin)\n"
)


class ChemReporterApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=12)
        self.master.title("Chem-Reporter (Tk)")
        self.master.geometry("640x220")
        self.master.minsize(520, 180)
        self.grid(sticky="nsew")

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Title
        title = ttk.Label(self, text="Chem-Reporter", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        # SMILES input
        ttk.Label(self, text="SMILES").grid(row=1, column=0, sticky="w")
        self.smiles_var = tk.StringVar()
        self.smiles_entry = ttk.Entry(self, textvariable=self.smiles_var)
        self.smiles_entry.grid(row=1, column=1, sticky="ew", padx=(8, 8))
        self.columnconfigure(1, weight=1)

        # Buttons
        self.search_btn = ttk.Button(self, text="Search", command=self.on_search)
        self.search_btn.grid(row=1, column=2, sticky="e")

        self.help_btn = ttk.Button(self, text="Help", command=self.on_help)
        self.help_btn.grid(row=2, column=2, sticky="e", pady=(8, 0))

        self.exit_btn = ttk.Button(self, text="Exit", command=self.master.destroy)
        self.exit_btn.grid(row=3, column=2, sticky="e", pady=(8, 0))

        # Status
        self.status_var = tk.StringVar(value="")
        self.status_lbl = ttk.Label(self, textvariable=self.status_var, foreground="green")
        self.status_lbl.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))

        # Bind Enter to Search
        self.smiles_entry.bind("<Return>", lambda _e: self.on_search())

    def on_help(self) -> None:
        messagebox.showinfo("Help", HELP_TEXT, parent=self)

    def on_search(self) -> None:
        smiles = self.smiles_var.get().strip()
        if not smiles:
            messagebox.showwarning("Missing input", "Please enter a SMILES string.", parent=self)
            return

        self.status_var.set("Fetching from PubChem…")
        self.update_idletasks()
        try:
            result = resolve(smiles)
            out_dir = write_outputs(result)
            self.status_var.set(f"Done. Saved to: {out_dir}")
            messagebox.showinfo("Success", f"Output folder:\n{out_dir}", parent=self)
        except Exception as e:
            self.status_lbl.configure(foreground="red")
            self.status_var.set("Failed.")
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            messagebox.showerror("Error", f"An error occurred:\n\n{tb}", parent=self)


def main() -> None:
    root = tk.Tk()
    # Native theming
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    app = ChemReporterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
