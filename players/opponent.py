

from players.player import Player


class Opponent(Player):
    def __init__(self):
        super().__init__(coords=(150, 150), width=550, display=False) 

    def init_ships(self) -> bool:
        self.get_ships()

    def get_ships(self):
        # ask opponent to send coords of ships
        pass