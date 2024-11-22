import csv
import os
import locale
from time import sleep
import tkinter as tk
from tkinter import messagebox

def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(       
                {                    
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

def save_data(filepath, products):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products) 
    print(f"Data successfully saved to {filepath}")

def remove_product(products, id):
    temp_product = None
    for product in products:
        if product["id"] == id:
            temp_product = product
            break
    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"

def view_inventory(products):
    header = f"{'#':<6} {'NAMN':<36} {'BESKRIVNING':<71} {'PRIS':<15} {'KVANTITET':<11}"
    separator = "-" * 140
    rows = []
    for index, product in enumerate(products, 1):
        name = product['name']
        desc = product['desc']
        price = product['price']
        quantity = product['quantity']
        
        price = locale.currency(price, grouping=True)
        row = f"{index:<5} {name:<35} {desc:<70} {price:<22} {quantity:<10}"
        rows.append(row)
    inventory_table = "\n".join([header, separator] + rows)
    return f"{inventory_table}"

def view_product(products, id):
    for product in products:
        if product["id"] == id:
            return f"Visar produkt: {product['name']} {product['desc']}"
    return "Produkten hittas inte"

def view_products(products):
    product_list = []
    for index, product in enumerate(products, 1):
        product_info = f"{index}) (#{product['id']}) {product['name']} \t {product['desc']} \t {locale.currency(product['price'], grouping=True)}"
        product_list.append(product_info)
    return "\n".join(product_list)

def add_product(products, name, desc, price, quantity):
    max_id = max(products, key=lambda x: x['id'])
    id_value = max_id['id']
    id = id_value + 1
    products.append(
        {
            "id": id,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity
        }
    )
    return f"Lade till produkt"

def change_product(product, name, desc, price, quantity):
    product['name'] = name
    product['desc'] = desc
    product['price'] = price
    product['quantity'] = quantity
    return f"Product with id:{id} was changed"

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product Inventory Management")
        self.geometry("1000x600")
        self.products = load_data('db_products.csv')
        
        self.create_widgets()
        self.update_inventory_view()

    def create_widgets(self):
        self.inventory_text = tk.Text(self, wrap="none", width=120, height=20)
        self.inventory_text.pack(pady=10)

        self.test_button = tk.Button(self, text="TEST", command=self.test)
        self.test_button.pack(side="left", padx=10)

    def update_inventory_view(self):
        self.inventory_text.delete(1.0, tk.END)
        self.inventory_text.insert(tk.END, view_inventory(self.products))

    def test(self):
        TestWindow(self)

class TestWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Test Window")
        self.geometry("400x300")
        self.parent = parent

if __name__ == "__main__":
    app = App()
    app.mainloop()