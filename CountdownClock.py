import pygame
#Clock class to be used in minigames for Minesweeper.
#Assumes that there is a surface created 
class CountdownClock:
    def __init__(self,duration):
        BLACK = (0,0,0)
        self.time = duration
        self.currentTime = 0
        self.start_ticks = pygame.time.get_ticks()
       
    def getTime(self):
        self.currentTime = int(pygame.time.get_ticks() - self.start_ticks)/1000
        return self.currentTime
        
    