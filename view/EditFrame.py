import tkinter as tk
from tkinter import ttk
from .FormFrame import validate_numbers
from . import TitledFrame


class EditFrame(tk.Frame):
    def __init__(self, master=None, edit_item=None):
        super().__init__(master)

        self.frame = None
        self.root = master

        self.edit_item = edit_item

        self.item_number = tk.StringVar()
        self.valorItem_var = tk.StringVar()
        self.descuentoItem_var = tk.StringVar()
        self.medioPago_var = tk.StringVar(value="EFECTIVO")

        self.create()

    def create(self):
        self.frame = TitledFrame.TitledFrame(self, title="Editar registro seleccionado")
        self.frame.pack(side=tk.TOP, padx=30, pady=15, fill=tk.BOTH)

        ttk.Label(self.frame.content_frame, text="Item Numero:").grid(row=2, column=0, sticky="e", padx=25, pady=0)
        number_entry = ttk.Entry(self.frame.content_frame, textvariable=self.item_number)
        number_entry.config(state='disabled')
        number_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame.content_frame, text="Valor del Item:", foreground="blue").grid(row=3, column=0,
                                                                                            sticky="e", padx=25,
                                                                                            pady=0)
        valor_entry = ttk.Entry(self.frame.content_frame, textvariable=self.valorItem_var)
        valor_entry.grid(row=3, column=1, padx=5, pady=5)
        valor_entry.config(validate="key", validatecommand=(self.root.register(validate_numbers), "%P"))

        ttk.Label(self.frame.content_frame, text="Descuento:", foreground="green").grid(row=3, column=2,
                                                                                        sticky="e", padx=25,
                                                                                        pady=0)
        descuento_entry = ttk.Entry(self.frame.content_frame, textvariable=self.descuentoItem_var)
        descuento_entry.grid(row=3, column=3, padx=5, pady=5)
        descuento_entry.config(validate="key", validatecommand=(self.root.register(validate_numbers), "%P"))

        ttk.Label(self.frame.content_frame, text="Medio de pago:", foreground="red").grid(row=3, column=4,
                                                                                          sticky="e", padx=25,
                                                                                          pady=0)
        medio_pago_combobox = ttk.Combobox(self.frame.content_frame, textvariable=self.medioPago_var,
                                           values=["EFECTIVO", "NEQUI", "DAVIPLATA", "DATAFONO"])
        medio_pago_combobox.grid(row=3, column=5, padx=5, pady=5)
        medio_pago_combobox.config(width=15)

        (ttk.Button(self.frame.content_frame, text="Editar registro", command=self.edit_item,
                    style="Accent.TButton")
         .grid(row=3, column=6, pady=10))
        pass
