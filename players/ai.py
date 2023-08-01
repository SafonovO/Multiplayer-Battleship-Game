'''
Class for the AI opponent. 
'''

import random
from time import sleep
from players.opponent import Opponent


class AI(Opponent):
    def __init__(self,ship_count,game_size):
        super().__init__(ship_count,game_size)
        self.init_ships()
        self.revealed = []
        self.guessed = []
        self.__size = self.board.get_size()

    def guess(self):
        pass

    def handleResult(self, isHit):
        pass


class EasyAI(Opponent):
    '''
    Easy AI is just a random number generator

    It will simply fire on random cells each time
    '''
    def __init__(self,ship_count,game_size):
        super().__init__(ship_count,game_size)
        self.init_ships()
        self.revealed = []
        self.guessed = []
        self.__size = self.board.get_size()

    def guess(self):
        sleep(1)
        success = False

        while not success:
            x = random.randint(0, self.__size - 1)
            y = random.randint(0, self.__size - 1)
            if (x, y) not in self.guessed:
                success = True

                self.guessed.append((x, y))
                return x, y


class MediumAI(AI):
    '''
    Medium AI will randomly guess a cell.

    If that cell is a hit, it will explore adjacent cells
    that have not been explored yet

    If the cell is a miss, guess some other random cell.
    '''
    def guess(self):
        '''
        Guesses that reveal part of a ship will have those
        coordinates placed in revealed.
        Subsequent guesses will be to coordinates adjacent
        to revealed coordinates.
        Once an entire ship is revealed, those coordinates
        will be added to guessed and removed from revealed.
        '''
        def guess(self):
            sleep(1)
            while True:
                x = random.randint(0, self.__size - 1)
                y = random.randint(0, self.__size - 1)
                if (x, y) not in self.guessed:
                    self.guessed.append((x, y))
                    return x, y



class HardAI(Opponent):
    '''
    '''
    pass
