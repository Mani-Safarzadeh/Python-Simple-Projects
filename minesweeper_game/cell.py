from settings import *
from tkinter import messagebox, Button
from collections import deque
from threading import Thread
# from playsound import playsound
import utils
import random
import time
import sys

class Cell:
    is_running= False
    is_first_click = True
    flags_count = FLAGS_COUNT
    total_time = 0
    all_cells = []
    def __init__(self, x, y, images, lbl_time, lbl_flags, lbl_game_won, lbl_high_score):
        self.x = x
        self.y = y
        self.images = images
        self.lbl_time = lbl_time
        self.lbl_flags = lbl_flags
        self.lbl_game_won = lbl_game_won
        self.lbl_high_score = lbl_high_score
        self.is_mine = False
        self.is_flag = False
        self.is_filled = False
        self.cell_btn_object = None
        Cell.all_cells.append(self)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
    
    def create_btn_object(self, location):
        btn = Button(location, image=self.images[0], relief='flat')
        btn.bind("<ButtonRelease-1>", lambda e: self.left_click_action())
        btn.bind("<Button-3>", lambda e: self.right_click_action())
        self.cell_btn_object = btn

    def left_click_action(self):
        Cell.is_running = True
        if Cell.flags_count == 0 and len([cell for cell in Cell.all_cells if cell.is_filled]) == 64:
            self.update_scores()
            # Thread(target=playsound, args=("Sounds/you_won.mp3",), daemon=True).start()
            self.show_messagebox("You won", "You won\nDo you want to play again?")
            return
        if Cell.is_first_click:
            self.first_click()
            Thread(target=self.run, daemon=True).start()
            return
        if self.is_mine:
            self.show_mines()
            # Thread(target=playsound, args=("Sounds/game_over.mp3",), daemon=True).start()
            self.show_messagebox("Game over", "Your lost\nDo you want to play again?")
            return
        self.show_cell()

    def right_click_action(self):
        if not self.is_filled or self.is_flag:
            if not self.is_flag and Cell.flags_count > 0:
                self.cell_btn_object.configure(image=self.images[10])
                Cell.flags_count -= 1
                self.is_filled = True
                self.is_flag = True
            elif self.is_flag:
                self.cell_btn_object.configure(image=self.images[0])
                Cell.flags_count += 1
                self.is_flag = False
                self.is_filled = False
            self.lbl_flags.configure(text=f"Flags: {Cell.flags_count}")
            return

    def first_click(self):
        for cell in Cell.all_cells:
            if cell.surrounded_cells_mines_length == 0 and not cell.is_mine:
                cell.open_empty_cells()

    def show_cell(self): 
        if self.surrounded_cells_mines_length == 0:
            self.cell_btn_object.configure(image=self.images[1])
        elif self.surrounded_cells_mines_length == 1:
            self.cell_btn_object.configure(image=self.images[2])
        elif self.surrounded_cells_mines_length == 2:
            self.cell_btn_object.configure(image=self.images[3])
        elif self.surrounded_cells_mines_length == 3:
            self.cell_btn_object.configure(image=self.images[4])
        elif self.surrounded_cells_mines_length == 4:
            self.cell_btn_object.configure(image=self.images[5])
        elif self.surrounded_cells_mines_length == 5:
            self.cell_btn_object.configure(image=self.images[6])
        elif self.surrounded_cells_mines_length == 6:
            self.cell_btn_object.configure(image=self.images[7])
        elif self.surrounded_cells_mines_length == 7:
            self.cell_btn_object.configure(image=self.images[8])
        elif self.surrounded_cells_mines_length == 8:
            self.cell_btn_object.configure(image=self.images[9])
        self.is_filled = True

    def show_mines(self):
        for cell in Cell.all_cells:
            if cell.is_mine: 
                cell.cell_btn_object.configure(image=random.choice([self.images[11], self.images[12], self.images[13]]))

    def open_empty_cells(self):
        queue = deque([self])
        visited = set()

        while queue:
            cell = queue.popleft()
            cell.show_cell()
            cell.is_filled = True

            if cell.surrounded_cells_mines_length == 0:
                for adjacent_cell in cell.surrounded_cells:
                    if adjacent_cell not in visited and not adjacent_cell.is_flag:
                        queue.append(adjacent_cell)
                        visited.add(adjacent_cell)
        Cell.is_first_click = False

    def restart(self):
        for cell in Cell.all_cells: 
            cell.is_mine = False
            cell.is_flag = False
            cell.is_filled = False
            cell.cell_btn_object.configure(image=self.images[0])
        Cell.is_running= False
        Cell.is_first_click = True
        Cell.total_time = 0
        Cell.flags_count = FLAGS_COUNT
        self.lbl_flags.configure(text=f"Flags: {Cell.flags_count}")
        self.lbl_time.configure(text="Time: 00:00")
        self.random_mines()
        for cell in Cell.all_cells:
            cell.cell_btn_object.configure(state="disabled")
        time.sleep(1)
        for cell in Cell.all_cells:
            cell.cell_btn_object.configure(state="normal")

    def run(self):
        while Cell.is_running:
            Cell.total_time += 1
            minute = Cell.total_time // 60
            second = Cell.total_time % 60
            self.lbl_time.configure(text=f"Time: {minute:02}:{second:02}")
            time.sleep(1)
        
    def show_messagebox(self, title, text):
        answer = messagebox.askyesno(title, text)
        if answer:
            self.restart()
        else:
            sys.exit(1)
    
    
    def update_scores(self):
        current = utils.load()
        current["games won"] += 1
        minutes, seconds = current["high score"].split(":")
        previous_time = (int(minutes) * 60) + int(seconds)
        if Cell.total_time < previous_time:
            m = Cell.total_time // 60
            s = Cell.total_time % 60
            current["high score"] = f"{m:02}:{s:02}"
        utils.save(current)
        self.lbl_game_won.configure(text=f"Games won:\n{current['games won']}")
        self.lbl_high_score.configure(text=f"High Score:\n{current['high score']}")

        
    @staticmethod
    def random_mines():
        picked_cells = random.sample(Cell.all_cells, MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True       

    @staticmethod
    def get_cell(x, y):
        for cell in Cell.all_cells:
            if cell.x == x and cell.y == y:
                return cell     
    
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell(self.x - 1, self.y - 1),
            self.get_cell(self.x - 1, self.y),
            self.get_cell(self.x - 1, self.y + 1),
            self.get_cell(self.x, self.y - 1),
            self.get_cell(self.x + 1, self.y - 1),
            self.get_cell(self.x + 1, self.y),
            self.get_cell(self.x + 1, self.y + 1),
            self.get_cell(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter
