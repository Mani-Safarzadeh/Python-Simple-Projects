from tkinter import *
from datetime import datetime
import json

def next_entry(entry: Entry):
    entry.focus_set()

def save(file_name, info):
    # Save the info dictionary to a JSON file
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

def read(file_name):
    try:
        # Read the JSON file and return the loaded data
        with open(file_name, "r", encoding="utf8") as f:
            info = json.load(f)
        return info
    except FileNotFoundError:
        # If the file is not found, return False
        return False
    
def back(tk: Tk, toplevel: Toplevel):
    # Destroy the window and restore the root window
    toplevel.destroy()
    tk.deiconify()

def tax(n: int) -> str:
    tax = (n * 7) / 100
    if n < 10000000:
        tax += 600
        return tax
    else:
        tax += (n // 10000000) * 600
        return tax

def get_end_date():
    today = str(datetime.now())[0:10]
    year, month, day = today.split("-")
    return (f"{year[2:4]}/{month}")