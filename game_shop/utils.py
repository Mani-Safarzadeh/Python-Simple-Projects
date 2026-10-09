from tkinter import Tk
import json

def change_window(current: Tk, new: Tk):
    current.withdraw()
    new.deiconify()

def load():
    with open('file.json', 'r', encoding='utf8') as file:
        return json.load(file)
    
def save(info):
    with open('file.json', 'w', encoding='utf8') as file:
        json.dump(info, file, ensure_ascii=False, indent=4)
