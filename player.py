

class Player:
    def __init__(self, board):
        self.board = board
        self.__miss_next_turn: False

    def place_ships(self) -> bool:
        pass

    def use_ability(self) -> bool:
        pass
