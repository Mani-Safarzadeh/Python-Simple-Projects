from tkinter import *
from utils import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import random

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

class WithdrawMoney:
    def __init__(self, root, file_name, info):
        self.root = root
        self.file_name = file_name
        self.info = info
        self.root.withdraw()
        self.withdraw_window = Toplevel(root)
        self.withdraw_window.title("Withdraw money")
        self.withdraw_window.protocol("WM_DELETE_WINDOW", root.destroy)

        self.lbl_amount = Label(self.withdraw_window, text="Enter Amount:", font=("", 14))
        self.entry_amount = Entry(self.withdraw_window, font=("", 14))

        self.lbl_enter_amount = Label(self.withdraw_window, text="Amount:", font=("", 14))
        self.btn_withdraw = Button(self.withdraw_window, text="Withdraw", font=("", 14), command=self.withdraw)
        self.btn_back = Button(self.withdraw_window, text="Back", font=("", 14), command=lambda: back(root, self.withdraw_window))
        self.lbl_enter_amount.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        self.btn_withdraw.grid(row=2, column=1, padx=10, pady=10, sticky='news')
        self.btn_back.grid(row=2, column=0, padx=10, pady=10, sticky='news')

        self.amounts = ['300000', '500000', '800000', '1200000', '1600000', '20000000', 'Other']
        self.combo_amount = Combobox(self.withdraw_window, values=self.amounts, font=("", 14))
        self.combo_amount.insert(0, "0")
        self.combo_amount.config(state='readonly')
        self.combo_amount.bind("<<ComboboxSelected>>", lambda e: self.bind_combobox())
        self.combo_amount.grid(row=0, column=1, padx=10, pady=10, sticky='news')
    def bind_combobox(self):
        combo_value = self.combo_amount.get()
        if combo_value == "Other":
            self.lbl_amount.grid(row=1, column=0, padx=10, pady=10, sticky="news")
            self.entry_amount.grid(row=1, column=1, padx=10, pady=10, sticky="news")
        else:
            self.lbl_enter_amount.grid_forget()
            self.entry_amount.grid_forget()
    def withdraw(self):
        combo_value = self.combo_amount.get().strip()
        if combo_value == "Other":
            entry_value = self.entry_amount.get().strip()
            if entry_value.isdigit():
                entry_value = int(entry_value)
                if entry_value > 0:
                    if entry_value <= self.info['balance']:
                        if entry_value % 100000 == 0:
                            self.info['balance'] -= entry_value
                            save(self.file_name, self.info)
                            messagebox.showinfo("Success", "Get your cache ->")
                        else:
                            messagebox.showerror("Error", "Invalid amount for money")
                    else:
                        messagebox.showerror("Error", "Not enough money to withdraw")
                else:
                    messagebox.showerror("Error", "Can't withdraw zero or negative amount of money")
            else:
                messagebox.showerror("Error", "Invalid format for money")
        else:
            combo_value = int(combo_value)
            if combo_value <= self.info['balance']:
                if combo_value != 0:
                    self.info['balance'] -= combo_value
                    save(self.file_name, self.info)
                    messagebox.showinfo("Success", "Get your cache ->")
                else:
                    messagebox.showerror("Error", "Can't withdraw zero or negative amount of money")
            else:
                messagebox.showerror("Error", "Not enough money to withdraw")
