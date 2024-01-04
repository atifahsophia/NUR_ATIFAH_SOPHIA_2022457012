import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Connect to your MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="food_order"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Example SQL query
sql_query = "SELECT * FROM `order`"

# Execute the SQL query
mycursor.execute(sql_query)

# Fetch the result
result = mycursor.fetchall()

# Function to handle the calculation and database saving
def collect_data():
    name = name_entry.get()
    phone_no = int(phone_no_entry.get())
    address = address_entry.get()
    food_set = food_var.get()
    food_pack = int(food_pack_entry.get())
    drinks = drinks_var.get()
    drinks_pack = int(drinks_pack_entry.get())
    
    # Prices for the selections
    prices_dish = {
        "Set A": 6,
        "Set B": 7,
        "Set C": 8,
    }
        
    prices_drinks = {
        "Orange juice": 3,
        "Ice chocolate": 2,
        "Sky juice": 1
    }
  
    # Clear entry widgets after calculation
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_no_entry.delete(0, tk.END)
    food_pack_entry.delete(0, tk.END)
    drinks_pack_entry.delete(0, tk.END)

    # Calculate the total price
    total_price = int(prices_dish[food_set] * food_pack + prices_drinks[drinks] * drinks_pack)

    # Insert data into the database
    sql = "INSERT INTO `order` (name, phone_no, address, food_set, food_pack, drinks, drinks_pack) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (name, phone_no, address, food_set, food_pack, drinks, drinks_pack)
    mycursor.execute(sql, val)
    mydb.commit()

    # Update the output label
    output_label.config(text=f"Set: {food_set}, Packs: {food_pack}, Drinks: {drinks}, Packs: {drinks_pack}, Total Price: RM{total_price}", fg="blue")

# Main window
window = tk.Tk()
window.title("Food Order")

frame = tk.Frame(window)
frame.grid(row=0, column=0)

# Add widgets to the main window
label = tk.Label(frame, text="Fill the information")
label.grid(row=0, column=0, padx=10, pady=10)

user_info_frame = tk.LabelFrame(frame, text="Customer Information")
user_info_frame.grid(row=1, column=0, padx=20, pady=10)

name_label = tk.Label(user_info_frame, text="Name")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(user_info_frame)
name_entry.grid(row=0, column=1, padx= 10, pady= 10)

address_label = tk.Label(user_info_frame, text="Address")
address_label.grid(row=1, column=0)
address_entry = tk.Entry(user_info_frame)
address_entry.grid(row=1, column=1, padx= 10, pady= 20)

phone_no_label = tk.Label(user_info_frame, text="Phone Number (01XXXXXX)")
phone_no_label.grid(row=2, column=0)

def is_numeric(value):
    try:
        integer_value = int(value)
        return True
    except ValueError:
        return False

def validate_phone_number(value):
    if is_numeric(value) or value == "":
        return True
    else:
        messagebox.showerror("Error", "Phone number must be numeric")
        return False

phone_no_entry = tk.Entry(user_info_frame, validate="key", validatecommand=(validate_phone_number, "%P"))
phone_no_entry.grid(row=2, column=1)

second_window = tk.Toplevel(window)
second_window.title("Order detail")

# Button to open the second window
second_window_button = tk.Button(frame, text="Go to Order Details", command= second_window)
second_window_button.grid(row=3, column=0, pady=10) 

# Order details display
order_detail_label = tk.Label(second_window, text="Order Details:")
order_detail_label.grid()

# The defined list by using pricebox
prices_text = tk.Text(second_window, height=15, width=45)
prices_text.grid(pady=20) 
prices_text.insert(tk.END, "Rice & Prices:\n\n")
prices_text.insert(tk.END, "Set A: Rice, Fried chicken, Vegetables  \nPrice: RM6\n\n")
prices_text.insert(tk.END, "Set B: Rice, Squid dish, Vegetables \nPrice: RM7\n\n")
prices_text.insert(tk.END, "Set C: Rice, Prawn dish, Vegetables \nPrice: RM8\n\n")
prices_text.configure(state='disabled')

# Trip Type Dropdown
food_var = tk.StringVar(second_window)
food_var.set("Select Your Set")
trip_dropdown = tk.OptionMenu(second_window, food_var, "Set A", "Set B", "Set C")
trip_dropdown.grid(pady=10)

# Packs Entry. Label and user can insert data thru entry
label = tk.Label(second_window, text="Packs:")
label.grid()
food_pack_entry = tk.Entry(second_window)
food_pack_entry.grid()

# Drinks type
drinks_var = tk.StringVar(second_window)
drinks_var.set("Select Your Drinks")
trip_dropdown = tk.OptionMenu(second_window, drinks_var, "Orange juice", "Ice chocolate", "Sky juice")
trip_dropdown.grid(pady=10)

# Packs Entry. Label and user can insert data thru entry
label_2 = tk.Label(second_window, text="Packs:")
label_2.grid()
drinks_pack_entry = tk.Entry(second_window)
drinks_pack_entry.grid()

# Calculate button in the second window
calculate_button = tk.Button(second_window, text="Calculate", command=collect_data)
calculate_button.grid(pady=10)
    
# Output Label & result
label = tk.Label(second_window)
label.grid(ipadx=10, ipady=10)
output_label = tk.Label(second_window, text="")
output_label.grid() 

window.mainloop()

# Close the database connection
mydb.close() 