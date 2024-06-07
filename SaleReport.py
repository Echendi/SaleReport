import csv
import os

path = 'items.csv'


def _ensure_csv_exists():
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["valorItem", "descuentoItem", "medioPago"])


class SaleReport:
    def __init__(self):
        self.items = []
        _ensure_csv_exists()

    def load_items_from_csv(self):
        self.items = []
        try:
            with open(path, 'r', newline='') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.items.append((row["valorItem"], row["descuentoItem"], row["medioPago"]))

            return self.items
        except FileNotFoundError:
            print("El archivo CSV no existe.")

    def save_to_csv(self, valor_item, discount, paid_method):
        if discount > valor_item:
            raise ValueError("El valor del item debe ser mayor al valor de descuento.")
        try:
            with open(path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([valor_item, discount, paid_method])
                self.items.append((valor_item, discount, paid_method))
        except Exception as e:
            raise Exception("Error al guardar en el archivo CSV:", e)

    def delete_item(self, row_index):
        if row_index < 0 or row_index >= len(self.items):
            raise IndexError("El índice de la fila está fuera de rango.")
        del self.items[row_index]
        self._save_all_items_to_csv()

    def update_item(self, row_index, new_valor_item, new_discount, new_paid_method):
        if row_index < 0 or row_index >= len(self.items):
            raise IndexError("El índice de la fila está fuera de rango.")
        self.items[row_index] = (new_valor_item, new_discount, new_paid_method)
        self._save_all_items_to_csv()

    def _save_all_items_to_csv(self):
        try:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["valorItem", "descuentoItem", "medioPago"])  # Escribir encabezados
                writer.writerows(self.items)
        except Exception as e:
            raise Exception("Error al guardar en el archivo CSV:", e)

    def calculate_total(self):
        general_total = 0
        cash_total = 0
        nequi_total = 0
        daviplata_total = 0
        datafono_total = 0
        general_discount = 0
        cash_discount = 0
        nequi_discount = 0
        daviplata_discount = 0
        datafono_discount = 0

        for item in self.items:
            general_total += int(item[0])
            general_discount += int(item[1])

            paid_method = item[2]
            if paid_method == "EFECTIVO":
                cash_total += int(item[0])
                cash_discount += int(item[1])
            if paid_method == "DAVIPLATA":
                daviplata_total += int(item[0])
                daviplata_discount += int(item[1])
            if paid_method == "NEQUI":
                nequi_total += int(item[0])
                nequi_discount += int(item[1])
            if paid_method == "DATAFONO":
                datafono_total += int(item[0])
                datafono_discount += int(item[1])

        return {
            "general_total": general_total,
            "cash_total": cash_total,
            "nequi_total": nequi_total,
            "daviplata_total": daviplata_total,
            "datafono_total": datafono_total,
            "general_discount": general_discount,
            "cash_discount": cash_discount,
            "nequi_discount": nequi_discount,
            "daviplata_discount": daviplata_discount,
            "datafono_discount": datafono_discount
        }


if __name__ == '__main__':
    print(SaleReport().load_items_from_csv())
