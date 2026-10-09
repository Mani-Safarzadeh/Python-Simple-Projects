from tkinter import *
from tkinter import messagebox
import json

def load_file():
    global contacts
    try:
        with open("contacts.json", "r", encoding="utf8") as file:
            contacts = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Source file not found\n You can fill your new contact list")

def save():
    with open("contacts.json", "w", encoding="utf8") as file:
        json.dump(contacts, file, ensure_ascii=False, indent=4)

def add(e):
    name = entry_search.get().lower().strip()
    number = entry_add.get().lower().strip()
    if len(number) == 11 and number.isdigit():
        contacts.update({name: number})
        entry_search.delete(0, END)
        entry_add.delete(0, END)
        messagebox.showinfo("Info", "Done")
        save()
    elif number.startswith("+") and number[1:].isdigit() and 14 > len(number) > 11:
        number = number.replace(number[0:3], "0")
        contacts.update({name: number})
        entry_search.delete(0, END)
        entry_add.delete(0, END)
        messagebox.showinfo("Info", "Done")
        save()
    else:
        messagebox.showerror("Error", "Number is not long enough or\n It's not in the correct format.")

def search(event=None):
    name = entry_search.get()
    name = name.lower().strip()
    if name in contacts.keys():
        messagebox.showinfo("Info" , f"{name}'s number is {contacts[name]}")
        entry_add.grid_forget()
        btn_add.grid_forget()
    else:
        messagebox.showinfo("Info" , f"{name.capitalize()} is not in phone book.\nYou can add {name.capitalize()} to phone book if you wish.")
        entry_add.grid(row=1, column=0, ipadx=10, ipady=10, sticky="news")
        btn_add.grid(row=1, column=1, ipadx=10, ipady=10, sticky="news")

# variables
contacts = {}
load_file()
root = Tk()
root.title("Phone Book")

entry_search = Entry(root, font=("", 14),)
entry_add = Entry(root, font=("", 14))

entry_search.bind("<Return>", lambda e: search())
entry_add.bind("<Return>", lambda e: add())

btn_Search = Button(root, font=("", 14), text="Search", command=search)
btn_add = Button(root, font=("", 14), text="Add", command=add)

entry_search.grid(row=0, column=0, ipadx=10, ipady=10, sticky="news")
btn_Search.grid(row=0, column=1, ipadx=10, ipady=10, sticky="news")

mainloop()