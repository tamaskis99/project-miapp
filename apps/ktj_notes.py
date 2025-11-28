import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path

NOTES_FILE = Path("ktj_notes.txt")


def open_notes_window(root: tk.Tk):
    win = tk.Toplevel(root)
    win.title("KTJ (LPGJPZ) Jegyzetelő")

    text = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=60, height=20)
    text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    if NOTES_FILE.exists():
        content = NOTES_FILE.read_text(encoding="utf-8")
        text.insert(tk.END, content)

    frame_buttons = tk.Frame(win)
    frame_buttons.pack(fill=tk.X, padx=5, pady=5)

    def save_notes():
        content = text.get("1.0", tk.END)
        NOTES_FILE.write_text(content, encoding="utf-8")

    btn_save = tk.Button(frame_buttons, text="Mentés", command=save_notes)
    btn_save.pack(side=tk.RIGHT)
