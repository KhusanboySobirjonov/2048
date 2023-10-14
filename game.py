import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random
import sqlite
import datetime

class Game():
    def __init__(self):
        self.__size = 4
        self.__matrix = []
        self.__root = ctk.CTk()
        self.__width = self.__size * 120 + (self.__size + 1) * 10
        self.__height = self.__size * 120 + (self.__size + 1) * 10 + 120
        self.__head_frame = ctk.CTkFrame(self.__root, width=self.__width, height=120)
        self.__head_frame.pack(side=tk.TOP)
        self.__frame = ctk.CTkFrame(self.__root, width=self.__width - 50, height=self.__height - 200, fg_color="#bbada0")
        self.__frame.pack(side=tk.BOTTOM, pady=5)
        self.__dict_color = {0 : '#cdc1b5', 2 : '#eee4da', 4 : '#ece0c8', 8 : '#f8ba05', 16 : '#fb9b00', 32 : '#fe5404', 64 : '#fc290c', 128 : '#a9174b',
                             256 : '#8701b1', 512 : '#158dc7', 1024 : '#0844fc', 2048 : '#67b131', 4096 : '#d2e929'}

        self.__max_score = 0

        self.__label_score = ctk.CTkLabel(self.__head_frame, text="Score : " + str(self.__max_score),
                                          font=("Bold", 28))
        self.__label_score.place(x=98, y=20)

        self.__label_best_score = ctk.CTkLabel(self.__head_frame, text="Best score : " + str(self.__max_score),
                                               font=("Bold", 28), anchor='e')
        self.__label_best_score.place(x=30, y=70)

        self.__new_game = ctk.CTkButton(self.__head_frame, text="New\nGame", font=("Bold", 28), command=lambda : self.__run())
        self.__new_game.place(x=self.__width - 150, y=25)
        self.__database = sqlite.Database()

        self.__run()

    def __run(self):
        """
        
        :return: None
        """
        self.__matrix = [[0 for j in range(self.__size)] for i in range(self.__size)]

        try:
            self.__database.create_table_scores()
        except Exception as er:
            print(er)

        self.__label_best_score.configure(text="Best score : " + str(max([s[1] for s in self.__database.select_all_scores()])))
        self.__max_score = 0

        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        x = (screen_width / 2) - (self.__width / 2)
        y = (screen_height / 2) - (self.__height / 2)

        self.__root.geometry(f"{self.__width}x{self.__height}+{int(x)}+{int(y)}")

        self.__root.title("2048")
        self.__root.resizable(False, False)
        self.__create_cell()
        self.__root.bind('<Key>', lambda event: self.__check_key(event))
        self.__root.mainloop()

    def __validation_grid(self):
        """
        Check each box to see if there are options
        :return: True | False
        """

        counter = 0
        for i in range(self.__size):
            for j in range(self.__size - 1):
                if self.__matrix[i][j] == self.__matrix[i][j + 1]:
                    counter += 1

        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] == 0:
                    counter += 1

        for i in range(self.__size):
            for j in range(self.__size - 1):
                if self.__matrix[j][i] == self.__matrix[j + 1][i]:
                    counter += 1
        return False if counter else True

    def __check_key(self, event):
        """
        Check and count in which direction it moves by pressing the button
        :param event:
        :return: None
        """

        key_code = event.keycode

        # Left array key
        if key_code in [38, 83, 113]:
            for i in range(self.__size):
                h = False
                for j in range(1, self.__size):
                    x = j
                    while x > 0 and (self.__matrix[i][x] == self.__matrix[i][x - 1] or self.__matrix[i][x - 1] == 0):
                        if self.__matrix[i][x] == self.__matrix[i][x - 1] and self.__matrix[i][x - 1] != 0:
                            self.__max_score += 2 * self.__matrix[i][x - 1]
                            h = True
                        self.__matrix[i][x - 1] += self.__matrix[i][x]
                        self.__matrix[i][x] = 0
                        x -= 1
                        if h:
                            break
                for j in range(1, self.__size):
                    x = j
                    while x > 0 and self.__matrix[i][x - 1] == 0:
                        self.__matrix[i][x], self.__matrix[i][x - 1] = self.__matrix[i][x - 1], self.__matrix[i][x]
                        x -= 1

            self.__create_cell()

        # Up array key
        elif key_code in [25, 80, 111]:
            for i in range(self.__size):
                h = False
                for j in range(1, self.__size):
                    x = j
                    while x > 0 and (self.__matrix[x][i] == self.__matrix[x - 1][i] or self.__matrix[x - 1][i] == 0):
                        if self.__matrix[x][i] == self.__matrix[x - 1][i] and self.__matrix[x - 1][i] != 0:
                            self.__max_score += 2 * self.__matrix[x - 1][i]
                            h = True
                        self.__matrix[x - 1][i] += self.__matrix[x][i]
                        self.__matrix[x][i] = 0
                        x -= 1
                        if h:
                            break
                for j in range(1, self.__size):
                    x = j
                    while x > 0 and self.__matrix[x - 1][i] == 0:
                        self.__matrix[x][i], self.__matrix[x - 1][i] = self.__matrix[x - 1][i], self.__matrix[x][i]
                        x -= 1

            self.__create_cell()

        # Right array key
        elif key_code in [40, 85, 114]:
            for i in range(self.__size-1, -1, -1):
                h = False
                for j in range(self.__size - 2, -1, -1):
                    x = j
                    while x < self.__size - 1 and (self.__matrix[i][x] == self.__matrix[i][x + 1] or self.__matrix[i][x + 1] == 0):
                        if self.__matrix[i][x] == self.__matrix[i][x + 1] and self.__matrix[i][x + 1] != 0:
                            self.__max_score += 2 * self.__matrix[i][x + 1]
                            h = True
                        self.__matrix[i][x + 1] += self.__matrix[i][x]
                        self.__matrix[i][x] = 0
                        x += 1
                        if h:
                            break
                for j in range(self.__size - 2, -1, -1):
                    x = j
                    while x < self.__size - 1 and self.__matrix[i][x + 1] == 0:
                        self.__matrix[i][x], self.__matrix[i][x + 1] = self.__matrix[i][x + 1], self.__matrix[i][x]
                        x += 1
            self.__create_cell()

        # Down arrow key
        elif key_code in [39, 84, 116]:
            for i in range(self.__size-1, -1, -1):
                h = False
                for j in range(self.__size-2, -1, -1):
                    x = j
                    while x < self.__size - 1 and (self.__matrix[x][i] == self.__matrix[x+1][i] or self.__matrix[x+1][i] == 0):
                        if self.__matrix[x][i] == self.__matrix[x+1][i] and self.__matrix[x+1][i] != 0:
                            self.__max_score += 2 * self.__matrix[x+1][i]
                            h = True
                        self.__matrix[x+1][i] += self.__matrix[x][i]
                        self.__matrix[x][i] = 0
                        x += 1
                        if h:
                            break
                for j in range(self.__size - 2, -1, -1):
                    x = j
                    while x < self.__size - 1 and self.__matrix[x + 1][i] == 0:
                        self.__matrix[x][i], self.__matrix[x + 1][i] = self.__matrix[x+1][i], self.__matrix[x][i]
                        x += 1
            self.__create_cell()

    def __create_matrix(self):
        """
        Create a matrix inside the frame
        :return: None
        """
        self.__label_score.configure(text=f"Score : {self.__max_score}")
        for i in range(self.__size):
            for j in range(self.__size):
                btn = ctk.CTkButton(self.__frame, (self.__width-(self.__size + 1) * 10) // self.__size, (self.__height-(120 + (self.__size + 1) * 10)) // self.__size, text=str('' if self.__matrix[i][j] == 0 else self.__matrix[i][j]), text_color=("#625847" if self.__matrix[i][j] in [2, 4] else "#ffffff"), fg_color=self.__dict_color[self.__matrix[i][j]],
                                    hover=False, font=("Bold", 40), border_color="#bbada0")
                btn.grid(row=i, column=j, padx=5, pady=5)
        if self.__validation_grid():
            self.__label_best_score.configure(
                text="Best score : " + str(max([s[1] for s in self.__database.select_all_scores()])))
            messagebox.showinfo("Game over", f"Max score {self.__max_score}  ")
            self.__database.add_score(Score=self.__max_score, Created_at=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            return

    def __create_cell(self):
        """
        Create a new value cell
        :return: None
        """
        empty_cells = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] == 0:
                    empty_cells += [[i, j]]

        if len(empty_cells) != 0:
            random_cells = random.choice(empty_cells)
            self.__matrix[random_cells[0]][random_cells[1]] = 2
        self.__create_matrix()

