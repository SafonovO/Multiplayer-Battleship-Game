# from ai import AI
import pygame
import sys
from board import Board
from cell import Cell
from enum import Enum
from typing import Union
from button import Button, ReactiveButton, TextButton
from fonts import get_font
SCREEN = pygame.display.set_mode((1300, 800))
BG = pygame.image.load("assets/Background.png")
#from Ai import Ai--
class Turn(Enum):
     PLAYER_ONE = 1
     PLAYER_TWO = 2

class GameManager:
    
    '''
    create two instances of board
    sends coords between boards
    passes turn
    '''
    '''
    manager will check if a miss is returned and flip boolean if no ships are hit
    0=game over 
    1= player1 
    2=player2
    '''
    turn = Turn.PLAYER_ONE
    __player1: Union[Board, None] = None
    __player2: Union[Board, None] = None
    #__ai= Ai()---
    __aigame=True
    # __aiplayer= AI()---
    #singleton class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def create_game(self, boards):
        self.__player1 = boards[0]
        self.__player2 = boards[1]
    
    '''
    Tracks turn
    needs to know if the cell hit contains a ship
    '''
    #called from play() in game.py
    def action(self, active_cell):
        #checks if it's the right persons turn then proceeds with action
        if(self.__aigame):
                self.accepted_action(active_cell)
                #maybe call ai here? depends on ai implementation---
        elif(self.turn == Turn.PLAYER_ONE and self.__player1.contains(active_cell)):
            self.accepted_action(active_cell)
        elif(self.turn == Turn.PLAYER_TWO and self.__player2.contains(active_cell)):
            self.accepted_action(active_cell)

    #executes action
    def accepted_action(self, active_cell):
        if not isinstance(active_cell, Cell):
            return
        if (not active_cell.hit()):
            '''
            for phase two calling AI to make a move
            later version will differentiate between
            '''          
            if self.turn == Turn.PLAYER_ONE:
                if(not self.__aigame):
                    self.turn = Turn.PLAYER_TWO
            elif self.turn == Turn.PLAYER_TWO: 
                
                self.turn = Turn.PLAYER_ONE    
                
            return
        #if hit subtract from nships
        if self.turn == Turn.PLAYER_ONE:
            self.__player2.minus()
        elif self.turn ==Turn.PLAYER_TWO:
            self.__player1.minus()
        self.endgame()
    
    '''
    checks if the game is over
    '''
    
    def endgame(self):
        if self.__player1.gameover():
            self.endgamescreen("Player2")
        elif self.__player2.gameover():
            self.endgamescreen("Player1")
        turn = self.turn
    
    def endgamescreen(self, winner):
        text=get_font(100).render(winner + " WINS!", True, '#b68f40')
        text_rect = text.get_rect(center=(650, 100))
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(650, 550))
        quit_button = TextButton(quit_button, text="QUIT", font=get_font(75))
        while(True):
            mouse = pygame.mouse.get_pos()
            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(text, text_rect)
            for button in [quit_button]:
                button.render(SCREEN, mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_hovered(mouse):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            

    
    
