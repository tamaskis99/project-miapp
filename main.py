import tkinter as tk
from tkinter import scrolledtext
from ktj_chat_engine import KTJChatEngine
from apps.ktj_costs import open_cost_window
from apps.ktj_notes import open_notes_window
from apps.ktj_timer import open_timer_window
from apps.ktj_calendar import open_calendar_window


class ChatGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = KTJChatEngine()

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.entry = tk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.on_send)

        send_btn = tk.Button(input_frame, text="Küldés", command=self.on_send)
        send_btn.pack(side=tk.RIGHT, padx=5)

        self.chat_box.tag_config("link", foreground="blue", underline=True)
        self.chat_box.tag_bind("link", "<Button-1>", self.on_link_click)

        self._append_text("assistant", "Szia, jelenleg én még egy tanuló fázisban lévő mini MI-modell vagyok, sajnos még nem rendelkezem hivatalos API-val (pl. OpenAI API), hogy minden elvárásodnak megfeleljek, de ígérem, igyekezni fogok kielégítő választ adni kérdéseidre. Esetleg további alkalmazásokat tudok mutatni, ha beírod a 'további alkalmazások' üzenetet.")

    def _append_text(self, role, text):
        self.chat_box.config(state=tk.NORMAL)
        prefix = "Te: " if role == "user" else "MI-mini: "
        self.chat_box.insert(tk.END, prefix + text + "\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    def on_send(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self._append_text("user", user_text)
        self.entry.delete(0, tk.END)
        result = self.engine.generate_reply(user_text)
        reply = result["reply"]
        flags = result.get("flags", {})
        if not flags.get("show_app_link"):
            self._append_text("assistant", reply)
        else:
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, "MI-mini: ")
            self.chat_box.insert(tk.END, reply + " ")
            start_index = self.chat_box.index(tk.END)
            link_text = "[Mini alkalmazások]"
            self.chat_box.insert(tk.END, link_text, ("link",))
            self.chat_box.insert(tk.END, "\n")
            self.chat_box.see(tk.END)
            self.chat_box.config(state=tk.DISABLED)

    def on_link_click(self, event):
        open_app_selector(self.root)


def open_app_selector(root: tk.Tk):
    win = tk.Toplevel(root)
    win.title("Mini alkalmazások")

    label = tk.Label(win, text="Válassz egy mini alkalmazást", font=("Arial", 12))
    label.pack(pady=10)

    btn1 = tk.Button(win, text="Költségelemző", width=20, command=lambda: open_cost_window(root))
    btn1.pack(pady=3)

    btn2 = tk.Button(win, text="Jegyzetelő", width=20, command=lambda: open_notes_window(root))
    btn2.pack(pady=3)

    btn3 = tk.Button(win, text="Időzítő", width=20, command=lambda: open_timer_window(root))
    btn3.pack(pady=3)

    btn4 = tk.Button(win, text="Naptár", width=20, command=lambda: open_calendar_window(root))
    btn4.pack(pady=3)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("KTJ (LPGJPZ) MI Chat")
    root.geometry("800x600")
    app = ChatGUI(root)
    root.mainloop()