class Transfer_Money:
    def __init__(self, root, file_name, info):
        self.root = root
        self.file_name = file_name
        self.info = info
        self.root.withdraw()
        self.transfer_window = Toplevel(root)
        self.transfer_window.title("Transfer money")
        self.transfer_window.protocol("WM_DELETE_WINDOW", root.destroy)

        self.lbl_amount = Label(self.transfer_window, font=("", 14), text="Amount of money:", anchor='w')
        self.entry_amount = Entry(self.transfer_window, font=("", 14), width=20)
        self.lbl_dist_card = Label(self.transfer_window, font=("", 14), text="Destination card:", anchor='w')
        self.entry_dist_card = Entry(self.transfer_window, font=("", 14), width=20)
        self.lbl_pin = Label(self.transfer_window, font=("", 14), text="Pin:", anchor='w')
        self.entry_pin = Entry(self.transfer_window, font=("", 14), width=7)
        self.lbl_cvv2 = Label(self.transfer_window, font=("", 14), text="CVV2:", anchor='w')
        self.entry_cvv2 = Entry(self.transfer_window, font=("", 14), width=7)
        self.lbl_year = Label(self.transfer_window, font=("", 14), text="Year:", anchor='w')
        self.entry_year = Entry(self.transfer_window, font=("", 14), width=7)
        self.lbl_month = Label(self.transfer_window, font=("", 14), text="Month:", anchor='w')
        self.entry_month = Entry(self.transfer_window, font=("", 14), width=7)
        self.btn_transfer = Button(self.transfer_window, font=("", 14), text="Transfer", width=20, command=self.transfer)
        self.btn_back = Button(self.transfer_window, font=("", 14), text="Back", width=20, command=lambda: back(root, self.transfer_window))
        self.lbl_amount.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="news")
        self.entry_amount.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="news")
        self.lbl_dist_card.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="news")
        self.entry_dist_card.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="news")
        self.lbl_pin.grid(row=4, column=0, padx=5, pady=5, sticky="news")
        self.entry_pin.grid(row=4, column=1, padx=5, pady=5, sticky="news")
        self.lbl_cvv2.grid(row=4, column=2, padx=5, pady=5, sticky="news")
        self.entry_cvv2.grid(row=4, column=3, padx=5, pady=5, sticky="news")
        self.lbl_year.grid(row=5, column=0, padx=5, pady=5, sticky="news")
        self.entry_year.grid(row=5, column=1, padx=5, pady=5, sticky="news")
        self.lbl_month.grid(row=5, column=2, padx=5, pady=5, sticky="news")
        self.entry_month.grid(row=5, column=3, padx=5, pady=5, sticky="news")
        self.btn_transfer.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="news")
        self.btn_back.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="news")
    def transfer(self):
        amount: str = self.entry_amount.get().strip()
        pin = self.entry_pin.get().strip()
        cvv2 = self.entry_cvv2.get().strip()
        year = self.entry_year.get().strip()
        month = self.entry_month.get().strip()
        if not amount.isdigit():
            messagebox.showerror("Error", "Money not in the correct format")
            return
        if int(amount) > 100000000 or int(amount) < 1:
            messagebox.showerror("Error", "This amount of money is not allowed")
            return
        if self.info['pin'] != pin or self.info['cvv2'] != cvv2:
            messagebox.showerror("Error", "Incorrect pin or cvv2")
            return
        _year_, _month_ = self.info['End Date'].split("/")
        if _year_ != year or _month_ != month:
            messagebox.showerror("Error", "Incorrect end date (year, month)")
            return
        dist_info = read(f"data/{self.entry_dist_card.get()[0:4]}.json")


class Change_Pin:
    def __init__(self, root, file_name, info):
        # Hide the main window
        self.root = root
        self.file_name = file_name
        self.info = info
        self.root.withdraw()

        # Create a new window for changing the pin
        self.pin_window = Toplevel(root)
        self.pin_window.title("Change pin")
        self.pin_window.protocol("WM_DELETE_WINDOW", root.destroy)

        # Create a frame to hold the widgets
        self.frame = LabelFrame(self.pin_window, font=("", 14), text="Change pin")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # Create labels for the old pin, new pin, and repeat new pin
        self.lbl_old = Label(self.frame, font=("", 14), text='Old pin:', anchor='w')
        self.lbl_new = Label(self.frame, font=("", 14), text='New pin:', anchor='w')
        self.lbl_repeat = Label(self.frame, font=("", 14), text='Repeat new pin:', anchor='w')
        self.lbl_old.grid(row=0, column=0, padx=5, pady=5, sticky='news')
        self.lbl_new.grid(row=2, column=0, padx=5, pady=5, sticky='news')
        self.lbl_repeat.grid(row=4, column=0, padx=5, pady=5, sticky='news')

        # Create entry fields for the old pin, new pin, and repeat new pin
        self.entry_old = Entry(self.frame, show="*", font=("", 14), width=18)
        self.entry_new = Entry(self.frame, show="*", font=("", 14), width=18)
        self.entry_repeat = Entry(self.frame, show="*", font=("", 14), width=18)
        self.entry_old.grid(row=1, column=0, padx=5, pady=5, sticky='news')
        self.entry_new.grid(row=3, column=0, padx=5, pady=5, sticky='news')
        self.entry_repeat.grid(row=5, column=0, padx=5, pady=5, sticky='news')

        # Create IntVar variables for the checkboxes
        self.c1 = IntVar(self.frame)
        self.c2 = IntVar(self.frame)
        self.c3 = IntVar(self.frame)

        # Create checkboxes for showing/hiding the old pin
        self.check_btn_1 = Checkbutton(self.frame, variable=self.c1, command=lambda: self.change_check_box(self.c1, self.entry_old))
        self.check_btn_2 = Checkbutton(self.frame, variable=self.c2, command=lambda: self.change_check_box(self.c2, self.entry_new))
        self.check_btn_3 = Checkbutton(self.frame, variable=self.c3, command=lambda: self.change_check_box(self.c3, self.entry_repeat))
        self.check_btn_1.grid(row=1, column=1, padx=5, pady=5, sticky='news')
        self.check_btn_2.grid(row=3, column=1, padx=5, pady=5, sticky='news')
        self.check_btn_3.grid(row=5, column=1, padx=5, pady=5, sticky='news')

        # Create buttons for changing the pin and going back
        self.btn_change = Button(self.frame, text='Change Pin', font=("", 14), width=20, command=self.change)
        self.btn_back = Button(self.frame, text='Back', font=("", 14), width=20, command=lambda: back(root, self.pin_window))
        self.btn_change.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='news')
        self.btn_back.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='news')

    def change_check_box(self, value: IntVar, entry):
        if value.get() == 1:
            entry['show'] = ''
        else:
            entry['show'] = '*'
    def change(self):
        if self.info['pin'] == self.entry_old.get():
            pin1 = self.entry_new.get()
            pin2 = self.entry_repeat.get()
            if pin1 == pin2:
                if pin1.isdigit() and len(pin1) == 4:
                    self.info['pin'] = pin1
                    save(self.file_name, self.info)
                    messagebox.showinfo("Success", "Your pin has changed.")
                    back(self.root, self.pin_window)
                else:
                    messagebox.showwarning("Warning", "Wrong format")
            else:
                messagebox.showwarning("Warning", "No match")
        else:
            messagebox.showerror("Error", "Old pin is invalid")
