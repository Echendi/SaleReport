import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from . import TitledFrame


class DataFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.date = datetime.today()

        self.data_frame = None
        self.root = master

        self.calendar = None
        self.lugar_var = tk.StringVar()

        self.create()

    def create(self):

        self.data_frame = TitledFrame.TitledFrame(self, title="Datos del reporte")
        self.data_frame.pack(side=tk.TOP, padx=30, pady=10, fill=tk.BOTH)

        ttk.Label(self.data_frame.content_frame, text="").grid(row=0, column=0, padx=30, sticky="ew")

        ttk.Label(self.data_frame.content_frame, text="Fecha: ").grid(row=0, column=1, sticky="ew")
        self.calendar = DateEntry(self.data_frame.content_frame, selectmode="day", year=self.date.year,
                                  month=self.date.month,
                                  day=self.date.day, date_pattern='dd-mm-yyyy', locale="es_ES")
        self.calendar.grid(row=0, column=2, pady=5, sticky="ew")

        ttk.Label(self.data_frame.content_frame, text="").grid(row=0, column=3, padx=50, sticky="ew")

        ttk.Label(self.data_frame.content_frame, text="Lugar o sede: ").grid(row=0, column=4, sticky="ew")
        sede_entry = ttk.Entry(self.data_frame.content_frame, textvariable=self.lugar_var)
        sede_entry.grid(row=0, column=5, pady=5, sticky="ew")
        pass