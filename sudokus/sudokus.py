import tkinter as tk
import customtkinter as ctk
from sudoku import Sudoku


# This is new version of my game. I commited it to git.
# Check is everything ok. pls)))


def good_array(arr):
    y = (0, 1, 2)
    ans = [[[], [], []],
           [[], [], []],
           [[], [], []]]
    for _y in range(3):
        temp = 0
        for _x in range(3):
            for i in y:
                ans[_y][_x].append(arr[i][temp:temp+3])
            temp += 3
        y = [x + 3 for x in y]
    return ans


class Start(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()

        self.geometry(size)
        self.title(title)
        self.resizable(0, 0)

        self.button_color = '#1F6AA5'
        self.bg = None
        self.sudokus_text = None
        self.game_button = None
        self.slider = None
        self.difficulty = None
        self.label = None
        self.game = None
        self.clock = False

        self.start_screen()

        self.mainloop()

    def start_screen(self):
        self.bg = ctk.CTkLabel(self, text=' ', bg_color=self.button_color, corner_radius=0)
        self.bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.sudokus_text = ctk.CTkLabel(
            self,
            text='Sudokus',
            bg_color=self.button_color,
            corner_radius=0,
            font=('Arial', 40, 'bold'),
            text_color='white',
        )
        self.sudokus_text.place(relx=0.5, rely=0.3, anchor='center')

        self.game_button = ctk.CTkButton(
            self,
            text='▶ Solve!',
            font=('Consolas', 25, 'bold'),
            command=self.start_game,
            border_width=2,
            border_color='black',
            bg_color=self.button_color
        )
        self.game_button.place(anchor='center', relx=0.5, rely=0.5)

        self.difficulty = tk.DoubleVar(value=0.5)
        self.slider = ctk.CTkSlider(
            self,
            from_=0.2,
            to=0.9,
            variable=self.difficulty,
            bg_color=self.button_color,
            command=self.update_label,
            button_color='orange',
            button_hover_color='orange'
        )
        self.slider.place(anchor='center', relx=0.5, rely=0.6)

        self.label = ctk.CTkLabel(
            self, text=f"Difficulty: {self.difficulty.get():.2f}",
            bg_color=self.button_color,
            font=('Consolas', 25, 'bold')
        )
        self.label.place(anchor='center', relx=0.5, rely=0.8)

    def update_label(self, value):
        if value <= 0.4:
            self.slider.configure(
                button_color='green',
                button_hover_color='green'
            )
        elif value <= 0.7:
            self.slider.configure(
                button_color='orange',
                button_hover_color='orange'
            )
        else:
            self.slider.configure(
                button_color='red',
                button_hover_color='red'
            )
        self.label.configure(text=f"Difficulty: {float(value):.2f}")

    def start_game(self):
        self.bg.place_forget()
        self.sudokus_text.place_forget()
        self.game_button.place_forget()
        self.slider.place_forget()
        self.label.place_forget()
        self.game = Game(self, self.difficulty.get())
        for i in range(1, 10):
            self.bind(str(i), lambda event: self.game.main.key_press(event))
        # use this for debug win)
        # self.bind('s', self.game.main.win)
        self.game.place(relx=0, rely=0, relwidth=1, relheight=1)


class Game(ctk.CTkFrame):
    def __init__(self, parent, difficulty):
        super().__init__(parent)

        # ref
        self.parent = parent
        self.parent.clock = True

        # getting board
        self.sudoku_board = Sudoku(3).difficulty(difficulty)
        self.left = 0
        for x in self.sudoku_board.board:
            for i in x:
                if i is None:
                    self.left += 1

        self.sudoku_board.show()
        self.sudoku_board_good = good_array(self.sudoku_board.board)

        self.solution = self.sudoku_board.solve().board
        self.solution_good = good_array(self.solution)

        # main frame
        self.main = MainFrame(self, self.sudoku_board_good, self.solution_good, self.left, parent)
        self.main.configure(border_color='black', border_width=10, fg_color='black')
        self.main.place(relx=0, rely=0.1, relheight=0.8, relwidth=1)

        # top and bottom
        self.top = Top(self, self.parent)
        self.top.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.bottom = Bottom(self)
        self.bottom.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

        # main loop
        self.main.set_up()


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, board, solution, left, root_window):
        super().__init__(parent)

        # variables
        self.board = board
        self.solution = solution
        self.left = left
        self.root_window = root_window
        self.buttons = [[[], [], []],
                        [[], [], []],
                        [[], [], []]]
        self.win_label = None
        self.active_btn = None
        self.original_btn_color = 0

        # layout
        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.boxes = [[0 for _ in range(3)] for _ in range(3)]

    def set_up(self):
        x, y = 0.025, 0.025
        for row in range(3):
            for column in range(3):
                frame = ctk.CTkFrame(self, fg_color='black')
                frame.place(relx=x, rely=y, relwidth=0.3, relheight=0.3)
                frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
                frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
                self.boxes[row][column] = [[0 for _ in range(3)] for _ in range(3)]
                x += 0.325
                temp = []
                for _row in range(3):
                    temp1 = []
                    for _column in range(3):
                        if self.board[row][column][_row][_column] is None:
                            text = ' '
                            button = ctk.CTkButton(
                                frame,
                                text=text,
                                font=('Consolas', 25, 'bold'),
                                border_width=1,
                                border_color='black',
                                corner_radius=0,
                                text_color_disabled='white',
                                hover_color='grey',
                                command=lambda r=row, c=column, _x=_row, _y=_column: self.set_button(r, c, _x, _y),
                                text_color='white'
                            )
                        else:
                            text = str(self.board[row][column][_row][_column])
                            button = ctk.CTkButton(
                                frame,
                                text=text,
                                font=('Consolas', 25, 'bold'),
                                border_width=1,
                                border_color='black',
                                corner_radius=0,
                                state='disabled',
                                text_color_disabled='white',
                                hover_color='grey',
                                text_color='white'
                            )
                        temp1.append(button)
                        self.original_btn_color = button.cget("fg_color")
                        button.grid(row=_row, column=_column, sticky='nsew')
                    temp.append(temp1)
                self.buttons[row][column] = temp
            y += 0.325
            x = 0.025

    def set_button(self, row, column, x, y):
        self.buttons[row][column][x][y].configure(fg_color='grey')
        self.active_btn = (row, column, x, y)

    def key_press(self, event):
        key = event.char

        if key.isdigit() and 1 <= int(key) <= 9:
            self.input_num(str(key))

    def input_num(self, num):
        if self.active_btn is not None:
            self.buttons[self.active_btn[0]][self.active_btn[1]][self.active_btn[2]][self.active_btn[3]].configure(
                text=num,
                fg_color=self.original_btn_color,
            )
            self.check(num)

    def check(self, num):
        t = self.buttons[self.active_btn[0]][self.active_btn[1]][self.active_btn[2]][self.active_btn[3]]
        s = self.solution[self.active_btn[0]][self.active_btn[1]][self.active_btn[2]][self.active_btn[3]]
        if str(s) == num:
            self.buttons[self.active_btn[0]][self.active_btn[1]][self.active_btn[2]][self.active_btn[3]].configure(
                state='disabled'
            )
            self.left -= 1
        else:
            self.buttons[self.active_btn[0]][self.active_btn[1]][self.active_btn[2]][self.active_btn[3]].configure(
                text=' ',
                fg_color='red'
            )
            self.after(
                1000,
                lambda: t.configure(fg_color=self.original_btn_color))
        self.active_btn = None
        if self.left <= 0:
            self.win()

    def win(self, event):
        self.win_label = ctk.CTkLabel(
            self,
            text='YOU SOLVE THIS',
            font=('Consolas', 20, 'bold'),
            bg_color='transparent',
            text_color='yellow',
            fg_color='transparent'
        )
        self.win_label.place(anchor='center', relx=0.5, rely=0.5)
        self.root_window.clock = False
        self.after(3000, self.restart)

    def restart(self):
        self.place_forget()
        self.root_window.start_screen()


