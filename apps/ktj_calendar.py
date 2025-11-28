import tkinter as tk
import datetime
import calendar


def open_calendar_window(root: tk.Tk):
    win = tk.Toplevel(root)
    win.title("KTJ (LPGJPZ) Naptár")

    today = datetime.date.today()
    year = today.year
    month = today.month

    label_title = tk.Label(win, text=f"{year}. {month}. hónap", font=("Arial", 12))
    label_title.pack(pady=5)

    frame_days = tk.Frame(win)
    frame_days.pack(padx=5, pady=5)

    days = ["H", "K", "Sze", "Cs", "P", "Sz", "V"]
    for i, d in enumerate(days):
        tk.Label(frame_days, text=d, width=4, font=("Arial", 10, "bold")).grid(row=0, column=i)

    month_cal = calendar.monthcalendar(year, month)

    for row_index, week in enumerate(month_cal, start=1):
        for col_index, day in enumerate(week):
            text = "" if day == 0 else str(day)
            if day == today.day:
                lbl = tk.Label(frame_days, text=text, width=4, bg="lightblue")
            else:
                lbl = tk.Label(frame_days, text=text, width=4)
            lbl.grid(row=row_index, column=col_index, padx=1, pady=1)
