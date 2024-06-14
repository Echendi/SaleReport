import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog
import os
import locale

from SaleReport import SaleReport
from view.EditFrame import EditFrame
from view.FormFrame import FormFrame
from view.RecordTable import RecordTable
from view.ReportFrame import ReportFrame
from view.TotalTable import TotalTable
from view.DataFrame import DataFrame


class App:
    instance = None

    def __init__(self, root):
        self.scrollable_frame = None
        self.data_frame = None
        self.form_frame = None
        self.report_frame = None
        self.edit_frame = None
        self.totals_table = None
        self.table = None
        self.style = None

        self.sale_report = SaleReport()
        self.index = 1
        self.root = root
        self.root.title("Registro de Pagos")

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
        # Crear un marco que contendrá el canvas y el scrollbar
        container = ttk.Frame(self.root)
        container.grid(row=0, column=0, sticky="nsew")

        # Crear un canvas y agregarlo al marco
        canvas = tk.Canvas(container)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Crear una barra de desplazamiento vertical y agregarla al marco
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar el canvas para usar la barra de desplazamiento
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un marco interior dentro del canvas
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Crear una ventana dentro del canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurar expansión del canvas y del marco contenedor
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        canvas.grid_rowconfigure(0, weight=1)
        canvas.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Agregar widgets al marco interior
        self.data_frame = DataFrame(master=self.scrollable_frame)
        self.data_frame.grid(row=0, column=0, sticky='ew')

        self.totals_table = TotalTable(self.scrollable_frame)
        self.totals_table.grid(row=1, column=0, sticky='nsew', padx=15, pady=0)

        self.form_frame = FormFrame(master=self.scrollable_frame, insert_item=self.insert_item)
        self.form_frame.grid(row=1, column=1, sticky='nsew')

        self.report_frame = ReportFrame(master=self.scrollable_frame, export_to_pdf=self.export_to_pdf)
        self.report_frame.grid(row=0, column=1, sticky='nsew', pady=30)

        separator = ttk.Separator(self.scrollable_frame, orient="horizontal")
        separator.grid(row=3, column=0, sticky='nsew', padx=15, pady=15, columnspan=2)

        self.table = RecordTable(self.scrollable_frame, self.on_button_click)
        self.table.grid(row=4, column=0, sticky='nsew', columnspan=2)

        self.edit_frame = EditFrame(master=self.scrollable_frame, edit_item=self.edit_item)
        self.edit_frame.grid(row=5, column=0, sticky='nsew', columnspan=2)

        # Configurar expansión para el contenedor
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

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
            self.table.table.insert("", "end", text=str(self.index),
                                    values=(format_number(valor_item), format_number(descuento_item), medio_pago))
            self.index += 1
            self.clear_form()
            self.sale_report.save_to_csv(float(valor_item), float(descuento_item), medio_pago)
            self.update_totals()

    def edit_item(self):
        row = self.edit_frame.item_number.get()
        if messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas editar el item #{row}?"):
            valor_item = self.edit_frame.valorItem_var.get()
            descuento_item = self.edit_frame.descuentoItem_var.get()
            medio_pago = self.edit_frame.medioPago_var.get()
            self.clear_form()
            self.sale_report.update_item(row, float(valor_item), float(descuento_item), medio_pago)
            self.reset_data()

    def clear_form(self):
        self.form_frame.valorItem_var.set("")
        self.form_frame.descuentoItem_var.set("")
        self.form_frame.medioPago_var.set("EFECTIVO")

    def update_totals(self):
        totals = self.sale_report.calculate_total()
        yi_sqp = self.sale_report.calculate_yi_sqp(totals)

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

        self.report_frame.yi_sqp_value.set(format_number(yi_sqp))

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

    def on_button_click(self, event):
        item = self.table.table.identify('item', event.x, event.y)
        row = self.table.table.item(item, 'text')
        values = self.table.table.item(item, 'values')
        if row:
            self.edit_frame.item_number.set(row)
            self.edit_frame.valorItem_var.set(unformat_number(values[0]))
            self.edit_frame.descuentoItem_var.set(unformat_number(values[1]))
            self.edit_frame.medioPago_var.set(values[2])

    def reset_data(self):
        self.index = 1
        self.table.table.delete(*self.table.table.get_children())
        self.load_items()
        self.update_totals()

    def export_to_pdf(self):
        location = self.data_frame.lugar_var.get()
        date_name = self.data_frame.calendar.get_date().strftime("%d-%m-%Y")
        if messagebox.askyesno("Confirmación", f"Se generará reporte para las fecha {date_name} "
                                               f"en {location if location else 'SIN LUGAR'}\n"
                                               "¿Estás seguro de que deseas generar el reporte?"
                                               "\nEsta acción limpiará los registros actuales"):
            if self.generate_pdf():
                self.sale_report.clear_csv()
                self.reset_data()

    def generate_pdf(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        location = self.data_frame.lugar_var.get()
        date_name = self.data_frame.calendar.get_date().strftime("%d-%m-%Y")
        date = self.data_frame.calendar.get_date().strftime("%d %B %Y")

        # Mostrar diálogo para guardar archivo y obtener la ruta
        filename = filedialog.asksaveasfilename(
            initialfile=f"{date_name}_{location}",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if not filename:
            return  # Si el usuario cancela el diálogo, salir de la función

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        c.drawString(50, height - 50, location)
        c.drawString(width - 150, height - 50, date)

        # Primera tabla: Totales
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 80, "Totales")

        # Encabezados de la primera tabla
        c.setFont("Helvetica-Bold", 12)
        headers = ["Categoría", "Total", "Descuento"]
        x_offset = 50
        y_offset = height - 120
        c.drawString(x_offset, y_offset, headers[0])
        for i, header in enumerate(headers[1:], start=1):
            c.drawString(x_offset + i * 100, y_offset, header)

        # Línea debajo de los encabezados
        c.line(50, y_offset - 2, width - 50, y_offset - 2)

        # Filas de la primera tabla
        c.setFont("Helvetica", 12)
        y = y_offset - 25  # Posición inicial Y para las filas
        for item_id in self.totals_table.totals_table.get_children():
            item = self.totals_table.totals_table.item(item_id)
            row_text = [item['text']] + list(map(str, item["values"]))

            # Verificar si hay suficiente espacio para la próxima fila
            if y < 50:
                c.showPage()  # Agregar una nueva página
                c.drawString(50, height - 50, location)
                c.drawString(width - 150, height - 50, date)
                y = height - 120  # Reiniciar Y para la nueva página

                # Encabezados de la primera tabla en la nueva página
                c.setFont("Helvetica-Bold", 12)
                c.drawString(x_offset, y_offset, headers[0])
                for i, header in enumerate(headers[1:], start=1):
                    c.drawString(x_offset + i * 100, y_offset, header)

                # Línea debajo de los encabezados en la nueva página
                c.line(50, y_offset - 2, width - 50, y_offset - 2)

            c.drawString(x_offset, y, row_text[0])
            for i, text in enumerate(row_text[1:], start=1):
                c.drawString(x_offset + i * 100, y, text)
            y -= 30  # Espacio entre filas

            # Línea debajo de cada fila
            c.line(50, y + 25, width - 50, y + 25)

        c.drawString(100, y - 15, "YI_SQP: " + self.report_frame.yi_sqp_value.get())
        # Espacio entre las dos tablas
        y -= 50

        # Segunda tabla: Registros
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y - 30, "Registros")

        # Encabezados de la segunda tabla
        c.setFont("Helvetica-Bold", 12)
        headers = ["Número", "Valor", "Descuento", "Medio de pago"]
        x_offset = 50
        y_offset = y - 70
        c.drawString(x_offset, y_offset, headers[0])
        for i, header in enumerate(headers[1:], start=1):
            c.drawString(x_offset + i * 100, y_offset, header)

        # Línea debajo de los encabezados de la segunda tabla
        c.line(50, y_offset - 2, width - 50, y_offset - 2)

        # Filas de la segunda tabla
        c.setFont("Helvetica", 12)
        y = y_offset - 25  # Posición inicial Y para las filas
        for item_id in self.table.table.get_children():
            item = self.table.table.item(item_id)
            row_text = [item['text']] + list(map(str, item["values"]))

            # Verificar si hay suficiente espacio para la próxima fila
            if y < 50:
                c.showPage()  # Agregar una nueva página
                c.drawString(50, height - 50, location)
                c.drawString(width - 150, height - 50, date)
                y = height - 120  # Reiniciar Y para la nueva página

            c.drawString(x_offset, y, row_text[0])
            for i, text in enumerate(row_text[1:], start=1):
                c.drawString(x_offset + i * 100, y, text)
            y -= 30  # Espacio entre filas

            # Línea debajo de cada fila
            c.line(50, y + 25, width - 50, y + 25)

        c.save()

        if os.name == 'posix':  # Para macOS y Linux
            os.system(f'open "{filename}"')
        elif os.name == 'nt':  # Para Windows
            os.startfile(filename)
        return True


def format_number(number):
    return '{:<2}{:>2}'.format('$', '{:,.2f}'.format(float(number)))


def unformat_number(formatted_number):
    clean_number = formatted_number.replace('$', '').replace(',', '').strip()
    return float(clean_number)


def main():
    root = tk.Tk()
    # root.state('zoomed')
    root.minsize(1000, 800)
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
