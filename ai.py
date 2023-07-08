'''
Class for the AI opponent. 
'''

import random
from time import sleep
import game_manager

class AI():
    '''
    Guesses that reveal part of a ship will have those coordinates placed in revealed.
    Subsequent guesses will be to coordinates adjacent to revealed coordinates.
    Once an entire ship is revealed, those coordinates will be added to guessed and 
    removed from revealed.
    '''
    revealed, guessed = [], []

    def __init__(self, size):
        self.__size = size
        print("Started AI opponent for size", self.__size)

    def run(self):
        print(self._size)

    def guess(self):
        sleep(1)
        while True:
            print("generating")
            x = random.randint(0, self.__size-1)
            y = random.randint(0, self.__size-1)
            if (x, y) not in self.guessed:
                self.guessed.append((x,y))
                return x, y

    def handleResult(self, isHit):
        pass

    def place_ships(self) -> bool:
        pass

    def use_ability(self) -> bool:
        pass
