from tkinter import *
from time import sleep
from threading import Thread
from random import choice

class TypeSpeedGUI:
    def __init__(self) -> None:
        # Root
        self.root = Tk()
        self.root.title("Typing speed application")
        self.root.geometry("800x600")
        # Frame
        self.frame = Frame(self.root)
        self.frame.pack(expand=True)
        # File and sentences
        self.texts = open("texts.txt", "r", encoding='utf8').read().split("\n")
        # Lable and button
        self.sample_label = Label(self.frame, text=choice(self.texts), font=("Helvetica", 18))
        self.input_entry = Entry(self.frame, width=40, font=("Helvetica", 24))
        self.speed_label = Label(self.frame, text="Speed:\n0.00 CPS\n0.00 CPM", font=("Helvetica", 18))
        self.reset_btn = Button(self.frame, text="Reset", font=("", 18), command=self.reset)
        # Binding
        self.input_entry.bind("<KeyPress>", self.start)
        # Put the elements on the screen
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.reset_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        # Variables
        self.counter = 0
        self.running = False
        # Mainloop
        self.root.mainloop()
        
    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                Thread(target=self.time_thread, daemon=False).start()
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg='red')
        else:
            self.input_entry.config(fg='black')
        if self.input_entry.get() == self.sample_label.cget('text')[0:-1]:
            self.running = False
            self.input_entry.config(fg='green')

    def time_thread(self):
        while self.running:
            sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed_label.config(text=f"Speed:\n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")

    def reset(self):
        self.running = False
        self.speed_label.config(text="Speed:\n0.00 CPS\n0.00 CPM")
        self.sample_label.config(text=choice(self.texts))
        self.input_entry.delete(0, END)


TypeSpeedGUI()