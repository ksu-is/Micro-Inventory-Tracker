from tkinter import *
from tkinter import messagebox
from db import Database

db = Database('store.db')


def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)


def add_item():
    if part_text.get() == '' or sku_text.get() == '' or supplier_text.get() == '' or price_text.get():
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(part_text.get(), sku_text.get(),
              supplier_text.get(), price_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (part_text.get(), sku_text.get(),
                            supplier_text.get(), price_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)

        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        sku_entry.delete(0, END)
        sku_entry.insert(END, selected_item[2])
        supplier_entry.delete(0, END)
        supplier_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
        inventory_entry.delete(0, END)
        inventory_entry.insert(END, selected_item[5])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], part_text.get(), sku_text.get(),
              supplier_text.get(), price_text.get())
    populate_list()


def clear_text():
    part_entry.delete(0, END)
    sku_entry.delete(0, END)
    supplier_entry.delete(0, END)
    price_entry.delete(0, END)
    inventory_entry.delete(0, END)


# Create window object
app = Tk()

# Part
part_text = StringVar()
part_label = Label(app, text='Part Name', font=('bold', 14), pady=20)
part_label.grid(row=0, column=0, sticky=W)
part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=1)
# SKU
sku_text = StringVar()
sku_label = Label(app, text='SKU', font=('bold', 14))
sku_label.grid(row=0, column=2, sticky=W)
sku_entry = Entry(app, textvariable=sku_text)
sku_entry.grid(row=0, column=3)
# Supplier
supplier_text = StringVar()
supplier_label = Label(app, text='Supplier', font=('bold', 14))
supplier_label.grid(row=1, column=0, sticky=W)
supplier_entry = Entry(app, textvariable=supplier_text)
supplier_entry.grid(row=1, column=1)
# Price
price_text = StringVar()
price_label = Label(app, text='Price', font=('bold', 14))
price_label.grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)
# Inventory
inventory_text = StringVar()
inventory_label = Label(app, text='Inventory', font=('bold', 14))
inventory_label.grid(row=0, column=4, sticky=W)
inventory_entry = Entry(app, textvariable=inventory_text)
inventory_entry.grid(row=0, column=5)

# Parts List (Listbox)
parts_list = Listbox(app, height=8, width=50, border=0)
parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Part', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Input', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)

app.title('Part Manager')
app.geometry('700x350')

# Populate data
populate_list()

# Start program
app.mainloop()


# To create an executable, install pyinstaller and run
# '''
# pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' part_manager.py
# '''
#test push