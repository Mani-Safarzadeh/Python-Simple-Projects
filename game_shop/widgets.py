from tkinter import *
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from settings import *
from utils import *
import pymysql
import re
import sys
import smtplib, ssl


class MyConnection:
    def __init__(self, user='root', password='root'):
        self.db = pymysql.connect(host='127.0.0.1', user=user, password=password, charset='utf8')
        self.cursor = self.db.cursor()

    def create_schema(self):
        query = "CREATE SCHEMA IF NOT EXISTS `game`;"
        self.cursor.execute(query)
        
    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS `game`.`games` (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,`name` VARCHAR(45) NOT NULL,`company` VARCHAR(40) NULL,`age` TINYINT UNSIGNED NULL,`price` INT UNSIGNED NOT NULL,`console` VARCHAR(30) NULL,`stock` SMALLINT UNSIGNED NOT NULL,`image` VARCHAR(200) NULL,PRIMARY KEY (`id`),UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE);"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS `game`.`users` (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,`username` VARCHAR(45) NOT NULL,`password` VARCHAR(45) NOT NULL,`email` VARCHAR(100) NULL,`phone` VARCHAR(15) NULL,PRIMARY KEY (`id`),UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS `game`.`order` (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,`name` VARCHAR(45) NOT NULL,`fullname` VARCHAR(45) NOT NULL,`number` SMALLINT(15) UNSIGNED NOT NULL,`address` VARCHAR(45) NOT NULL,`postal code` VARCHAR(45) NULL,PRIMARY KEY (`id`),UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,UNIQUE INDEX `postal code_UNIQUE` (`postal code` ASC) VISIBLE);"
        
    def select(self, name):
        query = "SELECT * FROM `game`.`games` WHERE `name`=%s"
        values = (name,)
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def select_all(self):
        query = "SELECT * FROM `game`.`games`;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, name, company, age, price, console, stock, file_address):
        query = "INSERT INTO `game`.`games` (`name`, `company`, `age`, `price`, `console`, `stock`, `image`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (name, company, age, price, console, stock, file_address)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error

    def delete(self, name):
        query = "DELETE FROM `game`.`games` WHERE `name`=%s"
        values = (name,)
        result = self.cursor.execute(query, values)
        self.db.commit()
        return result

    def update(self, name, company, age, price, console, stock, file_address, oldname):
        query = "UPDATE `game`.`games` SET `name`=%s, `company`=%s, `age`=%s, `price`=%s, `console`=%s, `stock`=%s, `image`=%s WHERE `name`=%s;"
        values = (name, company, age, price, console, stock, file_address, oldname)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error
        
    def search(self, name=None, company=None, age=None, min_price=None, max_price=None, console=None, min_stock=None, max_stock=None):
        query = "SELECT * FROM `game`.`games` WHERE 1=1"
        conditions = []
        values = []
        if name:
            conditions.append("`name` LIKE %s")
            values.append(f"%{name}%")
        if company:
            conditions.append("`company` LIKE %s")
            values.append(f"%{company}%")
        if age:
            conditions.append("`age` >=%s")
            values.append(age)
        if min_price:
            conditions.append("`price` >= %s")
            values.append(min_price)
        if max_price:
            conditions.append("`price` <= %s")
            values.append(max_price)
        if console:
            conditions.append("`console` LIKE %s")
            values.append(f"%{console}%")
        if min_stock:
            conditions.append("`stock` >= %s")
            values.append(min_stock)
        if max_stock:
            conditions.append("`stock` <= %s")
            values.append(max_stock)
        if conditions:
            query += " AND " + " AND ".join(conditions)
            self.cursor.execute(query, tuple(values))
            return self.cursor.fetchall()
        else:
            return self.select_all()

    def add_user(self, username, password, email=None, phone=None):
        query = "INSERT INTO `game`.`users` (`username`, `password`, `email`, `phone`) VALUES (%s, %s, %s, %s)"
        values = (username, password, email, phone)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error

    def find_user(self, username, password):
        query = "SELECT * FROM `game`.`users` WHERE `username`=%s AND `password`=%s"
        values = (username, password)
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.db.close()

