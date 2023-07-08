import ai
import pygame
import sys
from board import Board
from cell import Cell
from enum import Flag
from typing import Union
from button import Button, ReactiveButton, TextButton
from fonts import get_font

class Turn(Flag):
     PLAYER_ONE = 0
     PLAYER_TWO = 1


SCREEN = pygame.display.set_mode((1300, 800))
BG = pygame.image.load("assets/Background.png")

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
    __aigame=True
    run = True

    #singleton class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def create_game(self, boards):
        self.__player1 = boards[0]
        self.__player2 = boards[1]
        if(self.__aigame):
            # the boards will always be the same size. but AI will always be player 1
            self.__aiplayer= ai.AI(self.__player1.get_size())

    
    '''
    Tracks turn
    needs to know if the cell hit contains a ship
    '''
    #called from play() in game.py
    def action(self, active_cell):
        #checks if it's the right persons turn then proceeds with action
        if(self.turn == Turn.PLAYER_ONE):
            self.accepted_action(active_cell)
        elif(self.turn == Turn.PLAYER_TWO):
            x, y = self.__aiplayer.guess()
            self.accepted_action(self.__player1.get_cell(x, y))


    '''
    Checks if active_cell was a hit. 
    If hit, returns True, False otherwise.
    '''
    def accepted_action(self, active_cell):
        if not isinstance(active_cell, Cell):
            return False
        self.turn = self.turn ^ Turn.PLAYER_TWO
        if (active_cell.hit()):
            self.endgame()
            return True
        else:
            return False


    '''
    checks if the game is over
    '''
    
    def endgame(self):
        if self.__player1.gameover():
            self.endgamescreen("Player2")
        elif self.__player2.gameover():
            self.endgamescreen("Player1")
    

    
    def endgamescreen(self, winner):
        run = False
        text=get_font(100).render(winner + " WINS!", True, '#b68f40')
        text_rect = text.get_rect(center=(650, 100))
        quit_button = Button(image=pygame.image.load("assets/navy_button.png"), pos=(650, 550))
        quit_button = ReactiveButton(quit_button, hover_surface=pygame.image.load("assets/navy_button_hover.png"),
                                    active_surface=pygame.image.load("assets/navy_button_hover.png"))
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
            

    
    
