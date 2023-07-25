

from board.board import Board

BOARD_SIZE = 4
NUM_SHIPS = 5

class Player:
    def __init__(self,ship_count,game_size, coords=(850, 375), width=300, display=True):
        self.__miss_next_turn: False
        self.board = Board(size=game_size, num_ships=ship_count,
                           coords=coords, width=width, display=display)
        self.board.build_board()

    def init_ships(self) -> bool:
        self.board.place_ships()

    def use_ability(self) -> bool:
        pass
