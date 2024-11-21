import tkinter as tk
from tkinter import *
from tkinter import messagebox 
import csv  
from datetime import datetime
import os
#Added github change 

#File Path to CSV file
file_inventory = r"Inventory.csv"

# Login Functions
def login_validation(u,p):
    return u == "Imtiaz" and p == "123"
    
def try_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if login_validation(username, password):
        # If login is successful, close login window and show main window
        login_window.destroy()
        root.deiconify()  # Show the main application window
    else:
        # Show an error message
        messagebox.showerror("Login Failed", "Invalid username or password")

# Here I want to create a function that evaluates the price of a menu item by finding it in a hashmap 
# that maps the items to their corresponding prices
def Charge(item):
    Prices = {"SFC":6.95 ,"RFC":7.95,"LFC":8.95, 
    "SF":4.50,"RF":5.50,"LF":6.50,
    "CC":2.00,"TC":2.50,"RC":3.20,"LC":3.80,"CC":4.95,"S":0.60,"CHB":2.70,
    "SKP":3.65,"CMP":3.65,"BOP":3.65,"JS":1.90,"BS":1.95,
    "FC":1.70,"SCP7":3.95,"SCP10":4.95,
    "CN5":2.50,"CN10":4.80,"CB5":2.80,"CB10":5.50,"CCF3":2.95,"CCF5":4.50,"SFC":3.95,
    "CSB":2.95,"BB":2.95,"ZB":3.95,"CFB":3.95,"PBB":4.95,"BBP":1.95,"MAM":2.50,
    "PE":0.95,"PO":0.75,"PG":0.75,
    "SS":0.85,"LS":1.30,
    "DK":1.25
    }
    return Prices.get(item,0)

inventory = {"Potatoes":50,"Fish": 15,"Fish Cake":25,"Sampi":50,"S&K Pie" : 10,"C&M Pie": 10,"B&O Pie":10,"Sausage":25,
             "Rolls":20,"CS Patty":10,"B Patty":10,"Z Patty":10,"Chn Fillet":10,"PB Patty": 10,"Ckn Ng" : 30,"Chn Bts": 50,
             "Ckn Flts":20,"S/F Ckn": 100,"Pck Egg" : 30,"Pck Onion": 30,"Pck Gherkin":30,"Cans" : 48,"Sauce": 50
             }



#Assign weights to each item - ADD to csv file instead 
def deduct_item(item):
    ingredient_use = {
    "Cod Bites&Chips":{"Fish":0.5,"Potatoes": 0.25},"Regular Fish&Chips":{"Fish":1,"Potatoes": 0.5},
    "Large Fish&Chips":{"Fish":1.5,"Potatoes": 0.5},

    "Cod Bites":{"Fish":0.5},"Regular Fish":{"Fish":1},"Large Fish":{"Fish":1.5},"Fish Cake":{"Fish Cake":1},
    "Scampi 7pcs":{"Scampi":7},"Scampi 10pcs":{"Scampi":10},

    "Cone of Chips":{"Potatoes":0.1},"Tray of Chips":{"Potatoes":0.2},"Regular Chips":{"Potatoes":0.25},
    "Large Chips":{"Potatoes":0.5},"Cheesy Chips":{"Potatoes":0.25,"Cheese":0.2},
    "Battered Scallop":{"Potatoes":0.1},"Chip Butty":{"Potatoes":0.1,"Roll":1},

    "Steak&Kidney":{"S&K Pie":1},"Chicken&Mushroom":{"C&M Pie":1},"Beef&Onion":{"B&O Pie":1},

    "Jumbo Sausage":{"Sausage":1},"Battered Sausage":{"Sausage":1},"5 Chicken Nuggets":{"Ckn Ng":5},"10 Chicken Nuggets":{"Ckn Ng":10},
    "5 Chicken Bites":{"Chn Bts":5},"10 Chicken Bites":{"Chn Bts":10},"3 Chicken Fillets":{"Ckn Flts":3},"5 Chicken Fillets":{"Ckn Flts":5},
    "25 S/F Chicken":{"S/F Ckn": 25},

    "Chicken Steak Burger":{ "CS Patty":1,"Roll":1},"Beef Burger":{ "B Patty":1,"Roll":1},"Zinger Burger":{ "Z Patty":1,"Roll":1},
    "Chicken Fillet Burger":{ "Ckn Flts":1,"Roll":1},"Premium Beef Burger":{"PB Patty": 1,"Roll":1},"Battered Burger Patty":{ "Ckn Flts":1,"Roll":1},
    "Make it a Meal":{"Potatoes":0.2,"Cans":1},

    "Pickled Egg":{"Pck Egg" : 1},"Pickled Onion":{"Pck Onion" : 1},"Pickled Gherkin":{"Pck Gherkin" : 1},
    "Small Sauce":{"Sauce":5},"Large Sauce":{"Sauce":10}
    }
    return ingredient_use.get(item)

