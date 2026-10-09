from tkinter import *
from threading import Thread
from time import sleep

time_1 = 0
time_2 = 0
is_run_1 = False
is_run_2 = False

def reset(n):
    global time_1, time_2, is_run_1, is_run_2
    if n == 1:
        time_1 = 0
        lbl_1.config(text=string_to_time(time_1))
        is_run_1 = False
        start_1.config(text="Start")
    elif n == 2:
        time_2 = 0
        lbl_2.config(text=string_to_time(time_2))
        is_run_2 = False
        start_2.config(text="Start")

def string_to_time(time):
    mili_second = time % 100
    time = time // 100
    hour = time // 3600
    minute = time // 60 - (hour * 60)
    second = time % 60
    return f"{hour:02}:{minute:02}:{second:02}.{mili_second:02}"

def start__(n):
    Thread(target=run, args=(n,)).start()

def run(n):
    global is_run_1, is_run_2, time_1, time_2

    if n==1:
        is_run_1 = not is_run_1
        if is_run_1 == True:
            start_1.config(text="Pause")
            start_1.config(state=DISABLED)
        else:
            start_1.config(text="Start")
        while is_run_1:
            time_1 += 1
            sleep(0.01)
            start_1.config(state=NORMAL)
            lbl_1.config(text=string_to_time(time_1))
            lbl_1.update()
    elif n ==2:
        is_run_2 = not is_run_2
        if is_run_2 == True:
            start_2.config(text="Pause")
            start_2.config(state=DISABLED)
        else:
            start_2.config(text="Start")
        while is_run_2:
            time_2 += 1
            sleep(0.01)
            start_2.config(state=NORMAL)
            lbl_2.config(text=string_to_time(time_2))
            lbl_2.update()


def main():
    root = Tk()
    root.title("StopWatch")

    # main elements
    global  lbl_1, lbl_2, start_1, start_2, reset_1, reset_2
    start_1 = Button(root, text="Start", font=('', 20), borderwidth=0, activebackground='#dedee3', command=lambda: start__(1))
    start_2 = Button(root, text="Start", font=('', 20), borderwidth=0, activebackground='#dedee3', command=lambda: start__(2))
    lbl_1 = Label(root, text="00:00:00.00", font=('', 20), borderwidth=0, activebackground='#dedee3')
    lbl_2 = Label(root, text="00:00:00.00", font=('', 20), borderwidth=0, activebackground='#dedee3')
    reset_1 = Button(root, text="reset", font=('', 20), borderwidth=0, activebackground='#dedee3', command=lambda: reset(1))
    reset_2 = Button(root, text="reset", font=('', 20), borderwidth=0, activebackground='#dedee3', command=lambda: reset(2))

    # put the elements on the screen
    start_1.grid(row=0, column=0, ipadx=20, ipady=10, sticky='news')
    start_2.grid(row=1, column=0, ipadx=20, ipady=10, sticky='news')
    lbl_1.grid(row=0, column=1, ipadx=20, ipady=10, sticky='news')
    lbl_2.grid(row=1, column=1, ipadx=20, ipady=10, sticky='news')
    reset_1.grid(row=0, column=2, ipadx=20, ipady=20, sticky='news')
    reset_2.grid(row=1, column=2, ipadx=20, ipady=20, sticky='news')

    mainloop()

if __name__ == "__main__":
    main()