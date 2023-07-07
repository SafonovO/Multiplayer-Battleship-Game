from board import Board
from cell import Cell
from AI import AI
import pygame
class game_manager:
    
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
    turn=1
    __player1 = None
    __player2 = None
    __aiplayer= AI()
    #singleton class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(game_manager, cls).__new__(cls)
        return cls.instance
    
    @staticmethod
    #might be used later for phase two not using
    def create_game(self, game_type, size, num_of_ships):
        #initializes Board class
        self.__player1 =Board(size, num_of_ships)
        self.__player2 =Board(size, num_of_ships)
        #calls build_board() from board class
        self.__player1.build_board()
        
        #will eventually need to differentiate between ai and multiplayer creation
        if(game_type==1):
            self.__player2.build_board()
        else:
            self.__player2.build_board()
    
    '''
    Tracks turn
    needs to know if the cell hit contains a ship
    '''
    @staticmethod
    #called from play() in game.py
    def action(self, active_cell):
        #active_cell executes the hit
            if (not active_cell.hit()):
                
                '''
                for phase two calling AI to make a move
                later version will differentiate between
                ''' 
                if (self.turn==1):
                    self.__aiplayer.guess()
                elif(self.turn==2):
                    self.turn=1
            return self.endgame()
    '''
    checks if the game is over
    '''
    def draw(self, SCREEN):
        self.player1.draw_board(SCREEN)
        self.player2.draw_board(SCREEN)
        
        
    
    @staticmethod
    def endgame(self):
        if(self.player1.gameover() or self.player2.gameover()):
                return 0
        return self.turn