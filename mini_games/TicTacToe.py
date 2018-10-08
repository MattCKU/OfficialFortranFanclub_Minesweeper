from tkinter import *
import random as rand
import copy

GameB_Size = 840 # pixels
Color_x = 'BLACK'
Color_o = 'RED'
Color_border = 'GREY'
Color_background = 'WHITE'

Char_max_size = GameB_Size/60 # pixels: adjusting ratio
Letter_size = 0.5 # 0 to 1 : symbol size to cell ratio

State_start = 0 # Game Start
State_AI = 1 # Computers Turn
State_player = 2 # Players Turn
State_gg = 3 # Game over

Player = 2 # X: 2, O: 1, empty = 0
Tile_size = GameB_Size / 3


class TicTacToe(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.canvas = Canvas(height=GameB_Size, width=GameB_Size, bg=Color_background)
        self.canvas.pack()
        self.bind('<x>', self.exit)
        self.canvas.bind('<Button-1>', self.click)
        self.gamestate = State_start
        self.start_screen()
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.copy_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.first_time = TRUE

    def start_screen(self):
        self.canvas.delete('all')
        self.canvas.create_text(int(GameB_Size/2), int(GameB_Size/2), text='Second Chance', fill='RED', font=('Arial', int(-GameB_Size/10)))

    def new_board(self):
        self.canvas.delete('all')
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for n in range(1, 3):
            self.canvas.create_line(Tile_size*n, 0, Tile_size*n, GameB_Size, width=4, fill=Color_border) # vertical grid border
            self.canvas.create_line(0, Tile_size*n, GameB_Size, Tile_size*n, width=4, fill=Color_border) # horizontal grid border

    def click(self, event):
        x = self.PixeltoGrid(event.x)
        y = self.PixeltoGrid(event.y)

        if self.gamestate == State_start:
            self.new_board()
            self.gamestate = Player
        elif self.gamestate == State_player and self.board[x][y] == 0:
            self.new_move(x, y)

            if self.redeemed(self.board,1):
                self.gamestate = State_gg
                self.Game_result('AI WINS')
            elif self.tie():
                self.gamestate = State_gg
                self.Game_result('DRAW')
            else:
                self.gamestate = State_AI
                self.new_move_ai()

                if self.redeemed(self.board,2):
                    self.gamestate = State_gg
                    self.Game_result('Player WINS')
                elif self.tie():
                    self.gamestate = State_gg
                    self.Game_result('DRAW')
                else:
                    self.gamestate = State_player

    def new_move(self, x_pos, y_pos):
        self.draw_player(x_pos, y_pos)
        self.board[x_pos][y_pos] = 2

    def new_move_ai(self):
        not_moved = TRUE
        print("CLICK!")

        n = 0
        if not_moved:
            for i in range(0, 3):
                for j in range(0, 3):
                    n = n + 1
                    print(n)
                    self.copy_board = copy.deepcopy(self.board)
                    if self.is_free(self.copy_board, i, j):
                        if not_moved:
                            self.copy_board[i][j] = 2
                            if self.redeemed(self.copy_board, 2):
                                print("Computer Block" + str(i) + str(j)+str(n))
                                self.draw_ai(i, j)
                                self.board[i][j] = 1
                                not_moved = FALSE

                        if not_moved:
                            self.copy_board[i][j] = 1
                            if self.redeemed(self.copy_board, 1):
                                print("Computer Win"+str(i)+str(j)+str(n))
                                self.draw_ai(i, j)
                                self.board[i][j] = 1
                                not_moved = FALSE

                        if not_moved and n == 9:
                            print("Computer Random Middle" + str(i) + str(j) + str(n))
                            w=q=1
                            if self.board[w][q] == 0:
                                print("Computer Random Middle"+str(i)+str(j)+str(n))
                                self.draw_ai(w, q)
                                self.board[w][q] = 1
                                not_moved = FALSE

                            else:
                                fake = (0,2)
                                k = rand.choice(fake)
                                l = rand.choice(fake)
                                if self.board[k][l] !=0:
                                    while self.board[k][l] != 0:
                                        k = rand.randint(0, 2)
                                        l = rand.randint(0, 2)
                                if self.board[k][l] == 0:
                                    print("Computer Random Pure"+str(i)+str(j)+str(n))
                                    self.draw_ai(k, l)
                                    self.board[k][l] = 1
                                    not_moved = FALSE
                    else:
                        if not_moved and n == 9:
                            fake = (0, 2)
                            k = rand.choice(fake)
                            l = rand.choice(fake)
                            if self.board[k][l] != 0:
                                while self.board[k][l] != 0:
                                    k = rand.randint(0, 2)
                                    l = rand.randint(0, 2)
                            if self.board[k][l] == 0:
                                print("ComputerSUPER Random Pure" + str(i) + str(j) + str(n))
                                self.draw_ai(k, l)
                                self.board[k][l] = 1
                                not_moved = FALSE

    def draw_player(self, x_pos, y_pos):
        x = self.GridtoPixel(x_pos)
        y = self.GridtoPixel(y_pos)
        c = Tile_size/2*Letter_size

        self.canvas.create_line(x-c, y-c, x+c, y+c, width=Char_max_size, fill=Color_x) # Left Line (starting at the top)
        self.canvas.create_line(x+c, y-c, x-c, y+c, width=Char_max_size, fill=Color_x) # Right Line (starting at the top)

    def is_free(self, type, x, y):
        return type[x][y] == 0

    def draw_ai(self, x_pos, y_pos):
        x = self.GridtoPixel(x_pos)
        y = self.GridtoPixel(y_pos)
        c = 1.45 * Tile_size / 2 * Letter_size

        self.canvas.create_oval(x - c, y - c, x + c, y + c, fill=Color_o, outline="") # Outer Circle
        self.canvas.create_oval(x - c / 1.45, y - c / 1.45, x + c / 1.45, y + c / 1.45, fill=Color_background, outline="") # Inner Circle

    def delete_tile(self, x, y):
        x_pos = self.GridtoPixel(x)
        y_pos = self.GridtoPixel(y)
        c = 1.45 * Tile_size / 2 * Letter_size

        self.canvas.create_oval(x_pos, y_pos, 0, 0, fill=Color_o, outline="") # Outer Circle
        self.canvas.create_oval(x_pos, y_pos, 0, 0, fill=Color_background, outline="") # Inner Circle

    def redeemed(self, type, value):
        for y in range(3):
            if type[y] == [value, value, value]: # Horizontal Win
                return True

        for x in range(3):
            if type[0][x] == type[1][x] == type[2][x] == value:  # Vertical Wins
                return True

        if type[0][0] == type[1][1] == type[2][2] == value: #Diagonal Win
            return True
        elif type[0][2] == type[1][1] == type[2][0] == value: #Diagonal Win
            return True

        return False

    def tie(self):
        for row in self.board:
            if 0 in row:
                return False

        return True
    
    def isGameover(self, outcome):
        if outcome == 'Player WINS': # Player loses Pysweeper and TicTacToe
            return TRUE
        elif outcome == 'O WINS': # Go back to Pysweeper
            return FALSE

    def Game_result(self, outcome):
        self.canvas.delete('all')

        if outcome == 'Player WINS': # Therefore go back to Pysweeper
            status = 'You survived!'
            status_color = Color_x
            self.isGameover(TRUE)

        elif outcome == 'AI WINS': # Player loses Pysweeper and TicTacToe
            status = 'AI WINS!'
            status_color = Color_o
            self.isGameover(FALSE)

        elif outcome == 'DRAW': # Therefore benefit of doubt go back to Pysweeper
            status = 'Draw! (Barely Survived)'
            status_color = 'GREY'
            self.isGameover(FALSE)

        self.canvas.create_rectangle(0, 0, GameB_Size, GameB_Size, fill=status_color, outline='')
        self.canvas.create_text(int(GameB_Size / 2), int(GameB_Size / 2), text=status, fill='white', font=('Times', int(-GameB_Size / 12), 'bold'))

    def GridtoPixel(self, grid_pos):
        pixel_pos = grid_pos * Tile_size + Tile_size / 2
        return pixel_pos

    def PixeltoGrid(self, pixel_pos):
        if pixel_pos >= GameB_Size:
            pixel_pos = GameB_Size - 1

        grid_pos = int(pixel_pos / Tile_size)
        return grid_pos

    def exit(self):
        self.destroy()

def main():
    root = TicTacToe()
    root.mainloop()

main()
