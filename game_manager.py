import ai
from board import Board
from cell import Cell
from enum import Flag
from typing import Union

class Turn(Flag):
     PLAYER_ONE = 0
     PLAYER_TWO = 1

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
        print(self.turn)
        #checks if it's the right persons turn then proceeds with action
        if(self.turn == Turn.PLAYER_ONE):
            self.accepted_action(active_cell)
        # elif(self.turn == Turn.PLAYER_TWO):
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
        if self.__player1.gameover() or self.__player2.gameover():
            run = False
