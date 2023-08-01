'''
Class for the AI opponent. 
'''

import random
from time import sleep
from players.opponent import Opponent

class AI(Opponent):
    '''
    AI Interface

    All AI should support a guess function
    that allows it to guess a coordinate on the
    opponent's board

    Later AI will also support a set_last_hit(x, y)
    method that allows communication when a cell is 
    hit. Declare it in the interface
    '''
    def guess(self):
        pass

    def set_last_hit(self, x, y):
        pass



class EasyAI(AI):
    def __init__(self,ship_count,game_size):
        super().__init__(ship_count,game_size)
        self.init_ships()
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
    def __init__(self,ship_count,game_size):
        super().__init__(ship_count,game_size)
        self.init_ships()
        self.guessed = []
        self.__size = self.board.get_size()
        self.last_hit = None

    '''
    self.last_hit contains the coords of the last hit cell

    The idea behind Medium AI is to exlpore cells
    adjacent to the last hit cell

    once we have explored all adjacent cells and there are no
    more hits, set last_hit back to None and continue to
    find another random cell
    '''
    def guess(self):
        '''
        If there is not a recently hit cell to explore,
        simply pick a random one (like EasyAI)
        '''
        if self.last_hit == None:
            return self.random_guess()

        else:
            '''
            If we reach this point, it is because last_hit is not None

            We explore an adjacent cell that has not yet been fired on

            Do this with adjacent_cells(), which will return None
            if there are no adjacent cells that are available to be fired
            on. If there are available adjacent cells, it will return one
            of them
            '''
            adjacent = self.get_adjacent()
            if adjacent != None:
                self.guessed.append((adjacent[0], adjacent[1]))
                return adjacent

            else:
                # all adjacent cells are explored, take a random guess
                # also, set last_hit back to None
                self.last_hit = None
                return self.random_guess()

    def random_guess(self):
        # guess a random cell, similar to EasyAI
        success = False

        while not success:
            x = random.randint(0, self.__size - 1)
            y = random.randint(0, self.__size - 1)
            if (x, y) not in self.guessed:
                success = True

        self.guessed.append((x, y))
        return x, y

    def set_last_hit(self, x, y):
        '''
        Setter for last hit

        The idea is, if we fire a shot and hit, the client
        will call this method and set the last hit
        to let us know
        '''
        self.last_hit = (x, y)

    def get_adjacent(self):
        '''
        Prerequisite: self.last_hit is NOT None

        This function will examine the cells adjacent
        to last_hit

        If there exists some adjacent cell that has not
        been guessed, we return any one of them

        If all such adjacent cells have been guessed,
        return None

        Adjacent cells to (x, y) are:

        (x-1, y)
        (x+1, y)

        (x, y-1)
        (x, y+1)

        A cell is invalid if it is in self.guessed,
        or if it exceeds the boundaries of the board
        '''
        if self.last_hit == None:
            return None

        x = self.last_hit[0]
        y = self.last_hit[1]

        adjacents = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1)
        ]

        for cell in adjacents:
            if cell not in self.guessed and cell[0] < self.__size \
            and cell[1] < self.__size and cell[0] >= 0 and cell[1] >= 0:
                return cell[0], cell[1]

        return None