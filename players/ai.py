'''
Class for the AI opponent. 
'''

import random
from time import sleep
from players.opponent import Opponent


class AI(Opponent):
    '''
    Guesses that reveal part of a ship will have those coordinates placed in revealed.
    Subsequent guesses will be to coordinates adjacent to revealed coordinates.
    Once an entire ship is revealed, those coordinates will be added to guessed and 
    removed from revealed.
    '''

    def __init__(self,ship_count,game_size):
        super().__init__(ship_count,game_size)
        self.init_ships()
        self.revealed = []
        self.guessed = []
        self.__size = self.board.get_size()

    def guess(self):
        sleep(1)
        while True:
            x = random.randint(0, self.__size - 1)
            y = random.randint(0, self.__size - 1)
            if (x, y) not in self.guessed:
                self.guessed.append((x, y))
                return x, y

    def handleResult(self, isHit):
        pass