class Register:
    def __init__(self, login_window):
        # Hide the main window
        self.login_window = login_window
        self.login_window.withdraw()

        # Create a new window for registration
        self.register_window = Toplevel(self.login_window)
        self.register_window.title("Register")
        self.register_window.protocol("WM_DELETE_WINDOW", self.login_window.destroy)

        # Create a frame for the registration form
        self.frame = LabelFrame(self.register_window, font=("", 14), text="Register")
        self.deposite_values = ['500000', '1000000', '2000000', '5000000']
        self.value = IntVar(self.frame)

        # Create labels, Entries, Combobox and RadioButtons for the window
        self.lbl_first = Label(self.frame, font=("", 14), text="First name:", anchor='w')
        self.entry_first = Entry(self.frame, font=("", 14), width=28)
        self.lbl_last = Label(self.frame, font=("", 14), text="Last name:", anchor='w')
        self.entry_last = Entry(self.frame, font=("", 14), width=28)
        self.lbl_pin = Label(self.frame, font=("", 14), text="Four digit pin:", anchor='w')
        self.entry_pin = Entry(self.frame, font=("", 14), width=28)
        self.lbl_deposite = Label(self.frame, font=("", 14), text="Amount of money to deposit:", anchor='w')
        self.box_deposite = Combobox(self.frame, font=("", 14), values=self.deposite_values, width=28)
        self.box_deposite.insert(0, self.deposite_values[0])
        self.box_deposite.config(state='readonly')

        # Create buttons for creating an account and going back
        self.btn_next = Button(self.frame, font=("", 14), width=28, text="Create an account", command=self.register)
        self.btn_back = Button(self.frame, font=("", 14), width=28, text="Back", command=lambda: back(login_window, self.register_window))

        # Bind events to the entry fields
        self.entry_first.bind("<Down>", lambda e: next_entry(self.entry_last))
        self.entry_last.bind("<Down>", lambda e: next_entry(self.entry_pin))
        self.entry_pin.bind("<Return>", self.register)

        # Arrange the widgets in the frame using grid layout
        self.frame.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_first.grid(row=1, column=0, padx=5, pady=5, sticky='news')
        self.entry_first.grid(row=2, column=0, padx=5, pady=5, sticky='news')
        self.lbl_last.grid(row=3, column=0, padx=5, pady=5, sticky='news')
        self.entry_last.grid(row=4, column=0, padx=5, pady=5, sticky='news')
        self.lbl_pin.grid(row=5, column=0, padx=5, pady=5, sticky='news')
        self.entry_pin.grid(row=6, column=0, padx=5, pady=5, sticky='news')
        self.lbl_deposite.grid(row=7, column=0, padx=5, pady=5, sticky='news')
        self.box_deposite.grid(row=8, column=0, padx=5, pady=5, sticky='news')
        self.btn_next.grid(row=9, column=0, padx=5, pady=5, sticky='news')
        self.btn_back.grid(row=10, column=0, padx=5, pady=5, sticky='news')
    def register(self, event=None):
        pin = self.check_pin(self.entry_pin.get().strip())
        if pin:
            first_name = self.entry_first.get().strip()
            last_name = self.entry_last.get().strip()
            balance = int(self.box_deposite.get().strip())
            existings: list = read("data/existings.json")
            card_number = self.generate_unique_card_number(existings)
            existings.append(card_number)
            save("data/existings.json", existings)
            cvv2 = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            end_date = get_end_date()

            info = {
                "first name": first_name,
                "last name": last_name,
                "pin": pin,
                "balance": balance,
                "card number": card_number,
                "cvv2": cvv2,
                "End Date": end_date
            }
            save(f"data/{card_number[0:4]}.json", info)
            messagebox.showinfo("Success", f"Your new account was created\nYour card number: {card_number}")
            self.register_window.destroy()
            self.login_window.deiconify()
        else:
            return

    def check_pin(self, pin: str):
        if len(pin) == 4 and pin.isdigit():
            return pin
        else:
            messagebox.showerror("Error", "Pin must have four digits of number")

    def generate_unique_card_number(self, existings: list) -> str:
        while True:
            card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            if card_number not in existings:
                return card_number


