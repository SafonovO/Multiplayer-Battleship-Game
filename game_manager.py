import asyncio
import sys
from enum import Flag
from client import Client
from players.opponent import Opponent
from players.player import Player
from players.ai import AI

import pygame

from board.board import Board
from ships.normal_ship import NormalShip
from ships.ship import Ship
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

    async def create_game(self, ai_game, create, join):
        print("is this an ai game?", ai_game)
        self.turn = Turn.PLAYER_ONE
        self.run = True
        self.__player1 = Player()
        if ai_game:
            self.__player2 = AI()
            self.client = None
        else:
            self.client = Client()
            task = asyncio.ensure_future(self.client.start())
            self.__player2 = Opponent()
            if create:
                self.client.create_game()
            elif join:
                self.client.join_game()
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

    async def change_turn(self):
        self.turn ^= Turn.PLAYER_TWO
        if self.turn == Turn.PLAYER_TWO:
            if isinstance(self.__player2, AI):
                x, y = self.__player2.guess()
                self.validate_shot(self.__player1.board.get_cell(x, y))
            elif self.client:
                self.client.get_guess()
                while self.client.opp_guess is None:
                    # wait for opponent to guess
                    await asyncio.sleep(0.1)
                coords = (self.client.opp_guess).split(',')
                self.client.opp_guess = None
                # should prob check if coords is valid, ie not of size 0
                result = self.validate_shot(
                    self.__player1.board.get_cell(int(coords[0]), int(coords[1])))
                self.client.send_result(result)
            self.turn ^= Turn.PLAYER_TWO

    async def fire_shot(self):
        '''
        Returns true if the shot was fired successfully
        '''
        # checks if it's the right persons turn then proceeds with action
        if self.active_cell and self.turn == Turn.PLAYER_ONE:
            if isinstance(self.__player2, Opponent) and self.client:
                coords = self.active_cell.coordinates
                self.client.send_guess(coords[0], coords[1])
                self.client.get_result()
                while self.client.my_result is None:
                    # wait for response
                    await asyncio.sleep(0.1)
                print("result is", self.client.my_result)
                if self.client.my_result == "True":
                    self.active_cell.set_ship(NormalShip(1))
                self.client.my_result = None
            self.validate_shot(self.active_cell)
            self.active_cell.print_cell()
            self.active_cell = None
            return True
        return False

    def validate_shot(self, active_cell):
        '''
        Marks the active cell as hit.
        Checks if there was a ship in the active cell. 
        If ship, returns True, False otherwise.
        '''
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
                self.endgamescreen(False)
        elif self.__player2.board.gameover():
                self.endgamescreen(True)

    def endgamescreen(self, won):
        run = False
        # TO DO: end the damn game for multiplayer
        # if self.client:
        #     self.client.end_game()
        text = get_font(100).render("Congratulations, you won!" if won else "You lost, try again...", True, '#b68f40')
        text_rect = text.get_rect(center=(650, 100))
        quit_button = Button(image=pygame.image.load(
            "assets/navy_button.png"), pos=(650, 550))
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