def read_inventory():
    #Reads inventory from the CSV file and returns it as a dictionary
    inventory = {}
    with open(file_inventory, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            item, quantity = row
            inventory[item] = float(quantity)  # Assuming quantities might not be whole numbers
    return inventory

def write_inventory(inventory):
    #Writes the updated inventory back to the CSV file
    with open(file_inventory, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Quantity"])  # Write the header
        for item, quantity in inventory.items():
            writer.writerow([item, quantity])

# Function to remove items from the inventory once an order is complete
# 2 reg f&c current_order looks like this ['RFC', 'Regular Fish&Chips', 'RFC', 'Regular Fish&Chips']
# 1. Identify individual items
# 2. Map them to their associated weights
# 3. Deduct the weight from the inventory
def update_inventory():
    global current_order
    items = current_order[1::2]
    inventory = read_inventory()
    for item in items:
        # For each item find it's associated weighting
        ingredients = deduct_item(item)
        # If the item was found
        if ingredients:
            # iterate over dictionary of items and weights in order
            for ingredient,quantity in ingredients.items():
                if ingredient in inventory:
                    # Update the quantity for the ingredient in the inventory
                    if inventory[ingredient] >= quantity:
                        inventory[ingredient] -=quantity
                    else:
                        print(f"Insufficient stock for {ingredient}")
                else:
                    print(f"{ingredient}not found in inventory")
    write_inventory(inventory)  # Write the updated inventory back to CSV
    print("Updated Inventory:", inventory)

def restock_inventory(item, amount):
    if item in inventory:
        inventory[item] += amount
    else:
        print(f"{item} not found in inventory. Check item name.")


def add_to_total(item,name):
    global total
    global current_order
    current_order.append(item)
    price =Charge(item)
    total += price
    total_var.set(f"{total:.2f}")  # Update the displayed total
    current_order.append(name) # Add item to current order list
    order.insert(END,f"{name}\n") # Add item to order list

def cashback(cash):
    change = cash - total
    change = round(change,2)
    cashback_var.set(change)

# Function to calculate cashback based on manual entry in the payment box
def calculate_cashback():
    try:
        cash = float(payment_var.get())  # Convert the entry to a float
        cashback(cash)  # Use the existing cashback function
    except ValueError:
        cashback_var.set("Invalid input")  # Display error if entry isn't a valid number

# Function to save current order as a csv file
def save_order_to_csv():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = r"daily_orders.csv"
    with open(file_path,mode="a",newline="")as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, ",".join(current_order),f"{total:2f}"])

#Function to clear fileds for a new order and save order to the CSV
def complete_order():
    update_inventory()
    save_order_to_csv()
    clear_all()
    
    

# function to clear all fields
def clear_all():
    global total
    total = 0
    total_var.set("0.00")
    cashback_var.set("0.00")
    payment_var.set("")
    order.delete("1.0",END)

# Fuction to cancel the last item on the order
def cancel_item():
    global total
    global current_order
    # Find last item in order
    if current_order:
        item = current_order[-2]
        # Evaluate price of item
        price = Charge(item)
        # update total accordingly
        total = total - price
        #remove item from list
        current_order.pop()
        current_order.pop()
        # update total display
        total_var.set(f"{total:.2f}")

        # Update the Text Widget
        #Get number of lines in text widget
        last_index = order.index("end-1c").split(".")[0] # Get line number of last item
        #order.index("end-1c") -retrieves index of last character (end-1c gives last chr position, so we split it 
        # to get the last line number)

        start_index = f"{int(last_index) - 1}.0" # beginning of last line
        end_index = f"{last_index}.0" # beginning of last empty line
        order.delete(start_index,end_index)
    
    else:
        print("Order is empty so there are no items to remove")

