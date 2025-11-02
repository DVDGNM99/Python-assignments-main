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


def area_rettangolo(base: float, altezza: float) -> float:
	return base * altezza

def main() -> None:
	# Se vengono passati due argomenti, mantengo la modalità CLI per compatibilità
	if len(sys.argv) >= 3:
		try:
			base = parse_positive_number(sys.argv[1])
			altezza = parse_positive_number(sys.argv[2])
		except ValueError as e:
			print(f"Errore: {e}")
			print("Uso: python first_program.py <base> <altezza>")
			sys.exit(1)

		area = area_rettangolo(base, altezza)
		# Stampo con due decimali se ci sono parti decimali
		if area.is_integer():
			area_str = f"{int(area)}"
		else:
			area_str = f"{area:.2f}"

		print(f"L'area del rettangolo di base {base} e altezza {altezza} è {area_str}.")
	else:
		# Modalità GUI
		launch_gui()


def launch_gui() -> None:
	root = tk.Tk()
	root.title("Calcolo area rettangolo")
	root.resizable(False, False)

	frm = tk.Frame(root, padx=10, pady=10)
	frm.pack()

	lbl_base = tk.Label(frm, text="Base:")
	lbl_base.grid(row=0, column=0, sticky="e")
	ent_base = tk.Entry(frm)
	ent_base.grid(row=0, column=1)

	lbl_altezza = tk.Label(frm, text="Altezza:")
	lbl_altezza.grid(row=1, column=0, sticky="e")
	ent_altezza = tk.Entry(frm)
	ent_altezza.grid(row=1, column=1)

	lbl_result = tk.Label(frm, text="Area: -")
	lbl_result.grid(row=2, column=0, columnspan=2, pady=(8, 0))

	def on_calculate() -> None:
		try:
			b = parse_positive_number(ent_base.get().strip())
			a = parse_positive_number(ent_altezza.get().strip())
		except ValueError as e:
			messagebox.showerror("Errore", str(e))
			return

		area = area_rettangolo(b, a)
		if area.is_integer():
			area_str = f"{int(area)}"
		else:
			area_str = f"{area:.2f}"

		lbl_result.config(text=f"Area: {area_str}")

	def on_clear() -> None:
		ent_base.delete(0, tk.END)
		ent_altezza.delete(0, tk.END)
		lbl_result.config(text="Area: -")
		ent_base.focus_set()

	btn_calc = tk.Button(frm, text="Calcola", command=on_calculate)
	btn_calc.grid(row=3, column=0, pady=(10, 0))

	btn_clear = tk.Button(frm, text="Pulisci", command=on_clear)
	btn_clear.grid(row=3, column=1, pady=(10, 0))

	ent_base.focus_set()
	root.mainloop()


if __name__ == '__main__':
	main()

