import tkinter as tk
from tkinter import messagebox
from db import Database

# Instanciate databse object
db = Database('store.db')

# Main Application/GUI class


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Microsystems Inventory Tracker')
        # Width height
        master.geometry("700x350")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # Part
        self.part_text = tk.StringVar()
        self.part_label = tk.Label(
            self.master, text='Part Name', font=('bold', 14), pady=20)
        self.part_label.grid(row=0, column=0, sticky=tk.W)
        self.part_entry = tk.Entry(self.master, textvariable=self.part_text)
        self.part_entry.grid(row=0, column=1)
        # SKU 
        self.sku_text = tk.StringVar()
        self.sku_label = tk.Label(
            self.master, text='SKU', font=('bold', 14))
        self.sku_label.grid(row=0, column=2, sticky=tk.W)
        self.sku_entry = tk.Entry(
            self.master, textvariable=self.sku_text)
        self.sku_entry.grid(row=0, column=3)
        # Supplier
        self.supplier_text = tk.StringVar()
        self.supplier_label = tk.Label(
            self.master, text='Supplier', font=('bold', 14))
        self.supplier_label.grid(row=1, column=0, sticky=tk.W)
        self.supplier_entry = tk.Entry(
            self.master, textvariable=self.supplier_text)
        self.supplier_entry.grid(row=1, column=1)
        # Price
        self.price_text = tk.StringVar()
        self.price_label = tk.Label(
            self.master, text='Price', font=('bold', 14))
        self.price_label.grid(row=1, column=2, sticky=tk.W)
        self.price_entry = tk.Entry(self.master, textvariable=self.price_text)
        self.price_entry.grid(row=1, column=3)
        # Stock
        self.inventory_text = tk.StringVar()
        self.inventory_label = tk.Label(
            self.master, text='Stock', font=('bold', 14))
        self.inventory_label.grid(row=0, column=5, sticky=tk.W)
        self.inventory_entry = tk.Entry(self.master, textvariable=self.inventory_text)
        self.inventory_entry.grid(row=0, column=6)

        # Parts list (listbox)
        self.parts_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.parts_list.grid(row=3, column=0, columnspan=3,
                             rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        # Set scrollbar to parts
        self.parts_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.parts_list.yview)

        # Bind select
        self.parts_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add Part", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Remove Part", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(
            self.master, text="Update Part", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.exit_btn = tk.Button(
            self.master, text="Clear Input", width=12, command=self.clear_text)
        self.exit_btn.grid(row=2, column=3)

    def populate_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.parts_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.parts_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.part_text.get() == '' or self.sku_text.get() == '' or self.supplier_text.get() == '' or self.price_text.get() == '' or self.inventory_text.get() == '':
            messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        print(self.part_text.get())
        # Insert into DB
        db.insert(self.part_text.get(), self.sku_text.get(),
                  self.supplier_text.get(), self.price_text.get(), self.inventory.get())
        # Clear list
        self.parts_list.delete(0, tk.END)
        # Insert into list
        self.parts_list.insert(tk.END, (self.part_text.get(), self.sku_text.get(
        ), self.supplier_text.get(), self.price_text.get(), self.inventory.get()))
        self.clear_text()
        self.populate_list()

    # Runs when item is selected
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.parts_list.curselection()[0]
            # Get selected item
            self.selected_item = self.parts_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.part_entry.delete(0, tk.END)
            self.part_entry.insert(tk.END, self.selected_item[1])
            self.sku_entry.delete(0, tk.END)
            self.sku_entry.insert(tk.END, self.selected_item[2])
            self.supplier_entry.delete(0, tk.END)
            self.supplier_entry.insert(tk.END, self.selected_item[3])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, self.selected_item[4])
            self.inventory_entry.delete(0, tk.END)
            self.inventory_entry.insert(tk.END, self.selected_item[5])
        except IndexError:
            pass

    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.part_text.get(
        ), self.sku_text.get(), self.supplier_text.get(), self.price_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.part_entry.delete(0, tk.END)
        self.sku_entry.delete(0, tk.END)
        self.supplier_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
