from widgets import *

class App:
    def __init__(self):
        self.connection = MyConnection()
        self.connection.create_schema()
        self.connection.create_table()

        self.root = Tk()
        self.search_window = Toplevel(self.root)
        self.login_window = Toplevel(self.root)
        self.management_window = Toplevel(self.root)
        self.insert_window = Toplevel(self.management_window)
        self.update_window = Toplevel(self.management_window)
        self.delete_window = Toplevel(self.management_window)

        self.root.configure(bg=BG)
        self.search_window.configure(bg=BG)
        self.login_window.configure(bg=BG)
        self.management_window.configure(bg=BG)
        self.insert_window.configure(bg=BG)
        self.update_window.configure(bg=BG)
        self.delete_window.configure(bg=BG)

        self.root.title('App')
        self.search_window.title('Search game')
        self.login_window.title('Login or register')
        self.management_window.title('Management')
        self.insert_window.title('Insert game')
        self.update_window.title('Update game')
        self.delete_window.title('Delete game')

        self.root.geometry('500x300')
        self.search_window.geometry('1440x1080')
        self.management_window.geometry('800x300')
        self.insert_window.geometry('800x600')
        self.update_window.geometry('1000x600')
        self.delete_window.geometry('400x300')

        self.login_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.search_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.management_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.insert_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.update_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.delete_window.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.login_window.withdraw()
        self.search_window.withdraw()
        self.management_window.withdraw()
        self.insert_window.withdraw()
        self.update_window.withdraw()
        self.delete_window.withdraw()

        # ----------------- Root window widgets -----------------
        self.btn_management = Button(self.root, text='Management', cnf=config_btn, command=self.go_to_management)
        self.btn_search = Button(self.root, text="Search", cnf=config_btn, command=lambda: change_window(self.root, self.search_window))        
        self.btn_management.pack(cnf=config_btn_root_pack)
        self.btn_search.pack(cnf=config_btn_root_pack)

        # ----------------- Search window widgets -----------------
        search_window = SearchWindow(self.search_window, self.connection)
        self.btn_back_search = Button(self.search_window, cnf=config_btn, text="Back", command=lambda: change_window(self.search_window, self.root))
        self.btn_back_search.grid(row=7, rowspan=2, sticky='news', column=4)

        # ----------------- Login window widgets -----------------
        self.login_window.resizable(False, False)
        login_window = LoginOrRegister(self.login_window, self.management_window, self.connection)
        self.btn_back_login = Button(self.login_window, text='Back', cnf=config_btn, command=lambda:   change_window(self.login_window, self.root))
        self.btn_back_login.grid(row=1, column=0, padx=10, pady=10)
        

        # ----------------- Management window widgets -----------------
        self.btn_insert = Button(self.management_window, text="Insert Games", cnf=config_btn, command=lambda:  change_window(self.management_window, self.insert_window))
        self.btn_update = Button(self.management_window, text="Update Games", cnf=config_btn, command=lambda:  change_window(self.management_window, self.update_window))
        self.btn_delete = Button(self.management_window, text="Delete Games", cnf=config_btn, command=lambda:  change_window(self.management_window, self.delete_window))
        self.btn_back_management = Button(self.management_window, text="Back", cnf=config_btn, command=lambda: change_window(self.management_window, self.root))

        self.btn_insert.pack(cnf=config_btn_root_pack)
        self.btn_update.pack(cnf=config_btn_root_pack)
        self.btn_delete.pack(cnf=config_btn_root_pack)
        self.btn_back_management.pack(cnf=config_btn_root_pack)
        

        # ----------------- Insert window widgets -----------------
        insert_window = InsertWindow(self.insert_window, self.connection)
        insert_window.pack()
        self.btn_back_insert = Button(self.insert_window, text="Back", cnf=config_btn, command=lambda: change_window(self.insert_window, self.management_window))
        self.btn_back_insert.pack()

        # ----------------- Update window widgets -----------------
        update_winodw = UpdateWindow(self.update_window, self.connection)
        update_winodw.grid(row=0, column=0, padx=50, pady=20)
        self.btn_back_update = Button(self.update_window, text="Back", cnf=config_btn, command=lambda: change_window(self.update_window, self.management_window))
        self.btn_back_update.grid(row=1, column=0, padx=50)

        # ----------------- Delete window widgets -----------------
        delete_window = DeleteWindow(self.delete_window, self.connection)
        delete_window.pack()
        self.btn_back_delete = Button(self.delete_window, text="Back", cnf=config_btn, command=lambda: change_window(self.delete_window, self.management_window))
        self.btn_back_delete.pack()

        # runs the app
        self.root.mainloop()
        
        # closing the database and the program
        save({'is_logged_in': False})
        self.connection.close()
        sys.exit(0)
       
    def go_to_management(self):
        info = load()
        if not info['is_logged_in']:
            change_window(self.root, self.login_window)
        else:
            change_window(self.root, self.management_window)

if __name__ == '__main__':
    App()

