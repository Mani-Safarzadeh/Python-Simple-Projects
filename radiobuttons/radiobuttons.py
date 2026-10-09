from tkinter import *
from tkinter import messagebox
from json import load

def main():
    global root
    root = Tk()
    root.title("Quiz")
    a1 = IntVar(root)
    a2 = IntVar(root)
    a1.set(0)
    a2.set(0)

    lbl_q1 = Label(root, text="6*8?", font=('', 14))
    rb_q11 = Radiobutton(root, text='30', value=1, variable=a1, font=('', 14))
    rb_q12 = Radiobutton(root, text='60', value=2, variable=a1, font=('', 14))
    rb_q13 = Radiobutton(root, text='48', value=3, variable=a1, font=('', 14))
    rb_q14 = Radiobutton(root, text='90', value=4, variable=a1, font=('', 14))
    lbl_q1.grid(row=0, column=0, padx=5, pady=10, columnspan=4, sticky='w')
    rb_q11.grid(row=1, column=0, padx=5, pady=10, sticky='w')
    rb_q12.grid(row=1, column=1, padx=5, pady=10, sticky='w')
    rb_q13.grid(row=1, column=2, padx=5, pady=10, sticky='w')
    rb_q14.grid(row=1, column=3, padx=5, pady=10, sticky='w')

    lbl_q2 = Label(root, text="Capital of Iran? ", font=('', 14))
    rb_q21 = Radiobutton(root, text='Tehran', value=1, variable=a2, font=('', 14))
    rb_q22 = Radiobutton(root, text='Rasht', value=2, variable=a2, font=('', 14))
    rb_q23 = Radiobutton(root, text='Shiraz', value=3, variable=a2, font=('', 14))
    rb_q24 = Radiobutton(root, text='Yazd', value=4, variable=a2, font=('', 14))
    lbl_q2.grid(row=2, column=0, padx=5, pady=10, columnspan=4, sticky='w')
    rb_q21.grid(row=3, column=0, padx=5, pady=10, sticky='w')
    rb_q22.grid(row=3, column=1, padx=5, pady=10, sticky='w')
    rb_q23.grid(row=3, column=2, padx=5, pady=10, sticky='w')
    rb_q24.grid(row=3, column=3, padx=5, pady=10, sticky='w')

    btn_send =Button(root, text="Submit", command=lambda: send(a1, a2), font=("", 14))
    btn_send.grid(row=4, column=0, sticky='ew', padx=10, pady=10)

    mainloop()

def read():
    with open("answers.json", "r", encoding='utf8') as f:
        return load(f)

def send(*args: IntVar):
    answers = read()
    score = 0
    for i in range(len(args)):
        if args[i].get() == answers[i]:
            score += 5
        else:
            score -= 2
    messagebox.showinfo("Score", f"Your Score: {score}")

if __name__ == "__main__":
    main()