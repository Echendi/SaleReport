import tkinter as tk
from tkinter import ttk


class TotalTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.totals_table = None
        self.style = None
        self.root = master
        self.create()

    def create(self):
        monospace_font = ('Courier New', 12)

        self.style = ttk.Style()
        self.style.configure("Blue.TLabel", foreground="blue")
        self.style.configure("Green.TLabel", foreground="green")
        self.style.configure("Purple.TLabel", foreground="purple")
        self.style.configure("Red.TLabel", foreground="red")
        self.style.configure("Orange.TLabel", foreground="orange")

        # Tabla de totales
        title_label = ttk.Label(self, text="Tabla de Totales", style="Blue.TLabel")
        title_label.grid(row=0, column=0, columnspan=4)

        self.totals_table = ttk.Treeview(self, columns=("Total", "Descuento"), height=5)
        self.totals_table.heading("#0", text="Categoría", anchor="center")
        self.totals_table.heading("Total", text="Total", anchor="center")
        self.totals_table.heading("Descuento", text="Descuento", anchor="center")

        self.totals_table.column("Total", anchor="e")
        self.totals_table.column("Descuento", anchor="e")

        self.totals_table.tag_configure("blue", foreground="blue", font=('Courier New', 12, "bold"))
        self.totals_table.tag_configure("green", foreground="green",font=monospace_font)
        self.totals_table.tag_configure("purple", foreground="purple",font=monospace_font)
        self.totals_table.tag_configure("red", foreground="red",font=monospace_font)
        self.totals_table.tag_configure("orange", foreground="orange",font=monospace_font)

        self.totals_table.insert("", "end", text="Total", values=(0, 0), tags=("blue",))
        self.totals_table.insert("", "end", text="Efectivo", values=(0, 0), tags=("green",))
        self.totals_table.insert("", "end", text="Nequi", values=(0, 0), tags=("purple",))
        self.totals_table.insert("", "end", text="Daviplata", values=(0, 0), tags=("red",))
        self.totals_table.insert("", "end", text="Datafono", values=(0, 0), tags=("orange",))
        self.totals_table.grid(row=1, column=0, columnspan=4, pady=10, rowspan=3)
        pass
