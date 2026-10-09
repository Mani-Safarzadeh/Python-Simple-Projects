from tkinter import *
from utils import *
from settings import *
from cell import Cell
import sys


class Minesweeper:
    def __init__(self):
        # root
        self.root = Tk()
        self.root.title("MineSweeper")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg="#111")
        self.root.resizable(False, False)
        images = self.get_images()
        info = load()

        # Widgets definitions
        self.frame_top = Frame(self.root, bg="#222", width=width_percentage(100), height=height_percentage(20))
        self.frame_left = Frame(self.root, bg="#111", width=width_percentage(40), height=height_percentage(80))
        self.frame_right = Frame(self.root, bg="#ddd", width=width_percentage(60), height=height_percentage(20))
        self.lbl_time = Label(self.frame_top, font=("Helvetica", 24, "bold"), text="Time: 00:00", fg="#fff", bg="#222")
        self.lbl_flags = Label(self.frame_top, font=("Helvetica", 24, "bold"), text=f"Flags: {FLAGS_COUNT}", fg="#fff", bg="#222")
        self.btn_exit = Button(self.frame_left, font=("Helvetica", 24), text="Exit", fg="#fff", bg="#000", width=8, command=lambda: sys.exit(1))
        self.btn_restart = Button(self.frame_left, font=("Helvetica", 24), text="Restart", fg="#fff", bg="#000", width=8, command=lambda: Cell.restart(cell))
        self.lbl_games_won = Label(self.frame_left, font=("Helvetica", 20), text=f"Games won:\n{info['games won']}", fg="#fff", bg="#111")
        self.lbl_high_score = Label(self.frame_left, font=("Helvetica", 20), text=f"High Score:\n{info['high score']}", fg="#fff", bg="#111")
        
        # All cells
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                cell = Cell(x, y, images, self.lbl_time, self.lbl_flags, self.lbl_games_won, self.lbl_high_score)
                cell.create_btn_object(self.frame_right)
                cell.cell_btn_object.grid(column=x, row=y)
        Cell.random_mines()

        # Place Layout
        self.frame_top.place(x=0, y=0)
        self.frame_left.place(x=0, y=100)
        self.frame_right.place(x=200, y=100)
        self.lbl_time.place(x=100, y=50)
        self.lbl_flags.place(x=400, y=50)
        self.btn_exit.place(x=25, y=300)
        self.btn_restart.place(x=25, y=200)
        self.lbl_games_won.place(x=25, y=90)
        self.lbl_high_score.place(x=26, y=10)

        mainloop()

    @staticmethod
    def get_images():
        not_clicked = get_image("Images/not-clicked.png")
        clicked = get_image("Images/clicked.png")
        one = get_image("Images/1.jpg")
        two = get_image("Images/2.jpg")
        three = get_image("Images/3.jpg")
        four = get_image("Images/4.jpg")
        five = get_image("Images/5.jpg")
        six = get_image("Images/6.png")
        seven = get_image("Images/7.jpg")
        eight = get_image("Images/8.png")
        flag = get_image("Images/flag.jpg")
        mine_blue = get_image("Images/mine-blue.png")
        mine_green = get_image("Images/mine-green.png")
        mine_orange = get_image("Images/mine-orange.png")
        return [not_clicked, clicked, one, two, three, four, five, six, seven, eight, flag, mine_blue, mine_green, mine_orange]


if __name__ == "__main__":
    Minesweeper()