# Calculate Total Sales 
def total_sales():
    total_sales = 0.00
    today = datetime.now().strftime("%Y-%m-%d") #Today's date 
    file_path = os.path.join("daily_orders.csv") 

    try:
        with open(file_path,mode="r",newline="")as file:
            # Create a Reader object
            reader = csv.reader(file)
            next(reader)
            # iterate through each row
            for row in reader:
                # Extract the third row (the one that contains the price of the order) ensuring it isn't empty
                if row and len(row) >=3:
                    timestamp = row[0]
                    date =timestamp.split(" ")[0]

                    if date == today:
                        total_sales += float(row[2]) # convert the price of the order to a float and add to the running total

        print(f"Total sales for today: £{total_sales:.2f}")
    except Exception as e:
        print(f"An error occurred while reading the csv  file{e}")


total = 0
current_order = []


root = Tk() # Create the root widget
root.title("Wellington Fryer EPOS") # Add title to window
root.configure(background="white") # change background to black
root.minsize(1000,500)
root.geometry("300x300+100+100") # Set starting size and location of window



# Set Meals
set_meals = Label(root,text="Set Meals")
set_meals.grid(row=0,column=0)
SFC = tk.Button(root,text="Cod Bites&Chips",width = 15,command=lambda: add_to_total("SFC","Cod Bites&Chips"))
SFC.grid(row =1, column = 0)
RFC = tk.Button(root,text="Regular Fish&Chips",width = 15,command=lambda: add_to_total("RFC","Regular Fish&Chips"))
RFC.grid(row =2, column = 0)
LFC = tk.Button(root,text="Large Fish&Chips",width = 15,command=lambda: add_to_total("LFC","Large Fish&Chips"))
LFC.grid(row =3, column = 0)

# Fish
Fish = Label(root,text="Fish")
Fish.grid(row=0,column=1)
SF = tk.Button(root,text="Cod Bites",width = 15,command=lambda: add_to_total("SF","Cod Bites"))
SF.grid(row =1, column = 1)
RF = tk.Button(root,text="Regular Fish",width = 15,command=lambda: add_to_total("RF","Regular Fish"))
RF.grid(row =2, column = 1)
LF = tk.Button(root,text="Large Fish",width = 15,command=lambda: add_to_total("LF","Large Fish"))
LF.grid(row =3, column = 1)
FC = tk.Button(root,text="Fish Cake",width = 15,command=lambda: add_to_total("FC","Fish Cake"))
FC.grid(row =5, column = 1)
SCP = tk.Button(root,text="Scampi 7pcs",width = 15,command=lambda: add_to_total("SCP7","Scampi 7pcs"))
SCP.grid(row =6, column = 1)
SCP10 = tk.Button(root,text="Scampi 10pcs",width = 15,command=lambda: add_to_total("SCP10","Scampi 10pcs"))
SCP10.grid(row =7, column = 1)

# Chips
Chips= Label(root,text="Chips")
Chips.grid(row=0,column=2)
COC = tk.Button(root,text="Cone of Chips",width = 15,command=lambda: add_to_total("COC","Cone of Chips"))
COC.grid(row =1, column = 2)
TC = tk.Button(root,text="Tray of Chips",width = 15,command=lambda: add_to_total("TC","Tray of Chips"))
TC.grid(row =2, column = 2)
RC = tk.Button(root,text="Regular Chips",width = 15,command=lambda: add_to_total("RC","Regular Chips"))
RC.grid(row =3, column = 2)
LC = tk.Button(root,text="Large Chips",width = 15,command=lambda: add_to_total("LC","Large Chips"))
LC.grid(row =5, column = 2)
CC = tk.Button(root,text="Cheesy Chips",width = 15,command=lambda: add_to_total("CC","Cheesy Chips"))
CC.grid(row =6, column = 2)
S = tk.Button(root, text="Battered Scallop",width=15, command=lambda: add_to_total("S","Battered Scallop"))
S.grid(row=7,column=2)
CHB = tk.Button(root, text="Chip Butty",width=15, command=lambda: add_to_total("CHB","Chip Butty"))
CHB.grid(row=8,column=2)

