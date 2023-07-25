

from players.player import Player


class Opponent(Player):
    def __init__(self, ship_count,game_size):
        super().__init__(ship_count,game_size, coords=(150, 150), width=550, display=False)

    def set_client(self, client):
        self.client = client


    # def init_ships(self) -> bool:
    #     self.get_ships()

    def get_ships(self):
        # ask opponent to send coords of ships
        pass