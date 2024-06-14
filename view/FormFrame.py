import tkinter as tk
from tkinter import ttk
from . import TitledFrame


def validate_numbers(value):
    if value == "":
        return True
    elif value.isdigit():
        return True
    elif value.count('.') == 1 and value.replace('.', '').isdigit():
        return True
    return False


class FormFrame(tk.Frame):
    def __init__(self, master=None, insert_item=None):
        super().__init__(master)

        self.form_frame = None
        self.root = master

        self.insert_item = insert_item

        self.valorItem_var = tk.StringVar()
        self.descuentoItem_var = tk.StringVar()
        self.medioPago_var = tk.StringVar(value="EFECTIVO")

        self.create()

    def create(self):

        self.form_frame = TitledFrame.TitledFrame(self, title="Ingresar nuevo registro")
        self.form_frame.pack(side=tk.BOTTOM, padx=30)

        ttk.Label(self.form_frame.content_frame, text="Valor del Item:", foreground="blue").grid(row=2, column=0,
                                                                                                 sticky="e", padx=25,
                                                                                                 pady=0)
        valor_entry = ttk.Entry(self.form_frame.content_frame, textvariable=self.valorItem_var)
        valor_entry.grid(row=2, column=1, padx=5, pady=5)
        valor_entry.config(validate="key", validatecommand=(self.root.register(validate_numbers), "%P"))

        ttk.Label(self.form_frame.content_frame, text="Descuento:", foreground="green").grid(row=3, column=0,
                                                                                             sticky="e", padx=25,
                                                                                             pady=0)
        descuento_entry = ttk.Entry(self.form_frame.content_frame, textvariable=self.descuentoItem_var)
        descuento_entry.grid(row=3, column=1, padx=5, pady=5)
        descuento_entry.config(validate="key", validatecommand=(self.root.register(validate_numbers), "%P"))

        ttk.Label(self.form_frame.content_frame, text="Medio de pago:", foreground="red").grid(row=4, column=0,
                                                                                               sticky="e", padx=25,
                                                                                               pady=0)
        medio_pago_combobox = ttk.Combobox(self.form_frame.content_frame, textvariable=self.medioPago_var,
                                           values=["EFECTIVO", "NEQUI", "DAVIPLATA", "DATAFONO"])
        medio_pago_combobox.grid(row=4, column=1, padx=5, pady=5)
        medio_pago_combobox.config(width=15)

        (ttk.Button(self.form_frame.content_frame, text="Insertar registro", command=self.insert_item,
                    style="Accent.TButton")
         .grid(row=5, column=0, columnspan=2, pady=10))
        pass