# Pies & Sausages
PiesS = Label(root,text="Pies & Sausages")
PiesS.grid(row=4,column=0)
SKP = tk.Button(root,text="Steak&Kidney",width = 15,command=lambda: add_to_total("SKP","Steak&Kidney"))
SKP.grid(row =5, column = 0)
CMP = tk.Button(root,text="Chicken&Mushroom",width = 15,command=lambda: add_to_total("CMP","Chicken&Mushroom"))
CMP.grid(row =6, column = 0)
BOP = tk.Button(root,text="Beef&Onion",width = 15,command=lambda: add_to_total("BOP","Beef&Onion"))
BOP.grid(row =7, column = 0)
JS = tk.Button(root,text="Jumbo Sausage",width=15, command=lambda:add_to_total("JS","Jumbo Sausage"))
JS.grid(row=8,column=0)
BS = tk.Button(root,text="Battered Sausage",width=15, command=lambda:add_to_total("BS","Battered Sausage"))
BS.grid(row=9,column=0)


#Chicken 
Chicken = Label(root,text="Chicken")
Chicken.grid(row=0,column=3)
CN5 = tk.Button(root,text="5 Chicken Nuggets",width = 15,command=lambda:add_to_total("CN5","5 Chicken Nuggets"))
CN5.grid(row=1,column=3)
CN10 = tk.Button(root,text="10 Chicken Nuggets",width = 15,command=lambda:add_to_total("CN10","10 Chicken Nuggets"))
CN10.grid(row=2,column=3)
CB5 = tk.Button(root,text="5 Chicken Bites",width = 15,command=lambda:add_to_total("CB5","5 Chicken Bites"))
CB5.grid(row=3,column=3)
CB10 = tk.Button(root,text="10 Chicken Bites",width = 15,command=lambda:add_to_total("CB10","10 Chicken Bites"))
CB10.grid(row=5,column=3)
CCF3 = tk.Button(root,text="3 Chicken Fillets",width = 15,command=lambda:add_to_total("CCF3","3 Chicken Fillets"))
CCF3.grid(row=6,column=3)
CCF5 = tk.Button(root,text="5 Chicken Fillets",width = 15,command=lambda:add_to_total("CCF5","5 Chicken Fillets"))
CCF5.grid(row=7,column=3)
SFC = tk.Button(root,text="25 S/F Chicken",width = 15,command=lambda:add_to_total("SFC","25 S/F Chicken"))
SFC.grid(row=8,column=3)

#Burgers
Burgers = Label(root,text="Burgers")
Burgers.grid(row=0,column=4)
CSB = tk.Button(root,text="Chicken Steak Burger",width=15,command=lambda:add_to_total("CSB","Chicken Steak Burger"))
CSB.grid(row=1,column=4)
BB=tk.Button(root,text="Beef Burger",width=15,command=lambda:add_to_total("BB","Beef Burger"))
BB.grid(row=2,column=4)
ZB=tk.Button(root,text="Zinger Burger",width=15,command=lambda:add_to_total("ZB","Zinger Burger"))
ZB.grid(row=3,column=4)
CFB = tk.Button(root,text="Chicken Fillet Burger",width=15,command=lambda:add_to_total("CFB","Chicken Fillet Burger"))
CFB.grid(row=5,column=4)
PBB = tk.Button(root,text="Premium Beef Burger",width=15,command=lambda:add_to_total("PBB","Premium Beef Burger"))
PBB.grid(row=6,column=4)
BBP = tk.Button(root,text="Battered Burger Patty",width=15,command=lambda:add_to_total("BBP","Battered Burger Patty"))
BBP.grid(row=7 ,column=4) 
MAM = tk.Button(root,text="Make it a Meal",width=15,command=lambda:add_to_total("MAM","Make it a Meal"))
MAM.grid(row=8,column=4)