def account_balance(file_name, info):
    if info['balance'] < 12600:
        messagebox.showwarning("Warning", "You don't have enough credit to see your balance")
    else:
        info['balance'] -= 12600
        messagebox.showinfo("Info", f"Your account's balance is {info['balance']} Rial.")
        save(file_name, info)

def login(entry_number, entry_pin, sign_in,  root):
    global file_name, info
    # Get the card number and pin entered by the user
    number = entry_number.get().strip()
    pin = entry_pin.get().strip()

    # Check if the card number and pin are valid
    if len(number) == 16 and len(pin) == 4 and number.isdigit() and pin.isdigit():
        # Create the file name based on the first 4 digits of the card number
        file_name = f"data/{number[0:4]}.json"
        # Read the information from the file
        info = read(file_name)
        # Check if the pin and card number match
        if info['pin'] == pin and info['card number'] == number:
            messagebox.showinfo("Success", f"Welcome {info['first name']} {info['last name']}")
            # Close the sign_in window and restore the main window
            sign_in.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Error", "No such account with this pin and number")
    else:
        messagebox.showerror("Error", "Wrong card number or pin")

def main():
    root = Tk()
    root.withdraw()
    root.title("Financial features")

    # Create buttons for the main window
    btn_withdraw_money = Button(root, text="Withdraw Money", cnf=theme, command=lambda: WithdrawMoney(root, file_name, info))
    btn_transfer_money = Button(root, text="Money Transfer", cnf=theme, command=lambda: Transfer_Money(root, file_name, info))
    btn_account_balance = Button(root, text="Account Balance", cnf=theme, command=lambda : account_balance(file_name, info))
    btn_change_pin = Button(root, text="Change Pin", cnf=theme, command=lambda: Change_Pin(root, file_name, info))

    # Grid layout for the main window buttons
    btn_withdraw_money.grid(row=0, column=0)
    btn_transfer_money.grid(row=0, column=1)
    btn_account_balance.grid(row=1, column=0)
    btn_change_pin.grid(row=1, column=1)

    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.protocol("WM_DELETE_WINDOW", root.destroy)

    # Create a frame for the login form
    frame = LabelFrame(login_window, font=("", 14), text="Login")

    # Create labels and entry fields for card number and pin
    lbl_number = Label(frame, font=("", 14), text="Card number:", anchor='w')
    entry_number = Entry(frame, font=("", 14), width=20)
    lbl_pin = Label(frame, font=("", 14), text="Pin:", anchor='w')
    entry_pin = Entry(frame, font=("", 14), width=20)

    # Create buttons for login and creating a new account
    btn_login = Button(frame, font=("", 14), width=20, text="Login", command=lambda: login(entry_number, entry_pin, login_window, root))
    btn_new = Button(frame, font=("", 14), width=20, text="New Account", command=lambda: Register(login_window))

    # Bind events to the entry fields
    entry_number.bind("<Down>", lambda e: next_entry(entry_pin))
    entry_pin.bind("<Return>", lambda e: login(entry_number, entry_pin, login_window, root))

    # Arrange the widgets in the frame using grid layout
    frame.grid(row=0, column=0, padx=5, pady=5)
    lbl_number.grid(row=1, column=0, padx=5, pady=5, sticky='news')
    entry_number.grid(row=2, column=0, padx=5, pady=5, sticky='news')
    lbl_pin.grid(row=3, column=0, padx=5, pady=5, sticky='news')
    entry_pin.grid(row=4, column=0, padx=5, pady=5, sticky='news')
    btn_login.grid(row=5, column=0, padx=5, pady=5, sticky='news')
    btn_new.grid(row=6, column=0, padx=5, pady=5, sticky='news')

    mainloop()

if __name__ == "__main__":
    main()