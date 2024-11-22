import csv
import os
import locale
from time import sleep

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
            
            products.append(        #list
                {                    #dictionary
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

def save_data(filepath, products):

        # Write the products data to a CSV file
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  # Write the header row
        writer.writerows(products)  # Write the product data

    print(f"Data successfully saved to {filepath}")
    
def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
        input()
    else:
        return f"Product with id {id} not found"
        input()

def view_inventory(products):
    # skapa sidhuvudet av tabellen:
    header = f"{'#':<6} {'NAMN':<36} {'BESKRIVNING':<71} {'PRIS':<15} {'KVANTITET':<11}"
    separator = "-" * 140           #linje
    
    # rader för varje produkt:
    rows = []

    for index, product in enumerate(products, 1):
        name = product['name']
        desc = product['desc']
        price = product['price']
        quantity = product['quantity']
        
        price = locale.currency(price, grouping=True)
        row = f"{index:<5} {name:<35} {desc:<70} {price:<22} {quantity:<10}"

        rows.append(row)
    
    # kombinera sidhuvud och rader:
    inventory_table = "\n".join([header, separator] + rows)
    
    return f"{inventory_table}"

def view_product(products, id):
    # Go through each product in the list
    for product in products:
        # Check if the product's id matches the given id
        if product["id"] == id:
            # If it matches, return the product's name and description
            return f"Visar produkt: {product['name']} {product['desc']}"
    
    # If no matching product is found, return this message
    return "Produkten hittas inte"

def view_products(products):
    product_list = []
    for index, product in enumerate(products,1 ):
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

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('db_products.csv')
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_inventory(products))  # Show ordered list of products
        save_data('db_products.csv', products)

        choice = input("Vill du (L)ägg till produkt, (Ä)ndra produkt, (V)isa, (T)a bort en produkt, (S)para Eller (Q)uita och spara?").strip().upper()

        if choice == "L":
            name = input("namn på produkt: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Antal: "))

            print(add_product(products, name, desc, price, quantity))

        elif choice == "S":
            print("Sparrar...")
            print(save_data('db_products.csv',products))

        elif choice == "Q":
            print("Sparrar...")
            print(save_data('db_products.csv', products))
            break

        elif choice in ["V", "T", "Ä"]:
            index = int(input("Enter product ID: "))
            
            if choice == "V":   #visa
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product
                    print(view_product(products, id))  # view product using the actual ID
                    done = input()
                    
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

            elif choice == "T": #ta bort
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product

                    print(remove_product(products, id))  # Remove product using the actual ID
                    sleep(0.5)            

                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

            elif choice == "Ä":
                if 1 <= index <= len(products):  
                    product = products[index - 1] 
                    id = product['id']

                    print(f"Ändra produkt med ID: {id}")

                    name = input("Ändra namn: ")
                    desc = input("Ändra beskrivning: ")
                    price = float(input("Ändra pris: "))
                    quantity = int(input("Ändra kvantität: "))
                    print(change_product(product, name, desc, price, quantity,))
                    done = input()
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

        
    except ValueError:
        print("fel data typ")
        sleep(0.5)
