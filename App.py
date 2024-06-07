import tkinter as tk
from tkinter import ttk
from SaleReport import SaleReport

from view.FormFrame import FormFrame
from view.RecordTable import RecordTable
from view.TotalTable import TotalTable
from view.DataFrame import DataFrame


class App:
    instance = None

    def __init__(self, root):
        self.data_frame = None
        self.form_frame = None
        self.totals_table = None
        self.table = None
        self.style = None

        self.sale_report = SaleReport()
        self.index = 1
        self.root = root
        self.root.title("Registro de Pagos")

        """self.valorItem_var = tk.StringVar()
        self.descuentoItem_var = tk.StringVar()
        self.medioPago_var = tk.StringVar(value="EFECTIVO")"""

        self.total_general = tk.StringVar(value="0.0")
        self.total_efectivo = tk.StringVar(value="0.0")
        self.total_nequi = tk.StringVar(value="0.0")
        self.total_daviplata = tk.StringVar(value="0.0")
        self.total_datafono = tk.StringVar(value="0.0")

        self.discount_general = tk.StringVar(value="0.0")
        self.discount_efectivo = tk.StringVar(value="0.0")
        self.discount_nequi = tk.StringVar(value="0.0")
        self.discount_daviplata = tk.StringVar(value="0.0")
        self.discount_datafono = tk.StringVar(value="0.0")

        self.create_widgets()

        App.instance = self

    def create_widgets(self):

        self.data_frame = DataFrame(master=self.root)
        self.data_frame.grid(row=0, column=0, sticky='nsew', columnspan=2)

        self.totals_table = TotalTable(self.root)
        self.totals_table.grid(row=1, column=0, sticky='nsew', padx=15, pady=0)

        self.form_frame = FormFrame(master=self.root, insert_item=self.insert_item)
        self.form_frame.grid(row=1, column=1, sticky='nsew')

        separator = ttk.Separator(self.root, orient="horizontal")
        separator.grid(row=2, column=0, sticky='nsew', padx=15, pady=15, columnspan=2)

        self.table = RecordTable(self.root)
        self.table.grid(row=3, column=0, sticky='nsew', columnspan=2)

        # Cargar los datos del CSV en la tabla al iniciar la aplicación
        self.load_items()

    def load_items(self):
        new_items = self.sale_report.load_items_from_csv()
        if new_items is None:
            new_items = []
        for row in new_items:
            self.table.table.insert("", "end", text=str(self.index),
                              values=(format_number(row[0]), format_number(row[1]), row[2]))
            self.index += 1
        self.update_totals()

    def insert_item(self):
        valor_item = self.form_frame.valorItem_var.get()
        descuento_item = self.form_frame.descuentoItem_var.get()
        medio_pago = self.form_frame.medioPago_var.get()

        if medio_pago != "Seleccione":
            self.table.insert("", "end", text=str(self.index),
                              values=(format_number(valor_item), format_number(descuento_item), medio_pago))
            self.index += 1
            self.clear_form()
            self.sale_report.save_to_csv(int(valor_item), int(descuento_item), medio_pago)
            self.update_totals()

    def clear_form(self):
        self.form_frame.valorItem_var.set("")
        self.form_frame.descuentoItem_var.set("")
        self.form_frame.medioPago_var.set("EFECTIVO")

    def update_totals(self):
        totals = self.sale_report.calculate_total()
        self.total_general.set(format_number(totals["general_total"]))
        self.total_efectivo.set(format_number(totals["cash_total"]))
        self.total_nequi.set(format_number(totals["nequi_total"]))
        self.total_daviplata.set(format_number(totals["daviplata_total"]))
        self.total_datafono.set(format_number(totals["datafono_total"]))

        self.discount_general.set(format_number(totals["general_discount"]))
        self.discount_efectivo.set(format_number(totals["cash_discount"]))
        self.discount_nequi.set(format_number(totals["nequi_discount"]))
        self.discount_daviplata.set(format_number(totals["daviplata_discount"]))
        self.discount_datafono.set(format_number(totals["datafono_discount"]))

        self.totals_table.totals_table.item(self.totals_table.totals_table.get_children()[0],
                               values=(self.total_general.get(), self.discount_general.get()))
        self.totals_table.totals_table.item(self.totals_table.totals_table.get_children()[1],
                               values=(self.total_efectivo.get(), self.discount_efectivo.get()))
        self.totals_table.totals_table.item(self.totals_table.totals_table.get_children()[2],
                               values=(self.total_nequi.get(), self.discount_nequi.get()))
        self.totals_table.totals_table.item(self.totals_table.totals_table.get_children()[3],
                               values=(self.total_daviplata.get(), self.discount_daviplata.get()))
        self.totals_table.totals_table.item(self.totals_table.totals_table.get_children()[4],
                               values=(self.total_datafono.get(), self.discount_datafono.get()))


def format_number(number):
    return '{:<2}{:>25}'.format('$', '{:,.2f}'.format(float(number)))


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
