from tkinter import *
from time import sleep
from random import randint
import datetime

theme = {
    "bg": "#333333",
    "fg": "orange",
    "activebackground": "#272729",
    "activeforeground": "orange",
    "width": 20,
    "height": 3,
    "font": ("", 14),
    "padx": 10,
    "pady": 10
}


# functions
def do_work(n):
    if n == 1:
        try:
            customer = customers.pop(0)
            State_1.config(text=f"Doing customer\n#{customer} work.")
            operator_1.config(state='disabled', disabledforeground='#fff')
            for i in range(randint(5, 30)):
                sleep(0.1)
                root.update()
            State_1.config(text=f"Customer #{customer}\n work's done.")
            operator_1.config(state='normal')
        except IndexError:
            State_1.config(text=f"No customers in queue.")
    elif n == 2:
        try:
            customer = customers.pop(0)
            State_2.config(text=f"Doing customer\n#{customer} work.")
            operator_2.config(state='disabled', disabledforeground='#fff')
            for i in range(randint(5, 30)):
                sleep(0.1)
                root.update()
            State_2.config(text=f"Customer #{customer}\n work's done.")
            operator_2.config(state='normal')
        except IndexError:
            State_2.config(text=f"No customers in queue.")
    else:
        try:
            customer = customers.pop(0)
            State_3.config(text=f"Doing customer\n#{customer} work.")
            operator_3.config(state='disabled', disabledforeground='#fff')
            for i in range(randint(5, 30)):
                sleep(0.1)
                root.update()
            State_3.config(text=f"Customer #{customer}\n work's done.")
            operator_3.config(state='normal')
        except IndexError:
            State_3.config(text=f"No customers in queue.")


def getNumber(total_customers: int):
    customers.append(total_customers)
    total_customers += 1
    now = str(datetime.datetime.now())
    date = now[0:10]
    time = now[11:19]
    paper.config(text=f"{date}\n{time}\nYour number:{total_customers}\nPeople in queue: {len(customers)}")


customers = []
total_customers = 100

# Pages and configs
root = Tk()
information = Toplevel(root)
operators = Toplevel(root)
root.config(bg="#272729")
information.config(bg="#272729")
operators.config(bg="#272729")
root.title('Options')
information.title('information')
operators.title('operators')

# places
root.geometry('+350+60')
information.geometry('+650+100')
operators.geometry('+300+300')

# root
get_number = Button(root, text="Get Number", cnf=theme, height=2, command=lambda: getNumber(total_customers))
Exit = Button(root, text='Exit', font=("", 15), cnf=theme, height=2, command=exit)
get_number.grid(row=0, column=0, padx=10, pady=10)
Exit.grid(row=1, column=0, padx=10, pady=10)

# information
paper = Label(information, text="Null", cnf=theme, height=4)
paper.grid(row=0, column=0, padx=10, pady=10)

# operators
operator_1 = Button(operators, text='Operator 1', cnf=theme, height=2, command=lambda: do_work(1))
operator_2 = Button(operators, text='Operator 2', cnf=theme, height=2, command=lambda: do_work(2))
operator_3 = Button(operators, text='Operator 3', cnf=theme, height=2, command=lambda: do_work(3))
State_1 = Button(operators, text='State 1', cnf=theme, height=2)
State_2 = Button(operators, text='State 2', cnf=theme, height=2)
State_3 = Button(operators, text='State 3', cnf=theme, height=2)

operator_1.grid(row=0, column=0, padx=10, pady=10)
operator_2.grid(row=0, column=1, padx=10, pady=10)
operator_3.grid(row=0, column=2, padx=10, pady=10)
State_1.grid(row=1, column=0, padx=10, pady=10)
State_2.grid(row=1, column=1, padx=10, pady=10)
State_3.grid(row=1, column=2, padx=10, pady=10)

mainloop()
