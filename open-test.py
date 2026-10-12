import csv
import subprocess
import locale
import os


def truncate(text, amount):
    if len(text) > amount-3:
        return text[:amount-3] + "..."
    else:
        return text

def save_product(products):

    csv_file_path = "db_products.csv"

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  # Write the header row
        writer.writerows(products)  # Write the product data

    print(f"Data successfully saved to {csv_file_path}")



def format_currency(value):
    return locale.currency(value, grouping=True)


def list_products(products):
    try:
        for idx, product in enumerate(products, start=1):
            name = truncate(product['name'], 24)
            desc = truncate(product['desc'], 42)
            price = truncate(format_currency(product['price']), 15)
            quantity = product['quantity']

            print(f"{idx:<5} {name:<24} {desc:<42} {price:>15}     {quantity:<5}")
    except:
        print("Kunde inte öppna pdocuts.")


def view_product(idx, products):
    subprocess.run('cls', shell=True)
    product = products[idx - 1]
    print(f"ID: {product['id']}")
    print(f"Namn: {product['name']}")
    print(f"Beskrivning: {product['desc']}")
    print(f"Pris: {format_currency(product['price'])}")
    print(f"Antal: {product['quantity']}")


def get_product_by_id(id, products):
    for product in products:
        if product['id'] == id:
            return product
    return None


def add_product(products):
    if products:
        max_id = max(product['id'] for product in products)
        new_id = max_id + 1
    else:
        new_id = 1

    name = input("Namn: ")
    desc = input("Beskrivning: ")
    price = float(input("Pris: "))
    quantity = int(input("Antal: "))

    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }
    products.append(new_product)


def remove_product(id, products):
    for i, product in enumerate(products):
        if product['id'] == id - 1:
            return products.pop(i)
    return None


def load_data(filename): 
    products = []           #lista
    try: 
        with open(filename, 'r') as file:       #öppnar en fil med read-rättighet
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
    except:
        print(f"{filename} kunde inte öppnas")
            
    return products


    # found_max = max(products, key=lambda id: id['id'])
    # max_id = found_max['id']
    # new_id = max_id + 1

try:  
   locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  # Av någon anledning funkade inte sv_SE.UTF-8 för mig, jag fick error
except: 
   locale.setlocale(locale.LC_ALL, 'Swedish_Sweden.1252')

subprocess.run('cls', shell=True)

products = load_data('db_products.csv')


while True:
    list_products(products)
    
    print("-" * 100)
    option = input("Vad vill du göra? [# = visa produkt | L = lägg till | T = ta bort | E = ändra | Q = avsluta och spara] ").strip().upper()
    
    if option.isdigit():
        idx = int(option)
        
        if 0 < idx <= len(products):   
            view_product(idx, products)
            input() #bara vänta till tangentbordsklick
    elif option == 'L':
        add_product(products)
    elif option == 'T':
        prod_id = int(input("Ange ID för produkten som ska tas bort: "))
        remove_product(prod_id, products)
    elif option == 'Q':
        save_product(products)
        break
