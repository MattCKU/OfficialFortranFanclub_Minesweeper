"""
Cell Grid, New game, help, quit buttons functionality

"""
import gc
import pygame
import sys
import math
from Board import *
from Cell import Cell
from gamefunctions import *
import random
from matchgui import matchgui
import tkinter as tk
from tkinter import *
from mini_games.TicTacToe import *
from CountdownClock import CountdownClock
#from mini_games.SimpleMiniGame import *



#global maxes/mins/button sizes
button_width = 80
min_width = 3 * button_width
min_height = 240



#set up colors for use later
white = (255,255,255)
black = (0,0,0)
gray = (122,122,122)

#cell and flag images 20x20
revealed_image = pygame.image.load("tile.png")
cell_image = pygame.image.load("cell_image.png")
flag_image = pygame.image.load("flag_tile.png")
one_image = pygame.image.load("one_tile.png")
two_image = pygame.image.load("two_tile.png")
three_image = pygame.image.load("three_tile.png")
four_image = pygame.image.load("four_tile.png")
five_image = pygame.image.load("five_tile.png")
six_image = pygame.image.load("six_tile.png")
seven_image = pygame.image.load("seven_tile.png")
eight_image = pygame.image.load("eight_tile.png")
mine_image = pygame.image.load("mine_tile.png")

cell_size = 20
cell_contents = {
    '1' : one_image,
    '2' : two_image,
    '3' : three_image,
    '4' : four_image,
    '5' : five_image,
    '6' : six_image,
    '7' : seven_image,
    '8' : eight_image,
    'M' : mine_image,
    '-' : revealed_image
}

class cell_button:
    """
    @pre cell object with draw, clicked, reveal, flag functions
    @post none
    @return none
    """
    def __init__(self,x, y, width, height, cell):
        """
        @pre constructor for cell button object
        @post creates a rect at given location of given size
        @return none
        """
        self.m_cell = cell
        self.rect = pygame.Rect(x * width,y * height + 40,width,height)
        self.x= x
        self.y= y
        self.size = width

class gui_button:
    """
    @pre class for interface buttons (new game, quit, etc)
    @post gui bottn made with click functionality
    @return none
    """

    def __init__(self, color, x, y, width, height, text, action = None):
        """
        @pre constructor for button object, called on declaration
        @post creates a rect at given location of given size
        @return none
        """
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.is_clicked = False
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def clicked(self):
        """
        @pre called from main game loop to do associated action
        @post execute associated functions
        @return none
        """
        if(self.action != None):
            self.action()

    def draw(self,window,outline=None):
        """
        @pre draw method with option for outline
        @post button with given parameters
        @return none
        """
        if outline:
            pygame.draw.rect(window,(0,0,0),(self.x -2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))

        if self.text != "":
            font = pygame.font.SysFont(None,20)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

def quit_game():
    """
    @pre called by quit buttons, quits game
    @post game is quit
    @return none
    """
    pygame.quit()
    quit()

def reveal(gB, row,col):
    """
    @pre calls recReveal, return Tue if mine hit
    @post recursively change cell isflagged value
    @return True if mine is hit
    """
    return recReveal(gB,row,col)



