import tkinter as tk


def open_timer_window(root: tk.Tk):
    win = tk.Toplevel(root)
    win.title("KTJ (LPGJPZ) Időzítő")

    tk.Label(win, text="Másodpercek száma").pack(pady=5)
    seconds_var = tk.StringVar()
    entry = tk.Entry(win, textvariable=seconds_var)
    entry.pack(pady=5)

    time_var = tk.StringVar(value="00:00")
    label_time = tk.Label(win, textvariable=time_var, font=("Arial", 20))
    label_time.pack(pady=10)

    status_var = tk.StringVar(value="")
    label_status = tk.Label(win, textvariable=status_var)
    label_status.pack(pady=5)

    def format_time(sec):
        m = sec // 60
        s = sec % 60
        return f"{m:02d}:{s:02d}"

    def tick(remaining):
        if remaining < 0:
            status_var.set("Lejárt az idő")
            return
        time_var.set(format_time(remaining))
        win.after(1000, lambda: tick(remaining - 1))

    def start_timer():
        status_var.set("")
        try:
            total = int(seconds_var.get())
        except ValueError:
            status_var.set("Érvénytelen szám")
            return
        tick(total)

    btn_start = tk.Button(win, text="Indítás", command=start_timer)
    btn_start.pack(pady=5)
