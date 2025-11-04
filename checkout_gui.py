import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Load item price data
with open("item_database.json", "r") as f:
    item_prices = json.load(f)

# Load shared cart if exists
if os.path.exists("cart_data.json"):
    with open("cart_data.json", "r") as f:
        cart = json.load(f)
else:
    cart = {}

# Functions
def refresh_cart():
    tree.delete(*tree.get_children())
    total = 0
    for idx, (item, qty) in enumerate(cart.items(), start=1):
        unit_price = item_prices.get(item, 0)
        price = unit_price * qty
        total += price
        tree.insert("", "end", values=(idx, item, qty, f"₹{unit_price}", f"₹{price}"))
    update_summary(total)

def update_summary(subtotal):
    sgst = round(subtotal * 0.09, 2)
    cgst = round(subtotal * 0.09, 2)
    bag_cost = 5
    total = round(subtotal + sgst + cgst + bag_cost, 2)
    summary_var.set(
        f"Subtotal: ₹{subtotal}    SGST: ₹{sgst}    CGST: ₹{cgst}    Bag: ₹{bag_cost}    Total: ₹{total}"
    )

def add_item():
    item = item_entry.get().strip().lower()
    if item not in item_prices:
        messagebox.showerror("Item Error", f"'{item}' not found in database!")
        return
    qty = int(qty_spinbox.get())
    cart[item] = cart.get(item, 0) + qty
    refresh_cart()

def remove_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Item", "Please select an item to remove.")
        return
    for sel in selected:
        item_name = tree.item(sel)["values"][1]
        if item_name in cart:
            del cart[item_name]
    refresh_cart()

def update_quantity():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Item", "Please select an item to update.")
        return
    new_qty = int(qty_spinbox.get())
    for sel in selected:
        item_name = tree.item(sel)["values"][1]
        cart[item_name] = new_qty
    refresh_cart()

def clear_cart():
    cart.clear()
    refresh_cart()

# GUI Setup
root = tk.Tk()
root.title("🛍️ Queue-Free Checkout GUI")
root.geometry("820x520")
root.config(bg="#f4f4f4")  # Light grey background

# Style
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#333")
style.configure("Treeview", background="#ffffff", foreground="#333", rowheight=30, font=("Arial", 11))
style.map('Treeview', background=[('selected', '#b3e5fc')])

# Title
title_label = tk.Label(root, text="🛒 Queue-Free Checkout System", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#2e7d32")
title_label.pack(pady=10)

# Treeview Table
frame = tk.Frame(root, bg="#f4f4f4")
frame.pack()
tree = ttk.Treeview(frame, columns=("S.No", "Item", "Qty", "Unit Price", "Total"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.column("S.No", width=50, anchor="center")
tree.column("Item", width=200, anchor="center")
tree.column("Qty", width=80, anchor="center")
tree.column("Unit Price", width=100, anchor="center")
tree.column("Total", width=100, anchor="center")
tree.pack(pady=10)

# Summary Label
summary_var = tk.StringVar()
summary_label = tk.Label(root, textvariable=summary_var, font=("Arial", 12), bg="#f4f4f4", fg="#333")
summary_label.pack()

# Payment Mode
payment_frame = tk.Frame(root, bg="#f4f4f4")
payment_frame.pack(pady=10)

tk.Label(payment_frame, text="Payment Mode:", bg="#f4f4f4", font=("Arial", 11)).grid(row=0, column=0, padx=5)
payment_mode = tk.StringVar()
payment_mode.set("Cash")  # Default

payment_dropdown = ttk.Combobox(payment_frame, textvariable=payment_mode, values=["Cash", "Card", "UPI"], state="readonly")
payment_dropdown.grid(row=0, column=1, padx=5)

def confirm_payment():
    messagebox.showinfo("Payment Confirmed", f"Payment received via {payment_mode.get()}.\nThank you!")
    thank_you_label = tk.Label(root, text="🧡 Thank You for Shopping with Us!", font=("Arial", 14, "bold"), fg="#ff6f00", bg="#f4f4f4")
    thank_you_label.pack(pady=20)
    
    # Delete cart_data.json to reset for next user
    if os.path.exists("cart_data.json"):
        os.remove("cart_data.json")

# Confirm button
pay_btn = tk.Button(payment_frame, text="Confirm Payment", command=confirm_payment, bg="#4caf50", fg="white", font=("Arial", 11, "bold"))
pay_btn.grid(row=0, column=2, padx=10)

# Control Buttons
ctrl_frame = tk.Frame(root, bg="#f4f4f4")
ctrl_frame.pack(pady=10)

tk.Label(ctrl_frame, text="Item:", bg="#f4f4f4", font=("Arial", 11)).grid(row=0, column=0, padx=5)
item_entry = tk.Entry(ctrl_frame, width=20)
item_entry.grid(row=0, column=1, padx=5)

tk.Label(ctrl_frame, text="Qty:", bg="#f4f4f4", font=("Arial", 11)).grid(row=0, column=2, padx=5)
qty_spinbox = tk.Spinbox(ctrl_frame, from_=1, to=99, width=5)
qty_spinbox.grid(row=0, column=3, padx=5)

btn_style = {"bg": "#1976d2", "fg": "white", "font": ("Arial", 10, "bold"), "width": 10}

tk.Button(ctrl_frame, text="Add Item", command=add_item, **btn_style).grid(row=0, column=4, padx=5)
tk.Button(ctrl_frame, text="Update Qty", command=update_quantity, **btn_style).grid(row=0, column=5, padx=5)
tk.Button(ctrl_frame, text="Remove Item", command=remove_item, **btn_style).grid(row=0, column=6, padx=5)
tk.Button(ctrl_frame, text="Clear Cart", command=clear_cart, bg="#d32f2f", fg="white", font=("Arial", 10, "bold"), width=10).grid(row=0, column=7, padx=5)

# Initial refresh
refresh_cart()
root.mainloop()