"""
Idea for Game logic
https://inventwithpython.com/chapter10.html
Chapter 10 (TIC TAC TOE) from AL Swegigart MAking Games with Python and Pygame
"""
from tkinter import *
import random as rand
import copy

GameB_Size = 420  # pixels
Color_x = 'BLACK'
Color_o = 'RED'
Color_border = 'GREY'
Color_background = 'WHITE'

Char_max_size = GameB_Size/60  # pixels: adjusting ratio
Letter_size = 0.5  # 0 to 1 : symbol size to cell ratio

State_start = 0  # Game Start
State_AI = 1  # Computers Turn
State_player = 2  # Players Turn
State_gg = 3  # Game over

Player = 2  # X: 2, O: 1, empty = 0
Tile_size = GameB_Size / 3


class TicTacToe(Tk):

    def __init__(self):
        """ @pre    Board traits defined above method, canvas,board,
            and gamestates are defined here for external use in methods
            @post   Once the canvas, board, copy_board and screen are
            defined the game call reference the same entity.
        """
        root = self
        self.if_win=False
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
        root.mainloop()

    def start_screen(self):
        """ @pre    Clears the screen, introduces welcome screen
            @post   No changes are made anywhere
            @return Screen
        """
        self.canvas.delete('all')
        self.canvas.create_text(int(GameB_Size/2), int(GameB_Size/2), text='Second Chance', fill='RED', font=('Arial', int(-GameB_Size/10)))

    def new_board(self):
        """ @pre    Clears the screen, then prints
            a new screen of Canvas tiles
            @post   No changes are made anywhere
            @return Screen
        """
        self.canvas.delete('all')
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for n in range(1, 3):
            self.canvas.create_line(Tile_size*n, 0, Tile_size*n, GameB_Size, width=4, fill=Color_border)  # vertical grid border
            self.canvas.create_line(0, Tile_size*n, GameB_Size, Tile_size*n, width=4, fill=Color_border)  # horizontal grid border

    def click(self, event):
        """ @pre    Takes a left click from a user and transforms
            the user input into a coordinate to be used to
            determine gamestates and actions.
            @post   No changes are made anywhere
            @return None
        """
        x = self.pixel_to_grid(event.x)
        y = self.pixel_to_grid(event.y)

        if self.gamestate == State_start:
            self.new_board()
            self.gamestate = Player
        elif self.gamestate == State_player and self.board[x][y] == 0:
            self.new_move(x, y)

            if self.redeemed(self.board,1):
                self.gamestate = State_gg
                self.game_result('AI WINS')
            elif self.tie():
                self.gamestate = State_gg
                self.game_result('DRAW')
            else:
                self.gamestate = State_AI
                self.new_move_ai()

                if self.redeemed(self.board,2):
                    self.gamestate = State_gg
                    self.game_result('Player WINS')
                elif self.tie():
                    self.gamestate = State_gg
                    self.game_result('DRAW')
                else:
                    self.gamestate = State_player

    def new_move(self, x_pos, y_pos):
        """ @pre    Takes x & y coordinates and acts upon the location
            by sending the the parameters to the method to draw_player to
            print the move to the canvas (USER MOVE). The board is then updated with the new value.
            @post   Called in click() to update user moves
            @return None
        """
        self.draw_player(x_pos, y_pos)
        self.board[x_pos][y_pos] = 2

    def new_move_ai(self):
        """ @pre    Takes x & y coordinates and acts upon the location by sending
            the the parameters to the method to draw_ai toprint the move to
            the canvas (AI MOVE). The board is then updated with the new value. Handles AI LOGIC
            @post   Called in click() to update computer moves
            @return None
        """
        not_moved = TRUE
        n = 0
        if not_moved:
            for i in range(0, 3):
                for j in range(0, 3):
                    n = n + 1
                    self.copy_board = copy.deepcopy(self.board)
                    if self.is_free(self.copy_board, i, j):
                        if not_moved:
                            self.copy_board[i][j] = 2
                            if self.redeemed(self.copy_board, 2):
                                self.draw_ai(i, j)
                                self.board[i][j] = 1
                                not_moved = FALSE

                        if not_moved:
                            self.copy_board[i][j] = 1
                            if self.redeemed(self.copy_board, 1):
                                self.draw_ai(i, j)
                                self.board[i][j] = 1
                                not_moved = FALSE

                        if not_moved and n == 9:
                            w = q = 1
                            if self.board[w][q] == 0:
                                self.draw_ai(w, q)
                                self.board[w][q] = 1
                                not_moved = FALSE

                            else:
                                fake = (0, 2)
                                k = rand.choice(fake)
                                l = rand.choice(fake)
                                if self.board[k][l] !=0:
                                    while self.board[k][l] != 0:
                                        k = rand.randint(0, 2)
                                        l = rand.randint(0, 2)
                                if self.board[k][l] == 0:
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
                                self.draw_ai(k, l)
                                self.board[k][l] = 1
                                not_moved = FALSE

    def draw_player(self, x_pos, y_pos):
        """ @pre    Take in x and y position and create an X on the canvas
            tile at that position an X letter is printed to the canvas
            @post   Called in new_move() when the user clicks a tile.
            @return Updated Canvas/Screen
        """
        x = self.grid_to_pixel(x_pos)
        y = self.grid_to_pixel(y_pos)
        c = Tile_size/2*Letter_size

        self.canvas.create_line(x-c, y-c, x+c, y+c, width=Char_max_size, fill=Color_x)  # Left Line (starting at the top)
        self.canvas.create_line(x+c, y-c, x-c, y+c, width=Char_max_size, fill=Color_x)  # Right Line (starting at the top)

    def is_free(self, type, x, y):
        """ @pre    Take in either the board of the deepcopy of the board (copy_board)
            and check the value if the canvas/board is empty at that location.
            @post   Called in new_move() when the user clicks a tile.
            @return returns a TRUE or FALSE if the value is an empty tile
        """
        return type[x][y] == 0

    def draw_ai(self, x_pos, y_pos):
        """ @pre    Take in x and y position and create an
            X on the Canvas tile at that position.
            @post   Called in new_move_ai() when the computer decides a tile to combat the user.
            @return Updated Canvas/Screen
        """
        x = self.grid_to_pixel(x_pos)
        y = self.grid_to_pixel(y_pos)
        c = 1.45 * Tile_size / 2 * Letter_size

        self.canvas.create_oval(x - c, y - c, x + c, y + c, fill=Color_o, outline="") # Outer Circle
        self.canvas.create_oval(x - c / 1.45, y - c / 1.45, x + c / 1.45, y + c / 1.45, fill=Color_background, outline="")  # Inner Circle

    def redeemed(self, type, value):
        """ @pre    Take in the board (either original or deepcopy) and the player value (AI or Player)
            @post   Called in click() to check gamestates and called in new_move_ai to check for a win (AI LOGIC)
            @return Returns a TRUE or FALSE (TRUE for a WIN, FALSE for a LOSS or DRAW)
        """
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
        """ @pre    No input parameters needed,
            @post   Checks if user ties with the computer
            @return Returns a TRUE or FALSE (TRUE = TIE) 
        """
        for row in self.board:
            if 0 in row:
                return False

        return True
    
    def is_gameover(self, outcome):
        """ @pre    Takes in an event/state from game_result and sets the Bool for a win to true
            @post   Called in game_result take the final gamestates and finalize the result.
            @return Returns a TRUE or FALSE (TRUE for a WIN, FALSE for a LOSS or DRAW)
        """
        if outcome == 'Player WINS':  # Player loses Pysweeper and TicTacToe
            self.if_win = True
        elif outcome == 'O WINS':  # Go back to Pysweeper
            self.if_win = False

    def game_result(self, outcome):
        """ @pre    Handles an outcome from the click method, prints to the game screen,
            and sends the result to the is_gameover method.
            @post   Called in click() to clear the screen, take in gamestates and print the message to the screen.
            Sends the result to a value sumbitting method is_gameover.
            @return Updates Finish screen.
        """
        self.canvas.delete('all')

        if outcome == 'Player WINS':  # Therefore go back to Pysweeper
            status = 'You survived!'
            status_color = Color_x
            self.is_gameover(True)

        elif outcome == 'AI WINS':  # Player loses Pysweeper and TicTacToe
            status = 'AI WINS!'
            status_color = Color_o
            self.is_gameover(False)

        elif outcome == 'DRAW':  # Therefore benefit of doubt go back to Pysweeper
            status = 'Draw! (Barely Survived)'
            status_color = 'GREY'
            self.is_gameover(True)

        self.canvas.create_rectangle(0, 0, GameB_Size, GameB_Size, fill=status_color, outline='')
        self.canvas.create_text(int(GameB_Size / 2), int(GameB_Size / 2), text=status, fill='white', font=('Times', int(-GameB_Size / 12), 'bold'))
        self.exit()

    def grid_to_pixel(self, grid_pos):
        """ @pre    Takes in a grid position and converts the position to a pixel location on the canvas.
            @post   Called in draw_player and draw_ai methods to convert to pixel locations on the canvas.
            @return Returns the pixel conversion value (int/number)
        """
        pixel_pos = grid_pos * Tile_size + Tile_size / 2

        return pixel_pos

    def pixel_to_grid(self, pixel_pos):
        """ @pre    Takes the click position and converts it to a
            grid position to easily relate to the board/tile.
            @post   Called in click() to convert the pixel position to a grid value.
            @return Returns the grid location (int/number)
        """
        if pixel_pos >= GameB_Size:
            pixel_pos = GameB_Size - 1
        grid_pos = int(pixel_pos / Tile_size)

        return grid_pos

    def exit(self):
        """ @pre    Deletes a binding
            @post   Loacted in the self initialization method, used in game_result
            @return None
        """
        self.destroy()

#def main():
 #   root = TicTacToe()
 #   root.mainloop()
#
#main()
