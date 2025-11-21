# src/launcher_gui.py
import subprocess, os, threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
# --- at top of src/launcher_gui.py ---
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_ROOT / "scripts"
RESULTS = PROJECT_ROOT / "results"
ICON_PATH = PROJECT_ROOT / "assets" / "icon.ico"

def run_and_open(cmd, status_lbl, buttons):
    for b in buttons: b.config(state="disabled")
    status_lbl.config(text="Running...")

    def worker():
        try:
            proc = subprocess.run(cmd, cwd=PROJECT_ROOT)
            if proc.returncode != 0:
                messagebox.showerror("Chem-Reporter", f"Exit code: {proc.returncode}")
            else:
                if RESULTS.exists():
                    os.startfile(RESULTS)  # Windows: apre la cartella results
        except Exception as e:
            messagebox.showerror("Chem-Reporter", f"Error: {e}")
        finally:
            status_lbl.config(text="Ready")
            for b in buttons: b.config(state="normal")

    threading.Thread(target=worker, daemon=True).start()

def run_manual(status_lbl, buttons):
    run_and_open(["cmd", "/c", str(SCRIPTS / "run_app.bat")], status_lbl, buttons)

def run_csv(status_lbl, buttons):
    path = filedialog.askopenfilename(
        title="Select CSV",
        filetypes=[("CSV files", "*.csv")],
        initialdir=(PROJECT_ROOT / "input")
    )
    if not path:
        return
    run_and_open(["cmd", "/c", str(SCRIPTS / "run_batch.bat"), path], status_lbl, buttons)

def main():
    root = tk.Tk()
    root.title("Chem-Reporter Launcher")
    if ICON_PATH.exists():
        root.iconbitmap(default=str(ICON_PATH))

    frame = tk.Frame(root, padx=16, pady=16)
    frame.pack()

    status_lbl = tk.Label(frame, text="Ready")
    status_lbl.pack(pady=(0, 12))

    btn_manual = tk.Button(frame, text="Insert manually", width=24)
    btn_csv    = tk.Button(frame, text="Insert CSV",      width=24)
    buttons = [btn_manual, btn_csv]

    btn_manual.config(command=lambda: run_manual(status_lbl, buttons))
    btn_csv.config(command=lambda: run_csv(status_lbl, buttons))

    btn_manual.pack(pady=6)
    btn_csv.pack(pady=6)

    root.mainloop()

if __name__ == "__main__":
    main()
