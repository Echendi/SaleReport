import tkinter as tk
from tkinter import ttk


class ReportFrame(tk.Frame):
    def __init__(self, master=None, export_to_pdf=None):
        super().__init__(master)

        self.report_frame = None
        self.root = master
        self.yi_sqp_value = tk.StringVar()
        self.export_to_pdf = export_to_pdf
        self.create()

    def create(self):
        self.report_frame = tk.Frame(self)
        self.report_frame.pack(side=tk.TOP, padx=30, fill=tk.BOTH)

        ttk.Label(self.report_frame, text="YI SQP: ").grid(row=0, column=4)
        entry = ttk.Entry(self.report_frame, textvariable=self.yi_sqp_value)
        entry.config(state=tk.DISABLED)
        entry.grid(row=0, column=5)
        btn = tk.Button(self.report_frame, text="Generar Reporte",
                        command=self.generate_report)
        btn.grid(row=0, column=6)
        pass

    def generate_report(self):
        self.export_to_pdf()