class SearchWindow:
    def __init__(self, root: Tk, connection: MyConnection):
        self.root = root
        self.connection = connection

        self.view = ttk.Treeview(self.root, selectmode='browse')
        self.verscrlbar = ttk.Scrollbar(self.root, orient="vertical", command=self.view.yview)
        self.view.grid(row=1, column=1, columnspan=10)
        self.verscrlbar.grid(row=1, column=11, sticky='ns')
        self.view.configure(yscrollcommand=self.verscrlbar.set)

        self.view.bind('<Double-1>', self.on_double_click)
        self.lbl_image = Label(self.root)

        columns = ("1", "2", "3" , "4" , "5" , "6")
        widths = (180, 180, 75, 100, 100, 80)
        headings = ('Name', 'Company', 'Age', 'Price', 'Console', 'Stock')
        self.view["columns"] = columns
        self.view['show'] = 'headings'
        for column, width in zip(columns, widths):
            self.view.column(column, width=width, anchor='center')
        for column, heading in zip(columns, headings):
            self.view.heading(column, text=heading)

        self.refresh_database()

        Label(self.root, cnf=config_lbl, text='Search by Name: ').grid(row=2, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Company: ').grid(row=3, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Age: ').grid(row=4, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Min Price: ').grid(row=5, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Max Price: ').grid(row=6, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Console: ').grid(row=7, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Min Stock: ').grid(row=8, column=1)
        Label(self.root, cnf=config_lbl, text='Search by Max Stock: ').grid(row=9, column=1)
        self.e_name = Entry(self.root, cnf=config_entry)
        self.e_company = Entry(self.root, cnf=config_entry)
        self.e_age = Entry(self.root, cnf=config_entry)
        self.e_min_price = Entry(self.root, cnf=config_entry)
        self.e_max_price = Entry(self.root, cnf=config_entry)
        self.e_console = Entry(self.root, cnf=config_entry)
        self.e_min_stock = Entry(self.root, cnf=config_entry)
        self.e_max_stock = Entry(self.root, cnf=config_entry)
        self.e_name.grid(row=2, column=2)
        self.e_company.grid(row=3, column=2)
        self.e_age.grid(row=4, column=2)
        self.e_min_price.grid(row=5, column=2)
        self.e_max_price.grid(row=6, column=2)
        self.e_console.grid(row=7, column=2)
        self.e_min_stock.grid(row=8, column=2)
        self.e_max_stock.grid(row=9, column=2)
        self.btn_search = Button(self.root, cnf=config_btn, text="Search", command=self.search)
        self.btn_buy = Button(self.root, cnf=config_btn, text="Buy", command=self.buy)
        self.btn_search.grid(row=3, rowspan=2, sticky='news', column=4)
        self.btn_buy.grid(row=5, rowspan=2, sticky='news', column=4)

    def search(self):
        games = self.connection.search (
            self.e_name.get().strip(),
            self.e_company.get().strip(),
            self.e_age.get().strip(),
            self.e_min_price.get().strip(),
            self.e_max_price.get().strip(),
            self.e_console.get().strip(),
            self.e_min_stock.get().strip(),
            self.e_max_stock.get().strip()
        )
        self.view.delete(*self.view.get_children())
        for game in games:
            self.view.insert('', 'end', text=game[0], values=(game[1:8]))

    def buy(self):
        game = item = self.view.selection()[0]
        game = self.view.item(item, 'values')[0]
        email_window = Email(self.root, game)

    def refresh_database(self):
        self.view.delete(*self.view.get_children())
        games = self.connection.select_all()
        for game in games:
            self.view.insert('', 'end', text=f'row{game[0]}', values=(game[1:8]))

    def on_double_click(self, event):
        item = self.view.selection()[0]
        asks = self.view.item(item, 'values')[-1]
        try:
            img = Image.open(asks)
            img = img.resize((250, 250))
            img = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=img)
        except FileNotFoundError:
            self.lbl_image.grid_forget()
            return
        finally:
            self.lbl_image.grid(row=1, column=12)
            self.root.mainloop()



