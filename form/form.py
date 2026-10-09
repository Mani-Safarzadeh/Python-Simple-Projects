from tkinter import *

def save():
    with open(f"{entry_name.get()}.txt", 'w', encoding='utf8') as f:
        f.write(f"{entry_name.get()}\n{entry_age.get()}")
    entry_age.get()

root = Tk()
root.resizable(0, 0)
root.title('From')
# root.geometry('600x300')

entry_name = Entry(root, font=("", 14))
entry_age  = Entry(root, font=("", 14))

lbl_name = Label(root, font=("", 14), text="Enter your name: ")
lbl_age  = Label(root,  font=("", 14),text="Enter your age: ")
btn_quit = Button(root, font=("", 14), text="Exit", command=exit)
btn_save = Button(root,  font=("", 14),text="Save", command=save)

entry_name.grid(row=0, column=1, padx=10, pady=10, sticky='news')
entry_age.grid(row=1, column=1, padx=10, pady=10, sticky='news')
lbl_name.grid(row=0, column=0, padx=10, pady=10, sticky='news')
lbl_age.grid(row=1, column=0, padx=10, pady=10, sticky='news')
btn_quit.grid(row=2, column=0, padx=10, pady=10, sticky='news')
btn_save.grid(row=2, column=1, padx=10, pady=10, sticky='news')

mainloop()