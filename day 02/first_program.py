#!/usr/bin/env python3
"""Chiedere al copilot di generare un piccolo programma per calcolare l'area di un rettangolo
Calcola l'area di un rettangolo:

Uso:
 - Interattivo: esegui lo script e inserisci base e altezza quando richiesto.
 - Da riga di comando: python first_program.py <base> <altezza>

Il programma accetta numeri con la virgola o il punto come separatore decimale
e verifica che i valori siano positivi.
"""
import sys
import tkinter as tk
from tkinter import messagebox


def area_rettangolo(base: float, altezza: float) -> float:
	return base * altezza


def parse_positive_number(s: str) -> float:
	try:
		# Sostituisco la virgola con il punto per l'input italiano comune
		v = float(s.replace(',', '.'))
	except Exception:
		raise ValueError(f"'{s}' non è un numero valido")
	if v <= 0:
		raise ValueError("Il valore deve essere maggiore di zero")
	return v


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

