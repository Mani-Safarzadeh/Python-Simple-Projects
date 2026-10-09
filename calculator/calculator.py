from tkinter import *

root = Tk()
root.title("simple calculator")

def button_click(number):
    entry_calculation.insert(END, number)

def button_clear():
    entry_calculation.delete(0, END)

def equal():
    phrase = entry_calculation.get()
    try:
        answer = eval(phrase)
    except ZeroDivisionError:
        entry_calculation.delete(0, END)
        entry_calculation.insert(0, "Error")
        return
    except NameError:
        entry_calculation.delete(0, END)
        entry_calculation.insert(0, "Error")
        return
    entry_calculation.delete(0, END)
    entry_calculation.insert(0, answer)

entry_calculation = Entry(root, font=("", 15))
btn_1 = Button(root, text="1", font=("", 15), command=lambda: button_click(1))
btn_2 = Button(root, text="2", font=("", 15), command=lambda: button_click(2))
btn_3 = Button(root, text="3", font=("", 15), command=lambda: button_click(3))
btn_4 = Button(root, text="4", font=("", 15), command=lambda: button_click(4))
btn_5 = Button(root, text="5", font=("", 15), command=lambda: button_click(5))
btn_6 = Button(root, text="6", font=("", 15), command=lambda: button_click(6))
btn_7 = Button(root, text="7", font=("", 15), command=lambda: button_click(7))
btn_8 = Button(root, text="8", font=("", 15), command=lambda: button_click(8))
btn_9 = Button(root, text="9", font=("", 15), command=lambda: button_click(9))
btn_0 = Button(root, text="0", font=("", 15), command=lambda: button_click(0))
btn_plus     = Button(root, text="+", font=("", 15), command=lambda: button_click('+'))
btn_minus    = Button(root, text="-", font=("", 15), command=lambda: button_click('-'))
btn_multiply = Button(root, text="*", font=("", 15), command=lambda: button_click('*'))
btn_divide   = Button(root, text="/", font=("", 15), command=lambda: button_click('/'))
btn_clear    = Button(root, text="C", font=("", 15), command=button_clear)
btn_equal    = Button(root, text="=", font=("", 15), command=equal)

entry_calculation.grid(row=0, column=0, columnspan=4, sticky="news", ipadx=10, ipady=10)
btn_1.grid(row=3, column=0, sticky='news', ipadx=15, ipady=15)
btn_2.grid(row=3, column=1, sticky='news', ipadx=15, ipady=15)
btn_3.grid(row=3, column=2, sticky='news', ipadx=15, ipady=15)
btn_4.grid(row=2, column=0, sticky='news', ipadx=15, ipady=15)
btn_5.grid(row=2, column=1, sticky='news', ipadx=15, ipady=15)
btn_6.grid(row=2, column=2, sticky='news', ipadx=15, ipady=15)
btn_7.grid(row=1, column=0, sticky='news', ipadx=15, ipady=15)
btn_8.grid(row=1, column=1, sticky='news', ipadx=15, ipady=15)
btn_9.grid(row=1, column=2, sticky='news', ipadx=15, ipady=15)
btn_0.grid(row=4, column=1, sticky='news', ipadx=15, ipady=15)
btn_equal.grid(row=4, column=2, sticky='news', ipadx=15, ipady=15)
btn_plus.grid(row=1, column=3, sticky='news', ipadx=15, ipady=15)
btn_minus.grid(row=2, column=3, sticky='news', ipadx=15, ipady=15)
btn_multiply.grid(row=3, column=3, sticky='news', ipadx=15, ipady=15)
btn_divide.grid(row=4, column=3, sticky='news', ipadx=15, ipady=15)
btn_clear.grid(row=4, column=0, sticky='news', ipadx=15, ipady=15)

mainloop()