import csv
import os
import locale
from time import sleep
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Projekt.py: De e en projekt som använder tkinter, med förra uppgift som bas.

__author__  = "Ott Rudolf Pöld"
__version__ = "4.0.0"
__email__   = "Ott.Pold@elev.ga.ntig.se"

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
        self.geometry("1200x600")
        self.products = load_data('db_products.csv')
        self.sort_by = None
        self.sort_asc = True

        self.create_widgets()
        self.update_inventory_view()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Description", "Price", "Quantity"), show='headings')
        self.tree.heading("ID", text="ID", command=lambda: self.sort_treeview("ID", False))
        self.tree.heading("Name", text="Name", command=lambda: self.sort_treeview("Name", False))
        self.tree.heading("Description", text="Description", command=lambda: self.sort_treeview("Description", False))
        self.tree.heading("Price", text="Price", command=lambda: self.sort_treeview("Price", True))
        self.tree.heading("Quantity", text="Quantity", command=lambda: self.sort_treeview("Quantity", False))

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=200)
        self.tree.column("Description", width=400)
        self.tree.column("Price", width=100)
        self.tree.column("Quantity", width=100)

        self.tree.pack(fill="both", expand=True, pady=20)


        self.add_button = tk.Button(self, text="Add Product", command=self.add_product)
        self.add_button.pack(side="left", padx=10)
        
        self.edit_button = tk.Button(self, text="Edit Product", command=self.edit_product)
        self.edit_button.pack(side="left", padx=10)
        
        self.view_button = tk.Button(self, text="View Product", command=self.view_product)
        self.view_button.pack(side="left", padx=10)
        
        self.delete_button = tk.Button(self, text="Delete Product", command=self.delete_product)
        self.delete_button.pack(side="left", padx=10)
        
        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack(side="left", padx=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_app)
        self.quit_button.pack(side="left", padx=10)

    def update_inventory_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for product in self.products:
            product_id = product["id"] + 1
            self.tree.insert("", "end", values=(product_id, product["name"], product["desc"], locale.currency(product["price"], grouping=True), product["quantity"]))

    def sort_treeview(self, col, is_numeric):
        if self.sort_by == col:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_by = col
            self.sort_asc = True

        if is_numeric:
            self.products.sort(key=lambda x: float(x[col.lower()]), reverse=not self.sort_asc)
        else:
            self.products.sort(key=lambda x: x[col.lower()], reverse=not self.sort_asc)
        
        self.update_inventory_view()

    def add_product(self):
        AddProductWindow(self)

    def edit_product(self):
        EditProductWindow(self)

    def view_product(self):
        ViewProductWindow(self)

    def delete_product(self):
        DeleteProductWindow(self)

    def save_data(self):
        save_data('db_products.csv', self.products)
        messagebox.showinfo("Save Data", "Data successfully saved!")

    def quit_app(self):
        save_data('db_products.csv', self.products)
        self.destroy()

class AddProductWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Product")
        self.geometry("400x300")
        self.parent = parent

        tk.Label(self, text="Name").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Description").grid(row=1, column=0, padx=10, pady=10)
        self.desc_entry = tk.Entry(self)
        self.desc_entry.grid(row=1, column=1)

        tk.Label(self, text="Price").grid(row=2, column=0, padx=10, pady=10)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=2, column=1)

        tk.Label(self, text="Quantity").grid(row=3, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=3, column=1)

        tk.Button(self, text="Add", command=self.add_product).grid(row=4, column=0, columnspan=2, pady=10)

    def add_product(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        add_product(self.parent.products, name, desc, price, quantity)
        self.parent.update_inventory_view()
        self.destroy()

class EditProductWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Edit Product")
        self.geometry("400x300")
        self.parent = parent

        tk.Label(self, text="Enter Product ID").grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=0, column=1)

        tk.Label(self, text="New Name").grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self, text="New Description").grid(row=2, column=0, padx=10, pady=10)
        self.desc_entry = tk.Entry(self)
        self.desc_entry.grid(row=2, column=1)

        tk.Label(self, text="New Price").grid(row=3, column=0, padx=10, pady=10)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=3, column=1)

        tk.Label(self, text="New Quantity").grid(row=4, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=4, column=1)

        tk.Button(self, text="Edit", command=self.edit_product).grid(row=5, column=0, columnspan=2, pady=10)

    def edit_product(self):
        product_id = int(self.id_entry.get()) - 1
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        
        for product in self.parent.products:
            if product["id"] == product_id:
                change_product(product, name, desc, price, quantity)
                self.parent.update_inventory_view()
                self.destroy()
                return
        messagebox.showerror("Error", "Product not found!")

class ViewProductWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("View Product")
        self.geometry("400x200")
        self.parent = parent

        tk.Label(self, text="Enter Product ID").grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=0, column=1)

        self.view_button = tk.Button(self, text="View", command=self.view_product)
        self.view_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.product_label = tk.Label(self, text="", wraplength=300)
        self.product_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def view_product(self):
        product_id = int(self.id_entry.get()) - 1
        result = view_product(self.parent.products, product_id)
        self.product_label.config(text=result)

class DeleteProductWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Delete Product")
        self.geometry("400x200")
        self.parent = parent

        tk.Label(self, text="Enter Product ID").grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=0, column=1)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_product)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def delete_product(self):
        product_id = int(self.id_entry.get()) - 1
        result = remove_product(self.parent.products, product_id)
        self.parent.update_inventory_view()
        messagebox.showinfo("Delete Product", result)
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()