class minesweeper_gui:

    def gui_start(gB, rows, cols, mines):
        """
        @pre start game loop by passing created board and board info
        @post encompasses entire game loop
        @return none
        """
        cheat_mode=False
        num_mini_games=3


        pygame.init()
        pygame.font.init()

        #for checking if user has flagged/revealed everything
        flags = mines
        remaining = rows * cols - mines

        #dynamic board size
        if(cols * cell_size < min_width):
            display_width = min_width

        else:
            display_width = cols * cell_size

        if(rows * cell_size < min_height):
            display_height = min_height

        else:
            display_height = 40 + rows * cell_size

        #display background
        gameDisplay = pygame.display.set_mode((display_width, display_height))
        gameDisplay.fill(black)
        pygame.display.set_caption("Minesweeper")

        #create 2d array of cells, blit images
        cell_list = [[0 for i in range(cols)] for j in range(rows)]
        for row in range(rows):
            for column in range(cols):
                cell_list[row][column] = cell_button(column,row,cell_size,cell_size,gB.board[row][column])
                gameDisplay.blit(cell_image, (column * cell_size, 40 + row * cell_size))

        quit_button = gui_button((204,0,0),display_width - button_width/2, 0, button_width/2, 40, "Quit", quit_game)
        quit_button.draw(gameDisplay, 1)

        flags_button = gui_button((0,204,0),0, 0, 2 * button_width, 40, "Flags remaining: " + str(flags))
        flags_button.draw(gameDisplay, 1)
        mine_hit = False
        game_win = False
        quit_2 = ""

        while(mine_hit == False):
            #starting game loop
            flagged_count = 0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #Reveal tile
                    mouse_pos = pygame.mouse.get_pos()
                    m_rect = pygame.rect.Rect(mouse_pos, (1, 1))

                    if (quit_button.rect.colliderect(m_rect)):
                        quit_button.clicked()
                    if (game_win):
                        if(m_rect.colliderect(quit_2.rect)):
                            quit_2.clicked()

                    else:
                        #check mouse collide with list of cells
                        for row in range(rows):
                            for cell in cell_list[row]:

                                if (cell.rect.colliderect(m_rect)):

                                    if cell.m_cell.isFlagged == False:
                                        #if not flagged, turn revealed to true
                                        mine_hit = reveal(gB,cell.y,cell.x)

                                        if(mine_hit):
                                            mini_game_select=random.randint(1, num_mini_games)
                                            if(mini_game_select == 1):
                                                #simple game
                                                mini_game_win=simple_game(gameDisplay);
                                            elif(mini_game_select==2):
                                                #matching game
                                                matchingGame=matchgui()
                                                mini_game_win=matchingGame.if_win

                                            elif(mini_game_select==3):
                                                #Tic tac toe
                                                print("tic tac toe")
                                                tic_tac_toe=TicTacToe()
                                                mini_game_win = tic_tac_toe.if_win

                                            if(mini_game_win):
                                                #Won miniGame
                                                mine_hit=False;
                                                gB.board[cell.y][cell.x].isRevealed=False;
                                                flags += cell.m_cell.set_flag()
                                                flags_button.text = "Flags remaining: " + str(flags)
                                            elif(not mini_game_win):
                                                #Lose Mini Game
                                                for row in range(rows):
                                                    for cell in cell_list[row]:
                                                        cell.m_cell.set_revealed()
                                                update_display(gameDisplay, gB, cell_list, flagged_count,flags_button,quit_button)
                                                game_over(gameDisplay)
                                                pygame.quit()
                                                sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    #flag on right click
                    mouse_pos = pygame.mouse.get_pos()
                    m_rect = pygame.rect.Rect(mouse_pos,(1, 1))

                    for row in range(rows):
                        for cell in cell_list[row]:

                            if cell.rect.colliderect(m_rect):

                                if cell.m_cell.isRevealed != True:

                                    if(cell.m_cell.isFlagged == True):
                                        #if cell is flagged, toggle and update flag counter
                                        flags += cell.m_cell.set_flag()

                                    else:
                                        #if cell is not flagged, toggle and update flag counter if flags > 0

                                        if(flags > 0):
                                            flags += cell.m_cell.set_flag()

                                    flags_button.text = "Flags remaining: " + str(flags)
                                    flags_button.draw(gameDisplay, 1)
                elif event.type==pygame.KEYDOWN and event.key == 304:
                #Cheat mode
                    cheat_mode = not cheat_mode
                if (game_win == False): #Print display
                    if not cheat_mode: #Print normal board
                        flagged_count = update_display(gameDisplay, gB, cell_list, flagged_count,flags_button,quit_button)
                    else: #Print cheat board
                        flagged_count = update_display_cheat(gameDisplay, gB, cell_list, flagged_count,flags_button,quit_button)

                if(flagged_count == mines):

                    game_win = True
                    for row in range(rows):
                        for cell in cell_list[row]:
                            cell.m_cell.set_revealed()
                    flagged_count = update_display(gameDisplay, gB, cell_list, flagged_count,flags_button,quit_button)
                    pygame.font.init()
                    menu_but = gui_button((0,204,0),0,0, display_width-button_width,40, "YOU WIN!")
                    menu_but.draw(gameDisplay, 1)
                    quit_2 = gui_button(white,display_width-button_width, 0, button_width, 40, "Quit", quit_game)
                    quit_2.draw(gameDisplay, 1)
                    quit_isdrawn = True

                    if (quit_2.rect.colliderect(m_rect)):
                        quit_2.clicked()
                    pygame.display.update()

            pygame.display.update()

