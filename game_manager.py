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
from utilities.button import Button, ReactiveButton, TextButton
from board.cell import Cell
from utilities.fonts import get_font
from drawer import Drawer


class Turn(Flag):
    PLAYER_ONE = 0
    PLAYER_TWO = 1

SCREEN = pygame.display.set_mode((1300, 800))
BG = pygame.image.load("assets/Background.png")
draw= Drawer()
class GameManager:
    pygame.init()
    __player1=None
    __player2=None
    '''
    create two instances of board
    sends coords between boards
    passes turn
    '''    
    '''
    Drawing assets
    '''
    
    # singleton class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def start_client(self):
        self.client = Client()
        self.client.start()

    def get_player(self, player_ID):
        if player_ID == 1:
            return self.__player1
        if player_ID == 2:
            return self.__player2
        else: return None

    def shut_down(self):
        if self.client:
            self.client.send("close")
            self.client.join()
            print("joined client thread")

    async def create_game(self, ai_game,ship_count,game_size, create, join):
        print("is this an ai game?", ai_game)
        self.turn = Turn.PLAYER_ONE
        draw.ships_left=ship_count
        self.run = True
        self.__player1 = Player(ship_count,game_size)
        if ai_game:
            self.__player2 = AI(ship_count,game_size)
            self.client = None
        else:
            self.client = Client()
            task = asyncio.ensure_future(self.client.start())
            self.__player2 = Opponent(ship_count,game_size)
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
        if draw.active_cell is not None:
            draw.active_cell.draw_selected_cell(SCREEN)

    def update_placement(self):
        # Draw a larger board for the placement stage
        self.__player1.draw_large_board(SCREEN)
        if draw.active_cell is not None:
            draw.active_cell.draw_selected_cell(SCREEN)

    def preview_ship(self, num_left):
        '''
        This function previews the ship that is about to be placed.
        A ship will be drawn as a collection of contiguous green cells
        if the selected location is a valid place to put the ship
        If there is a conflict, the ship cells will be drawn in red
        The parameter num_left tells us which ship in the array we
        should consider
        The parameter vertical tells us the orientation of the ship
        '''
        s = self.__player1.board.get_ship(-num_left)

        cells = []

        for i in range(s.get_size()):
            if draw.vertical:
                newcell = (draw.active_cell.coordinates[0], draw.active_cell.coordinates[1] + i)
            else:
                newcell = (draw.active_cell.coordinates[0] + i, draw.active_cell.coordinates[1])
            cells.append(newcell)

        '''
        Check for conflicts.
        If there is a conflict,
            - set conflicts = True
            - remove the conflicting cell from the list
        '''   
        conflicts = False

        for c in cells:
            # is c out of bounds?
            # c[0] is the column. if c[0] >= the board size, we are out of bounds
            # c[1] is the row. if c[1] >= the board size, we are out of bounds
            if c[0] >= self.__player1.board.get_size():
                conflicts = True
                cells.remove(c)

            elif c[1] >= self.__player1.board.get_size():
                conflicts = True
                cells.remove(c)

            # does c already contain a ship?
            elif self.__player1.large_board.get_cell(c[0], c[1]).ship != None:
                conflicts = True

        '''
        Now, draw the cells in the list 'cells'
        If conflicts = True, draw said cells in red
        Draw them in green otherwise.
        '''

        for c in cells:
            color = "Red"
            if conflicts == False:
                color = "Green"

            self.__player1.large_board.get_cell(c[0], c[1]).draw_cell_color(SCREEN, color)


    def place_ship(self, num_left, vertical, active_cell):
        '''
        Create a list of cells that this ship would occupy
        let n = __player1. board.get_ship(-num_left)
        the list should be of length n.get_size()
        The first cell in the list will be active_cell
        then, proceed to add cells to the list in ascending
        order of column
        Maintain an array of cells which this ship will occupy.
        We can validate each cell before the ship is placed.
        A cell is invlid if:
            - another ship is placed there
            - its coordinates are out of bounds
        Then, place the ship into each of the cells iff all are valid
        NEW PARAMETER: vertical=True indiccates that this
        ship should be placed vertically. Set the cells as such
        '''
        s = self.__player1.board.get_ship(-num_left)

        cells = []

        for i in range(s.get_size()):
            if vertical:
                newcell = (active_cell.coordinates[0], active_cell.coordinates[1] + i)
            else:
                newcell = (active_cell.coordinates[0] + i, active_cell.coordinates[1])
            cells.append(newcell)

        # validate each cell
        # if any cell is invalid, return False
        for c in cells:
            # is c out of bounds?
            # c[0] is the column. if c[0] >= the board size, we are out of bounds
            # c[1] is the row. if c[1] >= the board size, we are out of bounds
            if c[0] >= self.__player1.board.get_size():
                draw.active_cell = None
                return False

            if c[1] >= self.__player1.board.get_size():
                draw.active_cell = None
                return False
            # does c already contain a ship?
            if self.__player1.large_board.get_cell(c[0], c[1]).ship != None:
                draw.active_cell = None
                return False

        # set the ship in each cell
        for c in cells:
            self.__player1.board.get_cell(c[0], c[1]).ship = s
            self.__player1.large_board.get_cell(c[0], c[1]).ship = s

        draw.active_cell = None

        '''
        if draw.active_cell:
            draw.active_cell.ship = s
            # place the ships onto the large board and then copy the ship to the small board
            self.__player1.board.get_cell(draw.active_cell.coordinates[0],draw.active_cell.coordinates[1]).ship = draw.active_cell.ship
            draw.active_cell = None
            return True
        '''
        return True

    def get_active_cell(self):
        return draw.active_cell

    def set_active_cell_placement(self,mouse):
        if self.__player1.large_board.get_cell_mouse(mouse) is not None:
            draw.active_cell = self.__player1.large_board.get_cell_mouse(mouse)
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
                result = self.validate_shot(self.__player1.board.get_cell(int(coords[0]), int(coords[1])))
                self.client.send_result(result)
            self.turn ^= Turn.PLAYER_TWO


    async def fire_shot(self,active_cell):
        '''
        Returns true if the shot was fired successfully
        '''
        # checks if it's the right persons turn then proceeds with action
        if active_cell and self.turn == Turn.PLAYER_ONE:
            if isinstance(self.__player2, Opponent) and self.client:
                coords = active_cell.coordinates
                self.client.send_guess(coords[0], coords[1])
                self.client.get_result()
                while self.client.my_result is None:
                    # wait for response
                    await asyncio.sleep(0.1)
                # print("result is", self.client.my_result)
                if self.client.my_result == "True":
                    active_cell.set_ship(NormalShip(1))
                self.client.my_result = None
            self.validate_shot(active_cell)
            # self.active_cell.print_cell()
            active_cell = None
            return True
        return False


    def validate_shot(self, active_cell):
        '''
        Checks if active_cell was a hit. 
        If hit, returns True, False otherwise.
        '''
        if (active_cell.hit()):
            self.endgame()
            return True
        else:
            return False

    '''
    checks if the game is over
    '''
    
    #checks if the game is over
    def endgame(self):
        if self.__player1.board.gameover():
            draw.endgamescreen("Player2")
        elif self.__player2.board.gameover():
            draw.endgamescreen("Player1")
    
    def render(self, bool, place):
        draw.render_elements(bool, self.__player1, self.__player2, place)
    
    async def event(self, type):
        if(type=='placement'):
            ret=await draw.event_check(type, self.__player2,self.set_active_cell_placement,self.place_ship)
        elif(type=='play'):
            ret=await draw.event_check(type, self.__player2, self.fire_shot,None)
        else:
            ret=await draw.event_check(type, self.__player2, None, None)
        
        return ret

    def draw(self,type):
        draw.draw_elements(type)
    