class LoginOrRegister:
    def __init__(self, root: Tk, management_window: Tk, connection: MyConnection):
        self.root = root
        self.management_window = management_window
        self.connection = connection
        self.frame_login = LabelFrame(self.root, cnf=config_lbl_frame, text='Login')
        self.frame_register = LabelFrame(self.root, cnf=config_lbl_frame, text='Register')
        self.frame_login.grid(row=0, column=0, padx=10, pady=10)
        self.frame_register.grid(row=0, column=1, padx=10, pady=10)

        Label(self.frame_login, cnf=config_lbl, text='Username').grid(row=0, column=0, padx=PADX, pady=PADY)
        Label(self.frame_login, cnf=config_lbl, text='Password').grid(row=1, column=0, padx=PADX, pady=PADY)
        Label(self.frame_register, cnf=config_lbl, text='Username').grid(row=0, column=0, padx=PADX, pady=PADY)
        Label(self.frame_register, cnf=config_lbl, text='Password').grid(row=1, column=0, padx=PADX, pady=PADY)
        Label(self.frame_register, cnf=config_lbl, text='Email').grid(row=2, column=0, padx=PADX, pady=PADY)
        Label(self.frame_register, cnf=config_lbl, text='Phone').grid(row=3, column=0, padx=PADX, pady=PADY)

        self.e_login_username = Entry(self.frame_login, cnf=config_entry)
        self.e_login_password = Entry(self.frame_login, cnf=config_entry)
        self.e_register_username = Entry(self.frame_register, cnf=config_entry)
        self.e_register_password = Entry(self.frame_register, cnf=config_entry)
        self.e_register_email = Entry(self.frame_register, cnf=config_entry)
        self.e_register_phone = Entry(self.frame_register, cnf=config_entry)

        self.e_login_username.grid(row=0, column=1, padx=PADX, pady=PADY)
        self.e_login_password.grid(row=1, column=1, padx=PADX, pady=PADY)
        self.e_register_username.grid(row=0, column=1, padx=PADX, pady=PADY)
        self.e_register_password.grid(row=1, column=1, padx=PADX, pady=PADY)
        self.e_register_email.grid(row=2, column=1, padx=PADX, pady=PADY)
        self.e_register_phone.grid(row=3, column=1, padx=PADX, pady=PADY)

        btn_sumbit_login = Button(self.frame_login, cnf=config_btn, text='Sumbit', command=self.sumbit_login)
        btn_sumbit_register = Button(self.frame_register, cnf=config_btn, text='Sumbit', command=self.submit_register)
        btn_sumbit_login.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY)
        btn_sumbit_register.grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY)

    def sumbit_login(self):
        username = self.e_login_username.get().strip()
        password = self.e_login_password.get().strip()

        account = self.connection.find_user(username, password)
        if account:
            messagebox.showinfo('Welcome', 'You have logged in successfully')
            self.root.destroy()
            self.management_window.deiconify()
            save({'is_logged_in': True})
            return
        messagebox.showerror('Error', 'No accounts found with such username and password')

    def submit_register(self):
        username = self.e_register_username.get().strip()
        password = self.e_register_password.get().strip()
        email = self.e_register_email.get().strip()
        phone = self.e_register_phone.get().strip()

        if email == '':
            email = None
        if phone == '':
            phone = None

        if username == '':
            messagebox.showerror('Error', 'You can not leave the username field empty')
            return
        if password == '':
            messagebox.showerror('Error', 'You can not leave the password field empty')
            return
        if len(password) < 8:
            messagebox.showerror('Error', 'At least eight characters are required for a password')
            return
        
        if email:
            if not re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email, re.IGNORECASE):
                messagebox.showerror('Error', 'Incorrect format for email')
                return
        if phone:
            if not re.search(r"^\+?\d{1,4}-?\d{1,3}-?\d+$", phone, re.IGNORECASE):
                messagebox.showerror('Error', 'Incorrect format for phone number')
                return
            if len(phone) > 15:
                messagebox.showerror('Error', 'Phone number length is too large')
                return
            
        result = self.connection.add_user(username, password, email, phone)
        if result == 0:
            messagebox.showinfo('Done', 'Your new account has been created')
            self.root.destroy()
            self.management_window.deiconify()
            save({'is_logged_in': True})
            return
        messagebox.showerror('Error', result)


