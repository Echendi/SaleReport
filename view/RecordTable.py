import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class RecordTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.tree_frame = None
        self.frame = None
        self.table = None
        self.root = master
        self.create()

    def create(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(self.frame, text="Tabla de Registros", font=("Arial", 15))
        title_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=0)

        self.frame = ttk.Frame(self.frame)
        self.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.table = ttk.Treeview(self.tree_frame, columns=("Valor Item", "Descuento", "Medio de pago"))

        self.table.heading("#0", text="Numero")
        self.table.heading("Valor Item", text="Valor Item")
        self.table.heading("Descuento", text="Descuento")
        self.table.heading("Medio de pago", text="Medio de pago")

        self.table.column("Valor Item", anchor="e")
        self.table.column("Descuento", anchor="e")
        self.table.column("Medio de pago", anchor="e")

        self.table.bind("<Button-1>", self.on_button_click)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.table["height"] = 15

        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.table.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=vsb.set)
        pass

    def on_button_click(self, event):
        item = self.table.identify('item', event.x, event.y)
        column = self.table.identify('column', event.x, event.y)
        messagebox.showinfo("Button Clicked", f"Button in row {self.table.item(item, 'text')} clicked!")
