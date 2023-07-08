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

    def guess(self) -> bool:
        sleep(1)
        x = random.randint(0, self.__size-1)
        y = random.randint(0, self.__size-1)
        return x, y

    def place_ships(self) -> bool:
        pass

    def use_ability(self) -> bool:
        pass
