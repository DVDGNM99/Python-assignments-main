#!/usr/bin/env python3
"""Small program to calculate the area of a rectangle.

Usage:
 - Interactive: run the script and enter base and height when prompted.
 - From command line: python first_program.py <base> <height>

The program accepts numbers using either comma or dot as decimal separator
and validates that values are positive.
"""
import os
import sys
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


def rectangle_area(base: float, height: float) -> float:
    return base * height


def main() -> None:
    # If two arguments are provided, keep CLI mode for compatibility
    if len(sys.argv) >= 3:
        try:
            base = parse_positive_number(sys.argv[1])
            height = parse_positive_number(sys.argv[2])
        except ValueError as e:
            print(f"Error: {e}")
            print("Usage: python first_program.py <base> <height>")
            sys.exit(1)

        area = rectangle_area(base, height)
        # Print with two decimals if there are fractional parts
        if area.is_integer():
            area_str = f"{int(area)}"
        else:
            area_str = f"{area:.2f}"

        print(f"The area of the rectangle with base {base} and height {height} is {area_str}.")
    else:
        # GUI mode
        launch_gui()


def launch_gui() -> None:
    root = tk.Tk()
    root.title("Rectangle Area Calculator")
    root.resizable(False, False)

    frm = tk.Frame(root, padx=10, pady=10)
    frm.pack()

    lbl_base = tk.Label(frm, text="Base:")
    lbl_base.grid(row=0, column=0, sticky="e")
    ent_base = tk.Entry(frm)
    ent_base.grid(row=0, column=1)

    lbl_height = tk.Label(frm, text="Height:")
    lbl_height.grid(row=1, column=0, sticky="e")
    ent_height = tk.Entry(frm)
    ent_height.grid(row=1, column=1)

    lbl_result = tk.Label(frm, text="Area: -")
    lbl_result.grid(row=2, column=0, columnspan=2, pady=(8, 0))

    def on_calculate() -> None:
        try:
            b = parse_positive_number(ent_base.get().strip())
            h = parse_positive_number(ent_height.get().strip())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        area = rectangle_area(b, h)
        if area.is_integer():
            area_str = f"{int(area)}"
        else:
            area_str = f"{area:.2f}"

        lbl_result.config(text=f"Area: {area_str}")

    def on_clear() -> None:
        ent_base.delete(0, tk.END)
        ent_height.delete(0, tk.END)
        lbl_result.config(text="Area: -")
        ent_base.focus_set()

    btn_calc = tk.Button(frm, text="Calculate", command=on_calculate)
    btn_calc.grid(row=3, column=0, pady=(10, 0))

    btn_clear = tk.Button(frm, text="Clear", command=on_clear)
    btn_clear.grid(row=3, column=1, pady=(10, 0))

    ent_base.focus_set()
    root.mainloop()


if __name__ == '__main__':
    main()
