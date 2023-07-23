

from board import Board

# BUG: adjusting the board size may cause the ships to be placed off-screen for the opponent
BOARD_SIZE = 8
NUM_SHIPS = 3

class Player:
    def __init__(self, coords=(850, 375), width=300, display=True):
        self.__miss_next_turn: False
        self.board = Board(size=BOARD_SIZE, num_ships=NUM_SHIPS,
                           coords=coords, width=width, display=display)
        self.board.build_board()
        self.init_ships()

    def init_ships(self) -> bool:
        self.board.place_ships()

    def use_ability(self) -> bool:
        pass
