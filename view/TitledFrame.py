import tkinter as tk
from tkinter import ttk


class TitledFrame(tk.Frame):
    def __init__(self, parent, title="", *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = ttk.Label(self, text=title, font=("Arial", 12, "bold"))
        self.title_label.pack(side="top", fill="x", pady=0)

        self.content_frame = ttk.Frame(self, borderwidth=1, relief="groove")
        self.content_frame.pack(side="top", fill="both", expand=True, padx=5, pady=0)