class Top(ctk.CTkFrame):
    def __init__(self, parent, ref):
        super().__init__(parent)

        # ref
        self.start = ref

        # background
        self.bg = ctk.CTkLabel(self, text=' ', bg_color='#1F6AA5')
        self.bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # timer text
        self.timer = ctk.CTkLabel(
            self,
            text='Time: ',
            bg_color='#1F6AA5',
            font=('Consolas', 25, 'bold'),
        )

        self.timer.place(anchor='center', relx=0.5, rely=0.5)

        # actual number
        self.sec = 0
        self.minutes = 0
        self.count(self.minutes, self.sec)

    def count(self, minutes, sec, *args):
        if self.start.clock:
            if sec > 60:
                sec = 0
                minutes += 1
            if len(str(sec)) < 2:
                temp = sec
                sec = f'0{temp}'
            if len(str(minutes)) < 2:
                temp = minutes
                minutes = f'0{temp}'
            self.timer.configure(text=f'Time  {minutes}:{sec}')
            self.after(1000, lambda: self.count(int(minutes), int(sec)+1))


class Bottom(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg = ctk.CTkLabel(self, text=' ', bg_color='#1F6AA5')
        self.bg.place(relx=0, rely=0, relwidth=1, relheight=1)


Start('Sudokus', '450x550')