def update_display(display, gB, cell_list,flagged_count,flags_button,quit_button):
    """
    @pre take display, game board, cell 2d array, and flagged count inputs
    @post update each game cell
    @return flagged count for game win checking
    """
    display.fill((0,0,0))
    flagged_count = 0
    for row in range(gB.get_height()):
        for cell in cell_list[row]:

            if cell.m_cell.isRevealed:
                display.blit(cell_contents[gB.board[cell.y][cell.x].get_cell_textRep()], (cell.x * cell_size, 40 + cell.y * cell_size))

            elif cell.m_cell.isFlagged:

                display.blit(flag_image,(cell.x * cell_size, 40 + cell.y * cell_size))
                if(cell.m_cell.isMined):
                    flagged_count += 1
            else:
                display.blit(cell_image, (cell.x * cell_size, 40 + cell.y * cell_size))
    flags_button.draw(display, 1)
    quit_button.draw(display, 1)
    return (flagged_count)

def update_display_cheat(display, gB, cell_list,flagged_count,flags_button,quit_button):
    """
    @pre take display, game board, cell 2d array, and flagged count inputs
    @post update each game cell displaying cheat info
    @return flagged count for game win checking
    """
    display.fill((0, 0, 0))
    flagged_count = 0
    for row in range(gB.get_height()):
        for cell in cell_list[row]:
            display.blit(cell_contents[gB.board[cell.y][cell.x].get_cell_textRep()], (cell.x * cell_size, 40 + cell.y * cell_size))
    if cell.m_cell.isFlagged and cell.m_cell.isMined:
        flagged_count += 1
    flags_button.draw(display, 1)
    quit_button.draw(display, 1)
    return (flagged_count)

def start_game(rows,cols,mines):
    """
    @pre Creates board to pass along with board details to gui_start
    @post runs gui_start to begin game loop
    @return none
    """
    ms = minesweeper_gui
    gB = Board(cols,rows)
    place_mines(gB,mines)
    board_create(gB)
    ms.gui_start(gB,rows, cols, mines)

def simple_game(Surface):
    temp = CountdownClock(2)
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans', 60)
    mini_game_size = Surface.get_width(), Surface.get_height()
    win_img=pygame.image.load("img/win_tile.png")
    lose_img=pygame.image.load("img/lose_tile.png")

    gameSurface = pygame.Surface(mini_game_size)
    gameSurface.blit(win_img, (0,0))
    gameSurface.blit(lose_img, (120,0))
    Surface.blit(gameSurface, (0,0))
    pygame.display.flip()
    while 1:
        blank = pygame.Rect(100, 120, 120, 120)
        blankrect = pygame.draw.rect(Surface, (0, 0, 0), blank, 1)
        Surface.fill((0,0,0), blankrect)
        for event in pygame.event.get():

            if (event.type == pygame.QUIT) or ((2 - temp.getTime()) < 0):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                mx, my = pygame.mouse.get_pos()
                if mx <= 120 and my <=60:
                    return True
                elif mx >120 and my<=60:
                    return False
        textsurface = font.render(str(int(3 - temp.getTime())), False, (255,255,255))

        Surface.blit(textsurface,(100,120))
        pygame.display.update()