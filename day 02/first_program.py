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
	if len(sys.argv) >= 3:
		try:
			base = parse_positive_number(sys.argv[1])
			altezza = parse_positive_number(sys.argv[2])
		except ValueError as e:
			print(f"Errore: {e}")
			print("Uso: python first_program.py <base> <altezza>")
			sys.exit(1)
	else:
		try:
			base = parse_positive_number(input("Inserisci la base del rettangolo: ").strip())
			altezza = parse_positive_number(input("Inserisci l'altezza del rettangolo: ").strip())
		except ValueError as e:
			print(f"Errore: {e}")
			sys.exit(1)

	area = area_rettangolo(base, altezza)
	# Stampo con due decimali se ci sono parti decimali
	if area.is_integer():
		area_str = f"{int(area)}"
	else:
		area_str = f"{area:.2f}"

	print(f"L'area del rettangolo di base {base} e altezza {altezza} è {area_str}.")


if __name__ == '__main__':
	main()

