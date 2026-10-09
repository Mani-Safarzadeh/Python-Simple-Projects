from tkinter import *
from tkinter import messagebox, ttk
from configurations import *
from datetime import datetime
import pymysql

def change_window(current: Tk, target: Tk):
    current.withdraw()
    target.deiconify()

class MyConnection:
    def __init__(self, user='root', password='root'):
        self.db = pymysql.connect(host='127.0.0.1', user=user, password=password, charset='utf8')
        self.cursor = self.db.cursor()
        self.create_schema()
        self.create_table()

    def create_schema(self):
        query = "CREATE SCHEMA IF NOT EXISTS `musclize`;"
        self.cursor.execute(query)
        
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS `musclize`.`users` (
        `idusers` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `username` VARCHAR(20) NOT NULL,
        `password` VARCHAR(20) NOT NULL,
        PRIMARY KEY (`idusers`),
        UNIQUE INDEX `id_UNIQUE` (`idusers` ASC) VISIBLE,
        UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);
        """
        self.cursor.execute(query)
        query = """
        CREATE TABLE IF NOT EXISTS `musclize`.`history` (
        `idhistory` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `idusers` INT UNSIGNED NOT NULL,
        `date` VARCHAR(10) NOT NULL,
        `name` VARCHAR(45) NOT NULL,
        `weight` SMALLINT(4) UNSIGNED NOT NULL,
        `sets` SMALLINT(4) UNSIGNED NOT NULL,
        `reps` SMALLINT(4) UNSIGNED NOT NULL,
        PRIMARY KEY (`idhistory`),
        UNIQUE INDEX `idhistory_UNIQUE` (`idhistory` ASC) VISIBLE);
        """
        self.cursor.execute(query)

    def add_user(self, username, password):
        query = "INSERT INTO `musclize`.`users` (`username`, `password`) VALUES (%s, %s)"
        values = (username, password,)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error
        
    def find_user(self, username, password):
        query = "SELECT * FROM `musclize`.`users` WHERE `username`=%s AND `password`=%s"
        values = (username, password)
        self.cursor.execute(query, values)
        return self.cursor.fetchone()
    
    def get_id(self, username):
        query = "SELECT `idusers` FROM `musclize`.`users` WHERE `username`=%s"
        values = (username)
        self.cursor.execute(query, values)
        return self.cursor.fetchone()[0]

    def add_workout(self, iduser, date, name, weight, sets, reps):
        query = "INSERT INTO `musclize`.`history` (`idusers`, `date`, `name`, `weight`, `sets`, `reps`) VALUES (%s, %s, %s, %s, %s, %s);"
        values = (iduser, date, name, weight, sets, reps)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error

    def find_workout(self, iduser, date, name, max_weight, min_weight):
        query = "SELECT * FROM `musclize`.`history` WHERE 1=1"
        conditions = []
        values = []
        if iduser:
            conditions.append("`idusers`=%s")
            values.append(iduser)
        if date:
            conditions.append("`date` LIKE %s")
            values.append(f"%{date}%")
        if name:
            conditions.append("`name` LIKE %s")
            values.append(f"%{name}%")
        if max_weight:
            conditions.append("`weight` <= %s")
            values.append(max_weight)
        if min_weight:
            conditions.append("`weight` >= %s")
            values.append(min_weight)
        if conditions:
            query += " AND " + " AND ".join(conditions)
            self.cursor.execute(query, tuple(values))
            return self.cursor.fetchall()
        else:
            query = "SELECT * FROM `musclize`.`history` WHERE `idusers`= %s"
            values = (iduser)
            self.cursor.execute(query, values)
            return self.cursor.fetchall()

    def delete_workout(self, date, name):
        query = "DELETE FROM `musclize`.`history` WHERE `date` LIKE %s AND `name` LIKE %s;"
        values = (date, name)
        result = self.cursor.execute(query, values)
        self.db.commit()
        return result

    def edit_workout(self, olddate, oldname, name, weight, sets, reps):
        query = "UPDATE `musclize`.`history` SET `name`=%s, `weight`=%s, `sets`=%s, `reps`=%s WHERE `date`=%s AND `name`=%s;"
        values = (name, weight, sets, reps, olddate, oldname)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error

class Login:
    def __init__(self, connection: MyConnection):
        self.connection = connection
        self.login_window = Tk()
        self.login_window.resizable(False, False)
        self.login_window.title(TITLE)

        self.frame1 = LabelFrame(self.login_window, text='Create an accout', cnf=lbl_frm_cnf)
        self.frame2 = LabelFrame(self.login_window, text='Sign in with an account', cnf=lbl_frm_cnf)
        self.e_user_1 = Entry(self.frame1, cnf=entry_cnf, width=18)
        self.e_pass_1 = Entry(self.frame1, cnf=entry_cnf, width=18)
        self.e_user_2 = Entry(self.frame2, cnf=entry_cnf, width=18)
        self.e_pass_2 = Entry(self.frame2, cnf=entry_cnf, width=18)
        self.btn_sumbit_1 = Button(self.frame1, text='Create', width=8, cnf=btn_cnf, command=self.create_account)
        self.btn_sumbit_2 = Button(self.frame2, text='Log in', width=8, cnf=btn_cnf, command=self.login)
        
        self.frame1.grid(cnf=grid_cnf, row=0, column=0)
        self.frame2.grid(cnf=grid_cnf, row=0, column=1)
        self.e_user_1.grid(cnf=grid_cnf, row=0, column=0)
        self.e_pass_1.grid(cnf=grid_cnf, row=1, column=0)
        self.e_user_2.grid(cnf=grid_cnf, row=0, column=0)
        self.e_pass_2.grid(cnf=grid_cnf, row=1, column=0)
        self.btn_sumbit_1.grid(cnf=grid_cnf, row=2, column=0)
        self.btn_sumbit_2.grid(cnf=grid_cnf, row=2, column=0)
                
    def create_account(self):
        username = self.e_user_1.get().strip()
        password = self.e_pass_1.get().strip()

        if username == '' or password == '':
            messagebox.showerror('Error', 'Do not leave the entries empty')
            return
        if len(username) > 20 or len(password) > 20:
            messagebox.showerror('Error', 'Too many characters for he entries')
            return
        if len(password) < 8:
            messagebox.showerror('Error', 'Password is too short')
            return
        
        result = self.connection.add_user(username, password)
        if result == 0:
            messagebox.showinfo('Success', 'Your new account has been created successfully')
            self.login_window.destroy()
            iduser = self.connection.get_id(username)
            MainMenu(iduser, self.connection)
            return
        messagebox.showerror('Error', result)

    def login(self):
        username = self.e_user_2.get().strip()
        password = self.e_pass_2.get().strip()
        
        result = self.connection.find_user(username, password)
        if result:
            messagebox.showinfo('Success', 'You have logged in to your account successfully')
            self.login_window.destroy()
            iduser = self.connection.get_id(username)
            MainMenu(iduser, self.connection)
            return
        messagebox.showerror('Error', 'No accounts were found with these info')

class MainMenu:
    def __init__(self, iduser, connection: MyConnection):
        self.connection = connection
        self.iduser = iduser

        self.main_menu = Tk()
        self.main_menu.resizable(False, False)
        self.main_menu.title(TITLE)

        self.new_workout = Toplevel(self.main_menu)
        self.new_workout.withdraw()
        self.new_workout.protocol('WM_DELETE_WINDOW', self.main_menu.destroy)
        self.new_workout.resizable(False, False)
        self.new_workout.title(TITLE)

        self.workout_history = Toplevel(self.main_menu)
        self.workout_history.withdraw()
        self.workout_history.protocol('WM_DELETE_WINDOW', self.main_menu.destroy)
        self.workout_history.resizable(False, False)
        self.workout_history.title(TITLE)

        NewWorkout(self.iduser, self.main_menu, self.new_workout, self.connection)
        WorkoutHistory(self.iduser, self.main_menu, self.workout_history, self.connection)

        self.btn_new_workout = Button(
            self.main_menu,
            text="New Workout",
            width=15,
            height=3,
            cnf=btn_cnf,
            command=lambda: change_window(self.main_menu, self.new_workout)
        )
        self.btn_workout_history = Button(
            self.main_menu,
            text="Workout History",
            width=15,
            height=3,
            cnf=btn_cnf,
            command=lambda: change_window(self.main_menu, self.workout_history)
        )
        self.btn_new_workout.grid(cnf=grid_cnf, row=0, column=0)
        self.btn_workout_history.grid(cnf=grid_cnf, row=0, column=1)

class NewWorkout:
    def __init__(self, isuser, main_menu: Tk, new_workout: Tk, connection: MyConnection):
        self.iduser = isuser
        self.main_menu = main_menu
        self.new_workout = new_workout
        self.connection = connection

        self.lbl_name = Label(self.new_workout, text='Exercise Name:', cnf=lbl_cnf)
        self.e_name = Entry(self.new_workout, cnf=entry_cnf)
        self.lbl_weight = Label(self.new_workout, text='Weight(kg):', cnf=lbl_cnf)
        self.e_weight = Entry(self.new_workout, cnf=entry_cnf)
        self.lbl_sets = Label(self.new_workout, text='Sets:', cnf=lbl_cnf)
        self.e_sets = Entry(self.new_workout, cnf=entry_cnf)
        self.lbl_reps = Label(self.new_workout, text='Reps:', cnf=lbl_cnf)
        self.e_reps = Entry(self.new_workout, cnf=entry_cnf)
        self.btn_back = Button(self.new_workout, text='Back', cnf=btn_cnf, command=lambda:change_window(self.new_workout, self.main_menu))
        self.btn_add = Button(self.new_workout, text='Add', cnf=btn_cnf, command=self.add_workout)

        self.lbl_name.grid(cnf=grid_cnf, row=0, column=0)
        self.e_name.grid(cnf=grid_cnf, row=0, column=1)
        self.lbl_weight.grid(cnf=grid_cnf, row=1, column=0)
        self.lbl_sets.grid(cnf=grid_cnf, row=2, column=0)
        self.lbl_reps.grid(cnf=grid_cnf, row=3, column=0)
        self.e_weight.grid(cnf=grid_cnf, row=1, column=1)
        self.e_sets.grid(cnf=grid_cnf, row=2, column=1)
        self.e_reps.grid(cnf=grid_cnf, row=3, column=1)
        self.btn_back.grid(cnf=grid_cnf, row=4, column=0)
        self.btn_add.grid(cnf=grid_cnf, row=4, column=1)

    def add_workout(self):
        name = self.e_name.get().strip()
        weight = self.e_weight.get().strip()
        sets = self.e_sets.get().strip()
        reps = self.e_reps.get().strip()

        for i in [name, weight, sets, reps]:
            if i == '':
                messagebox.showerror('Error', 'Do not leave any fields empty')
                return
        for j in [weight, sets, reps]:
            if not j.isdigit():
                messagebox.showerror('Error', 'Incorrect format for the entries')
                return
            
        date = str(datetime.now())[0:10]
        result = self.connection.add_workout(self.iduser, date, name, weight, sets, reps)
        self.e_name.delete(0, END)
        self.e_weight.delete(0, END)
        self.e_sets.delete(0, END)
        self.e_reps.delete(0, END)
        if result:
            messagebox.showerror('Error', result)
            return
        messagebox.showinfo('Success', 'Workout was added, keep on hitting PRS')      

class WorkoutHistory:
    def __init__(self, iduser, main_menu: Tk, workout_history: Tk, connection: MyConnection):
        self.iduser = iduser
        self.main_menu = main_menu
        self.workout_history = workout_history
        self.connection = connection

        self.frame_treeview = LabelFrame(self.workout_history, text='Data', cnf=lbl_frm_cnf)
        self.frame_output  = LabelFrame(self.workout_history, text='Options', cnf=lbl_frm_cnf)
        self.frame_options = LabelFrame(self.workout_history, text='Search by ...', cnf=lbl_frm_cnf)
        self.frame_treeview.grid(cnf=grid_cnf, row=0, column=0)
        self.frame_output.grid(cnf=grid_cnf, row=1, column=0)
        self.frame_options.grid(cnf=grid_cnf, row=0, rowspan=2, column=1)

        self.tabel = ttk.Treeview(self.frame_treeview, selectmode='browse')
        self.verscrlbar = ttk.Scrollbar(self.frame_treeview, orient='vertical', command=self.tabel.yview)
        self.tabel.grid(row=1, column=1, columnspan=10)
        self.verscrlbar.grid(row=1, column=11, sticky='ns')
        self.tabel.configure(yscrollcommand=self.verscrlbar.set)

        self.tabel.bind('<Double-1>', self.on_double_click)

        columns = ('1', '2', '3' , '4' , '5')
        widths = (190, 210, 75, 75, 75)
        headings = ('Date', 'Workout Name', 'Weight', 'Sets', 'Reps')
        self.tabel['columns'] = columns
        self.tabel['show'] = 'headings'
        for column, width in zip(columns, widths):
            self.tabel.column(column, width=width, anchor='center')
        for column, heading in zip(columns, headings):
            self.tabel.heading(column, text=heading)

        self.btn_delete = Button(self.frame_output, text='Delete', width=9, state='disabled', cnf=btn_cnf, font=('Calibiri', 17), command=self.delete)
        self.btn_edit = Button(self.frame_output, text='Edit', width=9, state='disabled', cnf=btn_cnf, font=('Calibiri', 17), command=self.edit)
        Label(self.frame_output, text='Name:', cnf=lbl_cnf).grid(row=0, column=1)
        Label(self.frame_output, text='Weight:', cnf=lbl_cnf).grid(row=1, column=1)
        Label(self.frame_output, text='Sets:', cnf=lbl_cnf).grid(row=0, column=3)
        Label(self.frame_output, text='Reps:', cnf=lbl_cnf).grid(row=1, column=3)
        self.new_name = Entry(self.frame_output, cnf=entry_cnf, state='disabled', width=9)
        self.new_weight = Entry(self.frame_output, cnf=entry_cnf, state='disabled', width=9)
        self.new_sets = Entry(self.frame_output, cnf=entry_cnf, state='disabled', width=9)
        self.new_reps = Entry(self.frame_output, cnf=entry_cnf, state='disabled', width=9)

        self.btn_delete.grid(row=0, column=0, padx=3, pady=5) 
        self.btn_edit.grid(row=1, column=0, padx=3, pady=5)

        self.new_name.grid(row=0, column=2, padx=3, pady=5)
        self.new_weight.grid(row=1, column=2, padx=3, pady=5)
        self.new_sets.grid(row=0, column=4, padx=3, pady=5)
        self.new_reps.grid(row=1, column=4, padx=3, pady=5)

        Label(self.frame_options, text='Year:', cnf=lbl_cnf).grid(cnf=grid_cnf, row=0, column=0)
        Label(self.frame_options, text='Month:', cnf=lbl_cnf).grid(cnf=grid_cnf, row=1, column=0)
        Label(self.frame_options, text='Day:', cnf=lbl_cnf).grid(cnf=grid_cnf, row=2, column=0)
        Label(self.frame_options, text='Workout name:', cnf=lbl_cnf).grid(cnf=grid_cnf, row=3, column=0)
        Label(self.frame_options, text='Max Weight:', cnf=lbl_cnf).grid(cnf=grid_cnf, row=4, column=0)
        Label(self.frame_options, text='Min weight:', cnf=lbl_cnf).grid(cnf=grid_cnf, row=5, column=0)

        self.e_year = Entry(self.frame_options, cnf=entry_cnf) 
        self.e_month = Entry(self.frame_options, cnf=entry_cnf)
        self.e_day = Entry(self.frame_options, cnf=entry_cnf)
        self.e_name = Entry(self.frame_options, cnf=entry_cnf)
        self.e_max_weight = Entry(self.frame_options, cnf=entry_cnf)
        self.e_min_weight = Entry(self.frame_options, cnf=entry_cnf)
        self.btn_back = Button(self.frame_options, text='Back', cnf=btn_cnf, command=lambda: change_window(self.workout_history, self.main_menu))
        self.btn_search = Button(self.frame_options, text='Search', cnf=btn_cnf, command=self.search)

        self.e_year.grid(cnf=grid_cnf, row=0, column=1)
        self.e_month.grid(cnf=grid_cnf, row=1, column=1)
        self.e_day.grid(cnf=grid_cnf, row=2, column=1)
        self.e_name.grid(cnf=grid_cnf, row=3, column=1)
        self.e_max_weight.grid(cnf=grid_cnf, row=4, column=1)
        self.e_min_weight.grid(cnf=grid_cnf, row=5, column=1)
        self.btn_back.grid(cnf=grid_cnf, row=6, column=0)
        self.btn_search.grid(cnf=grid_cnf, row=6, column=1)

    def on_double_click(self, event):
        self.btn_delete.configure(state='normal')
        self.btn_edit.configure(state='normal')
        self.new_name.configure(state='normal')
        self.new_weight.configure(state='normal')
        self.new_sets.configure(state='normal')
        self.new_reps.configure(state='normal')
        item = self.tabel.selection()[0]
        self.asks_date = self.tabel.item(item, 'values')[0]
        self.asks_name = self.tabel.item(item, 'values')[1]
    
    def delete(self):
        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to delete this record?')
        if answer:
            result = self.connection.delete_workout(self.asks_date, self.asks_name)
            if result == 1:
                messagebox.showinfo('Done', 'The record was deleted')
            else:
                messagebox.showerror('Error', 'Something went wrong!')

    def edit(self):
        name = self.new_name.get().strip()
        weight = self.new_weight.get().strip()
        sets = self.new_sets.get().strip()
        reps = self.new_reps.get().strip()
        result = self.connection.edit_workout(self.asks_date, self.asks_name ,name, weight, sets, reps)
        if result == 0:
            messagebox.showinfo('Success', 'Your record has been updated')
            return
        else:
            messagebox.showerror('Error', result)

    def search(self):
        date = None
        year = self.e_year.get().strip()
        month = self.e_month.get().strip()
        day = self.e_day.get().strip()
        if year != '' and month != '' and day != '':
            date = f"{year}-{int(month):02d}-{int(day):02d}"
        history = self.connection.find_workout(
            self.iduser,
            date,
            self.e_name.get().strip(),
            self.e_max_weight.get().strip(),
            self.e_min_weight.get().strip()
        )
        self.tabel.delete(*self.tabel.get_children())
        for item in history:
            self.tabel.insert('', 'end', text=item[0], values=(item[2:7]))