class InsertWindow:
    def __init__(self, root, connection: MyConnection, text="Insert Games"):
        self.connection = connection
        self.root = root
        self.frame = LabelFrame(self.root, text=text, cnf=config_lbl_frame)
        
        self.l_name = Label(self.frame, text="Game Name: ", cnf=config_lbl)
        self.l_company = Label(self.frame, text="Company: ", cnf=config_lbl)
        self.l_age = Label(self.frame, text="Age Classification: ", cnf=config_lbl)
        self.l_price = Label(self.frame, text="Price: ", cnf=config_lbl)
        self.l_console = Label(self.frame, text="Console: ", cnf=config_lbl)
        self.l_stock = Label(self.frame, text="Amount in stock: ", cnf=config_lbl)
        self.l_address = Label(self.frame, text="Picture Address: ", cnf=config_lbl)

        self.e_name = Entry(self.frame, cnf=config_entry)
        self.e_company = Entry(self.frame, cnf=config_entry)
        self.e_age = ttk.Combobox(self.frame, values=['', '+3', '+7', '+10', '+12', '+15', '+17', '+25'], foreground=FG, justify='center', font=FONT, state='readonly')
        self.e_price = Entry(self.frame, cnf=config_entry)
        self.e_console = Entry(self.frame, cnf=config_entry)
        self.e_stock = Entry(self.frame, cnf=config_entry)
        self.e_address = Button(self.frame, text='...', cnf=config_btn, command=self.seak_picture)
        self.file_address = None

        self.btn_save  = Button(self.frame, text="Save", cnf=config_btn, command=lambda: self.save(purpose='save'))
        self.btn_reset = Button(self.frame, text="Reset", cnf=config_btn, command=self.reset)
        
        self.l_name.grid(row=1, column=1, cnf=grid_config)
        self.l_company.grid(row=3, column=1, cnf=grid_config)
        self.l_age.grid(row=5, column=1, cnf=grid_config)
        self.l_price.grid(row=7, column=1, cnf=grid_config)
        self.l_console.grid(row=9, column=1, cnf=grid_config)
        self.l_stock.grid(row=11, column=1, cnf=grid_config)
        self.l_address.grid(row=13, column=1, cnf=grid_config)

        self.e_name.grid(row=1, column=3, cnf=grid_config)
        self.e_company.grid(row=3, column=3, cnf=grid_config)
        self.e_age.grid(row=5, column=3, cnf=grid_config)
        self.e_price.grid(row=7, column=3, cnf=grid_config)
        self.e_console.grid(row=9, column=3, cnf=grid_config)
        self.e_stock.grid(row=11, column=3, cnf=grid_config)
        self.e_address.grid(row=13, column=3, cnf=grid_config)

        self.btn_save.grid(row=15, column=1, cnf=grid_config)
        self.btn_reset.grid(row=15, column=3, cnf=grid_config)

        style = ttk.Style(self.root)
        style.theme_create(f'madval_style{self}', parent='alt',settings = {'TCombobox':{'configure':{'selectbackground': BG,'fieldbackground': BG,'background': BG}}})
        style.theme_use(f'madval_style{self}')
        style.map('TCombobox', fieldbackground=[('readonly', BG)])
        style.map('TCombobox', selectbackground=[('readonly', BG)])
        style.map('TCombobox', selectforeground=[('readonly',  FG)])
        style.configure("Treeview", background=BG, foreground=FG, rowheight=32, fieldbackground=BG, font=('Consalos', 16))
        style.configure("Treeview.Heading", background="#222222", foreground="cyan", font=('Consalos', 18))
        style.map("Treeview", background=[('selected', FG)])
        style.map("Treeview", foreground=[('selected', BG)])
    
    def reset(self):
        self.e_name.delete(0, END)
        self.e_company.delete(0, END)
        self.e_age.configure(state='normal')
        self.e_age.delete(0, END)
        self.e_age.configure(state='readonly')
        self.e_price.delete(0, END)
        self.e_console.delete(0, END)
        self.e_stock.delete(0, END)
        self.file_address = None
        self.e_address.config(text='...', image='')
        self.e_name.focus_set()

    def seak_picture(self):
        self.file_address = filedialog.askopenfilename()
        self.set_picture()

    def set_picture(self):
        try:
            if not self.file_address:
                self.file_address = None
                self.e_address.configure(text='...', image='')
                return
            self.img = Image.open(self.file_address)
            self.img = self.img.resize((200, 200))
            self.img = ImageTk.PhotoImage(self.img)
            self.e_address.configure(image=self.img)
        except:
            self.file_address = None
            self.e_address.configure(text='...', image='')

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def save(self, purpose, oldname=None):
        name = self.e_name.get().strip()
        company = self.e_company.get().strip()
        age = self.e_age.get().strip()
        price = self.e_price.get().strip()
        console = self.e_console.get().strip()
        stock = self.e_stock.get().strip()
        file_address = self.file_address

        if name == '':
            messagebox.showerror('Error', 'You can not leave the name field empty')
            return
        if price == '':
            messagebox.showerror('Error', 'You can not leave the price field empty')
            return
        if stock == '':
            messagebox.showerror('Error', 'You can not leave the stock field empty')
            return
        
        try:
            price = float(price)
            if price < 0:
                messagebox.showerror('Error', 'Negative values are not allowed for price')
                return
        except ValueError:
            messagebox.showerror('Error', 'Incorrect fromat for price')
            return

        try:
            stock = int(stock)
            if stock < 0:
                messagebox.showerror('Error', 'Negative values are not allowed for stock')
                return
        except ValueError:
            messagebox.showerror('Error', 'Incorrect format for stock')
            return

        if age == '':
            age = None
        if company == '':
            company = None
        if console == '':
            console = None
        if file_address == '':
            file_address = None

        if purpose == 'save':
            result = self.connection.insert(name, company, age, price, console, stock, file_address)
            if result == 0:
                messagebox.showinfo('Saved', 'Your game\'s info was saved.')
            else:
                messagebox.showerror('Error', result)

        elif purpose == 'update':
            result = self.connection.update(name, company, age, price, console, stock, file_address, oldname)
            if result == 0:
                messagebox.showinfo('Saved', 'Your game\' info was updated')
                return
            else:
                messagebox.showerror('Error', result)
        
        self.reset()


