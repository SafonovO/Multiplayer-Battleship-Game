import sys
from enum import Flag
from players.opponent import Opponent
from players.player import Player
from players.ai import AI

import pygame

from board.board import Board
from utilities.button import Button, ReactiveButton, TextButton
from board.cell import Cell
from utilities.fonts import get_font


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

    # singleton class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def create_game(self, ai_game):
        self.turn = Turn.PLAYER_ONE
        self.run = True
        self.__player1 = Player()
        self.__player2 = AI() if ai_game else Opponent()
        self.active_cell = None

    def update_boards(self):
        # draw my board
        self.__player1.board.draw_board(SCREEN)
        self.__player2.board.draw_board(SCREEN)
        # Draw active cell if it is not None
        if self.active_cell != None:
            self.active_cell.draw_selected_cell(SCREEN)


    def get_active_cell(self):
        return self.active_cell


    def set_active_cell(self, mouse):
        '''
        returns false if mouse click is not on cell, 
        returns true and sets the active cell otherwise
        '''
        if self.__player2.board.get_cell_mouse(mouse) != None:
            self.active_cell = self.__player2.board.get_cell_mouse(mouse)
            return True
        return False


    def change_turn(self):
        self.turn ^= Turn.PLAYER_TWO
        if self.turn == Turn.PLAYER_TWO:
            if isinstance(self.__player2, AI):
                x, y = self.__player2.guess()
                self.validate_shot(self.__player1.board.get_cell(x, y))
                self.change_turn()
            else:
                pass
                # wait for other opponent to make guess


    def fire_shot(self):
        '''
        Returns true if the shot was fired successfully
        '''
        # checks if it's the right persons turn then proceeds with action
        if self.active_cell and self.turn == Turn.PLAYER_ONE:
            self.validate_shot(self.active_cell)
            self.active_cell = None
            return True
        return False


    def validate_shot(self, active_cell):
        '''
        Checks if active_cell was a hit. 
        If hit, returns True, False otherwise.
        '''
        active_cell.set_is_guessed(True)
        if (active_cell.hit()):
            self.endgame()
            return True
        else:
            return False

    '''
    checks if the game is over
    '''

    def endgame(self):
        if self.__player1.board.gameover():
            self.endgamescreen("Player2")
        elif self.__player2.board.gameover():
            self.endgamescreen("Player1")

    def endgamescreen(self, winner):
        run = False
        text = get_font(100).render(winner + " WINS!", True, '#b68f40')
        text_rect = text.get_rect(center=(650, 100))
        quit_button = Button(image=pygame.image.load("assets/navy_button.png"), pos=(650, 550))
        quit_button = ReactiveButton(quit_button, hover_surface=pygame.image.load("assets/navy_button_hover.png"),
                                     active_surface=pygame.image.load("assets/navy_button_hover.png"))
        quit_button = TextButton(quit_button, text="QUIT", font=get_font(75))
        while (True):
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
