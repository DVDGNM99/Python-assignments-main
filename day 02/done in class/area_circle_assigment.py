#!/usr/bin/env python3
"""Calculate the area of a circle.

Usage:
 - Interactive (GUI): run the script without arguments to open the window.
 - From command line: python area_circle_assignment.py <radius>

The program accepts numbers using either comma or dot as decimal separator
and validates that the value is positive.
"""
import os
import sys
import math
import tkinter as tk
from tkinter import messagebox

# Ensure the repository root (parent of this file) is on sys.path so
# `common_utils.py` located in the repository root can be imported when
# running the script directly from the `day 02` folder.
SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from common_utils import parse_positive_number


def circle_area(radius: float) -> float:
    return math.pi * radius * radius


# parse_positive_number is imported from the shared module `common_utils`


def launch_gui() -> None:
    root = tk.Tk()
    root.title("Circle Area Calculator")
    root.resizable(False, False)

    frm = tk.Frame(root, padx=10, pady=10)
    frm.pack()

    lbl_r = tk.Label(frm, text="Radius:")
    lbl_r.grid(row=0, column=0, sticky="e")
    ent_r = tk.Entry(frm)
    ent_r.grid(row=0, column=1)

    lbl_result = tk.Label(frm, text="Area: -")
    lbl_result.grid(row=1, column=0, columnspan=2, pady=(8, 0))

    def on_calculate() -> None:
        try:
            r = parse_positive_number(ent_r.get().strip())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        area = circle_area(r)
        if area.is_integer():
            area_str = f"{int(area)}"
        else:
            area_str = f"{area:.2f}"
        lbl_result.config(text=f"Area: {area_str}")

    def on_clear() -> None:
        ent_r.delete(0, tk.END)
        lbl_result.config(text="Area: -")
        ent_r.focus_set()

    btn_calc = tk.Button(frm, text="Calculate", command=on_calculate)
    btn_calc.grid(row=2, column=0, pady=(10, 0))

    btn_clear = tk.Button(frm, text="Clear", command=on_clear)
    btn_clear.grid(row=2, column=1, pady=(10, 0))

    ent_r.focus_set()
    root.mainloop()


def main() -> None:
    if len(sys.argv) >= 2:
        try:
            r = parse_positive_number(sys.argv[1])
        except ValueError as e:
            print(f"Error: {e}")
            print("Usage: python area_circle_assignment.py <radius>")
            sys.exit(1)

        area = circle_area(r)
        if area.is_integer():
            area_str = f"{int(area)}"
        else:
            area_str = f"{area:.2f}"
        print(f"The area of the circle with radius {r} is {area_str}.")
    else:
        launch_gui()


if __name__ == '__main__':
    main()