class UpdateWindow(InsertWindow):
    def __init__(self, root, connection: MyConnection, text='Update Games'):
        super().__init__(root, connection)
        self.disable()
        self.frame.configure(text=text)
        self.btn_save.configure(text="Update", command=self.update)
        
        self.frame2 = Frame(self.root, bg=BG)
        self.l_search_game = Label(self.frame2, text="Search games to be updated: ", cnf=config_lbl, padx=PADX*2, pady=PADY*2)
        self.e_search_game = Entry(self.frame2, cnf=config_entry)
        self.btn_search = Button(self.frame2, text="Search", cnf=config_btn, command=self.search)
        
        self.frame2.grid(row=0, column=1)
        self.l_search_game.grid(row=0, column=1)
        self.e_search_game.grid(row=1, column=1)
        self.btn_search.grid(row=2, column=1)
    
    def disable(self):
        self.e_name.configure(state='disabled', disabledbackground=BG)
        self.e_company.configure(state='disabled', disabledbackground=BG)
        self.e_age.configure(state='disabled')
        self.e_price.configure(state='disabled', disabledbackground=BG)
        self.e_console.configure(state='disabled', disabledbackground=BG)
        self.e_stock.configure(state='disabled', disabledbackground=BG)
        self.e_address.configure(state='disabled')
        self.btn_save.configure(state='disabled')
        self.btn_reset.configure(state='disabled')

    def enable(self):
        self.e_name.configure(state='normal')
        self.e_company.configure(state='normal')
        self.e_age.configure(state='readonly')
        self.e_price.configure(state='normal')
        self.e_console.configure(state='normal')
        self.e_stock.configure(state='normal')
        self.e_address.configure(state='normal')
        self.btn_save.configure(state='normal')
        self.btn_reset.configure(state='normal')

    def updatename(self):
        oldname = self.e_search_game.get().strip()
        return self.connection.select(oldname), oldname
    
    def showinfo(self, info):
        self.e_name.insert(0, info[1])
        if info[2] != None:
            self.e_company.insert(0, info[2])
        if info[3] != None:
            self.e_age.config(state='normal')
            self.e_age.insert(0, info[3])
            self.e_age.config(state='readonly')
        self.e_price.insert(0, info[4])
        if info[5] != None:
            self.e_console.insert(0, info[5])
        self.e_stock.insert(0, info[6])
        if info[7] != None:
            self.file_address = info[7]
        self.set_picture()
    
    def search(self):
        self.enable()
        self.reset()
        info, oldname = self.updatename()

        if info:
            self.showinfo(info)
            messagebox.showinfo('Found', 'The game was found.\nNow you can update tha game.')
        else:
            self.disable()
            messagebox.showerror('Error', f'Game {oldname} Not Found!')
            return

    def update(self):
        info, oldname = self.updatename()
        if not info:
            self.disable()
            messagebox.showerror('Error', f'Game {oldname} Not Found!')
            return
        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to update this game?')
        if answer:
            self.save(purpose='update', oldname=oldname)


