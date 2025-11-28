import tkinter as tk
from tkinter import ttk


def open_cost_window(root: tk.Tk):
    win = tk.Toplevel(root)
    win.title("KTJ (LPGJPZ) Költségelemző")

    frame_input = tk.Frame(win)
    frame_input.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(frame_input, text="Megnevezés").grid(row=0, column=0, padx=3, pady=3)
    tk.Label(frame_input, text="Összeg").grid(row=0, column=1, padx=3, pady=3)

    name_var = tk.StringVar()
    price_var = tk.StringVar()

    entry_name = tk.Entry(frame_input, textvariable=name_var)
    entry_name.grid(row=1, column=0, padx=3, pady=3)

    entry_price = tk.Entry(frame_input, textvariable=price_var)
    entry_price.grid(row=1, column=1, padx=3, pady=3)

    tree = ttk.Treeview(win, columns=("name", "price"), show="headings", height=8)
    tree.column("name", width=200)
    tree.column("price", width=100)
    tree.heading("name", text="Megnevezés")
    tree.heading("price", text="Összeg")
    tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    total_var = tk.StringVar(value="Összesen: 0")

    label_total = tk.Label(win, textvariable=total_var)
    label_total.pack(pady=5)

    def add_item():
        name = name_var.get().strip()
        price_text = price_var.get().strip()
        if not name or not price_text:
            return
        try:
            price = float(price_text.replace(",", "."))
        except ValueError:
            return
        tree.insert("", tk.END, values=(name, price))
        name_var.set("")
        price_var.set("")
        update_total()

    def update_total():
        total = 0.0
        for item in tree.get_children():
            values = tree.item(item, "values")
            try:
                total += float(values[1])
            except Exception:
                pass
        total_var.set("Összesen: " + str(round(total, 2)))

    btn_add = tk.Button(frame_input, text="Hozzáadás", command=add_item)
    btn_add.grid(row=1, column=2, padx=3, pady=3)