# Pickles
Pickles = Label(root,text="Pickles")
Pickles.grid(row=0,column=5)
PE = tk.Button(root,text="Pickled Egg",width=15, command=lambda: add_to_total("PE","Pickled Egg"))
PE.grid(row=1,column=5)
PO = tk.Button(root,text="Pickled Onion",width=15, command=lambda: add_to_total("PO","Pickled Onion"))
PO.grid(row=2,column=5)
PG = tk.Button(root,text="Pickled Gherkin",width=15,command=lambda:add_to_total("PG","Pickled Gherkin"))
PG.grid(row=3,column=5)

# Sauces
Sauces = Label(root,text="Sauces")
Sauces.grid(row=4,column=5)
SS = tk.Button(root,text="Small Sauce",width=15,command=lambda:add_to_total("SS","Small Sauce"))
SS.grid(row=5,column=5)
LS=tk.Button(root,text="Large Sauce",width=15,command=lambda:add_to_total("LS","Large Sauce"))
LS.grid(row=6,column=5)

# Drinks
Drinks = Label(root,text="Drinks")
Drinks.grid(row=7,column=5)
Cans = tk.Button(root,text="Cans",width=15, command=lambda:add_to_total("DK","Can"))
Cans.grid(row=8,column=5)



# Total Display
ltotal =Label(root, text = "Total")
ltotal.grid(row=10, column=0)
# Use StringVar to dynamically update the tool value 
total_var = StringVar()
total_var.set(f"{total:.2f}")  # Set initial total as 0.00
Total = Entry(root, textvariable=total_var, state='readonly')  # Make the entry readonly
Total.grid(row=10, column=1)

# Order list display 
lorder = Label(root,text="Order List")
lorder.grid(row=0,column=6)
order = Text(root,width=30,height=20,state="normal")
order.grid(row=1,column=6, rowspan=10)

# Payment Entry -To enter cash given (when it isn't a single note)
lpayment = Label(root,text="Payment")
lpayment.grid(row=11,column=0)
payment_var = StringVar()
Payment = Entry(root,textvariable=payment_var)
Payment.grid(row=11,column=1)

# Button to calculate cashback based on custom payment entry
calculate_button = Button(root, text="Calculate", command=calculate_cashback)
calculate_button.grid(row=11, column=2)

# Cashback Display
lcashback = Label(root,text="Cashback")
lcashback.grid(row=12,column=0)
cashback_var = DoubleVar()
cashback_var.set(0.00)
Cashback = Entry(root, textvariable=cashback_var,state='readonly')
Cashback.grid(row=12,column=1)

# Cash Notes Buttons
Twenty = tk.Button(root,text="£20",width = 5,command= lambda: cashback(20) )
Twenty.grid(row =11, column = 3)
Ten = tk.Button(root,text="£10",width = 5,command= lambda:cashback(10) )
Ten.grid(row =11, column = 4)
Five = tk.Button(root,text="£5",width = 5,command= lambda: cashback(5) )
Five.grid(row =11, column = 5)

# Button to clear all fields so the next order can be taken without having to rerun the program
complete = tk.Button(root,text="Complete Order",width=15,command=complete_order)
complete.grid(row=13,column=1)

#Button to cancel an order
cancel_order = tk.Button(root,text="Cancel Order",width=10,command=clear_all)
cancel_order.grid(row=13, column=4)

# Button to cancel last item in the order 
item_cancel  = tk.Button(root,text="Cancel Item",width=10,command= cancel_item)
item_cancel.grid(row=13,column=3)

# Button to calculate the total sales made during the day
sales = tk.Button(root,text="Total Sales",command=total_sales)
sales.grid(row=14, column=1)

root.withdraw() # Hides the EPOS until the user logs in 

# Login Window
login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("300x300")
login_window.grab_set()  # Focus on login window, blocking interactions with main window

tk.Label(login_window,text="Username:").pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:").pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=try_login)
login_button.pack(pady=10)

root.mainloop()