class DeleteWindow(InsertWindow):
    def __init__(self, root, connection: MyConnection, text="Delete Games"):
        self.connection = connection
        self.root = root

        self.frame = LabelFrame(self.root, text=text, cnf=config_lbl_frame)
        self.e_name = Entry(self.frame, cnf=config_entry)
        self.btn_search = Button(self.frame, text="Search", cnf=config_btn, command=self.search)
        self.btn_delete = Button(self.frame, text="Delete", state='disabled', cnf=config_btn, command=self.delete)

        self.e_name.grid(row=1, column=1, cnf=grid_config)
        self.btn_search.grid(row=2, column=1, cnf=grid_config)
        self.btn_delete.grid(row=3, column=1, cnf=grid_config)
                 
    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)

    def updatename(self):
        name = self.e_name.get().strip()
        return self.connection.select(name), name

    def search(self):
        info, name = self.updatename()
        if info:
            messagebox.showinfo('Found', f'Game {name} was found')
            self.btn_delete.configure(state='normal')
        else:
            messagebox.showerror('Error', f'Game {name} was not found')
            self.btn_delete.configure(state='disabled')

    def delete(self):    
        info, name = self.updatename()
        if not info:
            messagebox.showerror('Error', f'Game {name} was not found')
            self.btn_delete.configure(state='disabled')
            return
        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to delete this game?')
        if answer:
            result = self.connection.delete(f'{name}')
            if result == 1:
                messagebox.showinfo('Done', 'The game was deleted')
            else:
                messagebox.showerror('Error', 'Something went wrong!')
        self.e_name.delete(0, END)
    

class Email:
    def __init__(self, root: Tk, game):
        self.root = root
        self.root.withdraw()
        self.game = game
        self.window = Toplevel(root)
        self.window.protocol('WM_DELETE_WINDOW', lambda: sys.exit(1))
        self.window.configure(bg=BG)
        self.window.title('Enter your email')
        self.window.resizable(False, False)
        self.lbl_email = Label(self.window, text="Enter your email:", cnf=config_lbl)
        self.e_email = Entry(self.window, cnf=config_entry)
        self.btn_back = Button(self.window, text="Back", cnf=config_btn, command=lambda: change_window(self.window, self.root))
        self.btn_sumbit = Button(self.window, text="Sumbit", cnf=config_btn, command=self.send_email)
        self.lbl_email.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.e_email.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.btn_back.grid(row=2, column=0, padx=10, pady=10)
        self.btn_sumbit.grid(row=2, column=1, padx=10, pady=10)

    def send_email(self):
        receiver_email = self.e_email.get().strip()
        sender_email = 'safarzdeh.mani87@gmail.com'
        sender_password = 'yttyncywuiehzvzs'
        message = f'Hi There!\nYou have successfully bought the game {self.game}.\nEnjoy your time.'
        smtp_server = 'smtp.gmail.com'
        port = 465

        if not re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", receiver_email, re.IGNORECASE):
            messagebox.showerror('Error', 'Incorrect format for email')
            return
        
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(smtp_server, port=port, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message)
        except smtplib.SMTPException:
            messagebox.showerror('Error', 'Something went wrong')
            return
        
        messagebox.showinfo('Success', 'You have bought this game\nEnjoy your time')
        change_window(self.window, self.root)
        

        