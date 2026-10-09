# importing libraries
from tkinter import *
from tkinter import messagebox
from threading import Thread
from time import sleep
import os

# variables
is_run_1 = False    
is_run_2 = False
time_1 = 0
time_2 = 0

def is_valid():
    try:
        int(minute_spinbox_1.get())
        int(minute_spinbox_2.get())
        int(hour_spinbox_1.get())
        int(hour_spinbox_2.get())
        return True
    except ValueError:
        return False
    
def set_time(n):
    global time_1, time_2
    if is_valid():
        if n==1:
            hour = hour_spinbox_1.get()
            minute = minute_spinbox_1.get()
            time_1 = (hour * 3600) + (minute * 60)
            lbl_time_1.config(text=f"{hour:>02}:{minute:>02}:00")
        elif n==2:
            hour = hour_spinbox_2.get()
            minute = minute_spinbox_2.get()
            time_2 = (hour * 3600) + (minute * 60)
            lbl_time_2.config(text=f"{hour:>02}:{minute:>02}:00")
    else:
        return

def reset(n):
    global time_1, time_2, is_run_1, is_run_2
    if n==1:
        time_1 = 0
        is_run_1 = False
        hour_spinbox_1.config(state=NORMAL)
        minute_spinbox_1.config(state=NORMAL)
        hour_spinbox_1.delete(0, END)
        minute_spinbox_1.delete(0, END)
        hour_spinbox_1.insert(0, '0')
        minute_spinbox_1.insert(0, '0')
        lbl_time_1.config(text="00:00:00")
        btn_start_1.config(text='Start')
    elif n==2:
        time_2 = 0
        is_run_2 = False
        hour_spinbox_2.config(state=NORMAL)
        minute_spinbox_2.config(state=NORMAL)
        hour_spinbox_2.delete(0, END)
        minute_spinbox_2.delete(0, END)
        hour_spinbox_2.insert(0, '0')
        minute_spinbox_2.insert(0, '0')
        lbl_time_2.config(text="00:00:00")
        btn_start_2.config(text='Start')
def run(n):
    if is_valid():
        if n==1:
            hour = int(hour_spinbox_1.get())
            minute = int(minute_spinbox_1.get())
            time_1 = (hour * 3600) + (minute * 60)
            while time_1 > 0 and is_run_1:
                time_1 -= 1
                hour = time_1 // 3600
                minute = (time_1 - (hour * 3600)) // 60
                second = (time_1 - (hour * 3600) - (minute * 60))
                lbl_time_1.config(text=f"{hour:02}:{minute:02}:{second:02}")
                sleep(1)
                if time_1 == 0:
                    messagebox.showinfo("Alert", "Time to use your drug")
        elif n==2:
            hour = int(hour_spinbox_2.get())
            minute = int(minute_spinbox_2.get())
            time_2 = (hour * 3600) + (minute * 60)
            while time_2 > 0 and is_run_2:
                time_2 -= 1
                hour = time_2 // 3600
                minute = (time_2 - (hour * 3600)) // 60
                second = (time_2 - (hour * 3600) - (minute * 60))
                lbl_time_2.config(text=f"{hour:02}:{minute:02}:{second:02}")
                sleep(1)
                if time_2 == 0:
                    messagebox.showinfo("Alert", "Time to use your drug")
    else:
        return

def start(n):
    global is_run_1, is_run_2
    if n==1:
        is_run_1 = not is_run_1
        if btn_start_1['text'] =='Start':
            btn_start_1.config(text='Pause')
            minute_spinbox_1.config(state=DISABLED)
            hour_spinbox_1.config(state=DISABLED)
        else:
            btn_start_1.config(text='Start')
            minute_spinbox_1.config(state=NORMAL)
            hour_spinbox_1.config(state=NORMAL)
    elif n==2:
        is_run_2 = not is_run_2
        if btn_start_2['text'] =='Start':
            btn_start_2.config(text='Pause')
            minute_spinbox_2.config(state=DISABLED)
            hour_spinbox_2.config(state=DISABLED)
        else:
            btn_start_2.config(text='Start')
            minute_spinbox_2.config(state=NORMAL)
            hour_spinbox_2.config(state=NORMAL)
    Thread(target=run, args=(n,), daemon=True).start()


# main page
root = Tk()
root.title("Drugs")

# label frames
lbl_frame_1 = LabelFrame(root, text="Amoxicilin", font=("", 16))
lbl_frame_2 = LabelFrame(root, text="Adult Cold", font=("", 16))

# put the frames on the screen
lbl_frame_1.grid(row=0, column=0)
lbl_frame_2.grid(row=0, column=1)

# timers
lbl_time_1 = Label(lbl_frame_1, text="00:00:00", font=("", 30))
lbl_time_2 = Label(lbl_frame_2, text="00:00:00", font=("", 30))

# the boxes for setting the time
hour_spinbox_1 = Spinbox(lbl_frame_1, from_=0, to=23, width=3, font=("", 24), command=lambda: set_time(1))
hour_spinbox_2 = Spinbox(lbl_frame_2, from_=0, to=23, width=3, font=("", 24), command=lambda: set_time(2))
minute_spinbox_1 = Spinbox(lbl_frame_1, from_=0, to=59, width=3, font=("", 24), command=lambda:set_time(1))
minute_spinbox_2 = Spinbox(lbl_frame_2, from_=0, to=59, width=3, font=("", 24), command=lambda: set_time(2))

# buttons for starting the timer and reseting the timer
btn_start_1 = Button(lbl_frame_1, text="Start", font=("", 24), command=lambda: start(1))
btn_start_2 = Button(lbl_frame_2, text="Start", font=("", 24), command=lambda: start(2))
btn_reset_1 = Button(lbl_frame_1, text="Reset", font=("", 24), command=lambda: reset(1))
btn_reset_2 = Button(lbl_frame_2, text="Reset", font=("", 24), command=lambda: reset(2))

# put the elements on the screen 
lbl_time_1.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
lbl_time_2.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

hour_spinbox_1.grid(row=1, column=0, padx=20, pady=10)
hour_spinbox_2.grid(row=1, column=0, padx=20, pady=10)
minute_spinbox_1.grid(row=1, column=1, padx=20, pady=10)
minute_spinbox_2.grid(row=1, column=1, padx=20, pady=10)

btn_start_1.grid(row=2, column=0, padx=20, pady=10, sticky="news")
btn_start_2.grid(row=2, column=0, padx=20, pady=10, sticky="news")
btn_reset_1.grid(row=2, column=1, padx=20, pady=10, sticky="news")
btn_reset_2.grid(row=2, column=1, padx=20, pady=10, sticky="news")

# Run the application
mainloop()

# Clearing the Terminal
os.system("clear") 