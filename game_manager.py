# from ai import AI
from board import Board
from cell import Cell
from enum import Enum
from typing import Union

class Turn(Enum):
     GAME_OVER = 0
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
    # __aiplayer= AI()
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
        #active_cell executes the hit
            if not active_cell.hit():
                
                '''
                for phase two calling AI to make a move
                later version will differentiate between
                ''' 
                if self.turn == Turn.PLAYER_ONE:
                    # self.__aiplayer.guess()
                    pass
                elif self.turn == Turn.PLAYER_TWO:
                    self.turn = Turn.PLAYER_ONE
            return self.endgame()

    '''
    checks if the game is over
    '''
    def endgame(self):
        if self.__player1.gameover() or self.__player2.gameover():
            return Turn.GAME_OVER
        return self.turn