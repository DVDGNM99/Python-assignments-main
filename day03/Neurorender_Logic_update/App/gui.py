"""
Lean Tkinter GUI that wires user actions to pure logic and rendering.
Move/port widgets from your old HW_GUI_input.py incrementally.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from App.logic import (
    load_regions_from_json, prepare_render_inputs, validate_acronyms, LogicError
)
from App.rendering import load_atlas, get_structures, build_scene, add_regions, render, AtlasLoadError

DEFAULT_ATLAS = "allen_mouse_25um"
DEFAULT_ALPHA = 0.5

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NeuroRender (day03)")
        self.geometry("720x480")
        self.resizable(True, True)

        # --- Controls (minimal for now) --- #
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        # Regions JSON
        ttk.Label(frm, text="Regions JSON:").grid(row=0, column=0, sticky="w")
        self.json_var = tk.StringVar(value=str(Path("regions.json").resolve()))
        ttk.Entry(frm, textvariable=self.json_var, width=60).grid(row=0, column=1, sticky="ew")
        ttk.Button(frm, text="Browse", command=self._browse_json).grid(row=0, column=2)

        # Atlas name
        ttk.Label(frm, text="Atlas:").grid(row=1, column=0, sticky="w")
        self.atlas_var = tk.StringVar(value=DEFAULT_ATLAS)
        ttk.Entry(frm, textvariable=self.atlas_var).grid(row=1, column=1, sticky="ew")

        # Alpha
        ttk.Label(frm, text="Alpha (0..1):").grid(row=2, column=0, sticky="w")
        self.alpha_var = tk.StringVar(value=str(DEFAULT_ALPHA))
        ttk.Entry(frm, textvariable=self.alpha_var).grid(row=2, column=1, sticky="w")

        # Load + Render
        ttk.Button(frm, text="Load & Prepare", command=self._on_prepare).grid(row=3, column=0, pady=8)
        ttk.Button(frm, text="Render", command=self._on_render).grid(row=3, column=1, pady=8)

        # Results
        self.status = tk.StringVar(value="Ready")
        ttk.Label(frm, textvariable=self.status).grid(row=4, column=0, columnspan=3, sticky="w", pady=(10,0))

        frm.columnconfigure(1, weight=1)

        # Internal state
        self._display_items = []   # strings "ACR — Name"
        self._valid_acronyms = []  # validated against atlas
        self._colors = []          # hex colors aligned with valid_acronyms

    def _browse_json(self):
        p = filedialog.askopenfilename(
            title="Select regions.json",
            filetypes=[("JSON", "*.json"), ("All files", "*.*")]
        )
        if p:
            self.json_var.set(p)

    def _on_prepare(self):
        try:
            # Load JSON
            items = load_regions_from_json(self.json_var.get())
            self._display_items = [it.display for it in items]

            # Load atlas just to validate acronyms once
            atlas = load_atlas(self.atlas_var.get().strip())
            structs = get_structures(atlas)

            # Normalize selections & colors (here we use ALL from JSON by default)
            acrs, cols, alpha = prepare_render_inputs(self._display_items, None, float(self.alpha_var.get()))

            valid, invalid = validate_acronyms(acrs, structs)
            self._valid_acronyms = valid
            # Keep colors aligned to valid ones
            self._colors = cols[: len(valid)]

            msg = f"Prepared {len(valid)} regions. Invalid: {len(invalid)}"
            if invalid:
                msg += f" (skipped: {', '.join(invalid[:8])}{'…' if len(invalid)>8 else ''})"
            self.status.set(msg)
            messagebox.showinfo("Preparation", msg)

        except (LogicError, AtlasLoadError, ValueError) as e:
            self.status.set(f"Error: {e}")
            messagebox.showerror("Error", str(e))

    def _on_render(self):
        if not self._valid_acronyms:
            messagebox.showwarning("Nothing to render", "Run 'Load & Prepare' first.")
            return
        try:
            scene = build_scene(self.atlas_var.get().strip())
            add_regions(scene, self._valid_acronyms, self._colors, float(self.alpha_var.get()))
            self.status.set("Rendering…")
            render(scene)
            self.status.set("Done.")
        except (AtlasLoadError, ValueError) as e:
            self.status.set(f"Render error: {e}")
            messagebox.showerror("Render error", str(e))

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
