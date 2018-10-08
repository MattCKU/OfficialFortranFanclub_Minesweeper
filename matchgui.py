import pygame
import tkinter as tk
import random
from random import shuffle
from tkinter import messagebox
from tkinter import *

class matchgui:
    def __init__(self):
        self.if_win=False
        root = tk.Tk()
        button = tk.Button(root, text="Start")
        root.title("Welcome to the Matching game!")

        self.parent = root
        self.buttons = [[tk.Button(root, fg="black", bg="SkyBlue", font="50", width=10, height=5, command=lambda row=row, column=column:
        self.select(row, column)) for column in range(5)] for row in range(2)]
        for row in range(2):
            for column in range(5):
                self.buttons[row][column].grid(row=row, column=column)

        self.state = False
        self.setupboard()


        button.grid(row=2, column=2)
        root.mainloop()

    def setupboard(self):
        self.board = list('XXYYZZAABB')
        random.shuffle(self.board)
        self.board = [self.board[:5], self.board[5:10]]
        for row in self.buttons:
            for button in row:
                button.config(text='', state=tk.NORMAL)

    def select(self, row, column):
        self.buttons[row][column].config(text=self.board[row][column])
        self.buttons[row][column].config(state=tk.DISABLED)
        if not self.state:
            self.state = (row, column)
        else:
            x,y = self.state
            if self.board[row][column] == self.board[x][y]:
                self.board[row][column] = ''
                self.board[x][y] = ''
                if not any(''.join(row) for row in self.board):
                    messagebox.showinfo(title='SUCCESS!', message='You win! You cam back to minesweeper ')
                    self.if_win=True
                    root.destroy()
                """else:
                    messagebox.showinfo(title='FAIL!!', message='You lose! Game Over! ')"""

            else:
                self.parent.after(300, self.cover, row, column, x, y)
            self.state = False

    def cover(self, x1, y1, x2, y2):
        self.buttons[x1][y1].config(text='', state=tk.NORMAL)
        self.buttons[x2][y2].config(text='', state=tk.NORMAL)
    def get_if_win(self):
        return self.if_win




#root.title("Welcome to the Matching game!")
"""photo = PhotoImage(file="apple.png")
label1 = Label1(root,image=photo)
label1.pack()"""
#matchgui(root)
"""label = tk.Label(root, text="Welcome to the matching game!")"""
#button = tk.Button(root, text="Start")
"""label.grid(row=4,column=4)"""
#button.grid(row=2,column=2)
#root.mainloop()