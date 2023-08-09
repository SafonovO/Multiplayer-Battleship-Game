import asyncio
from enum import Enum, Flag
from client import Client
from players.opponent import Opponent
from players.player import Player
from players.ai import EasyAI, AI, HardAI, MedAI

import pygame
from pygame.locals import *
from pygame import mixer

from board.board import Board
from ships.normal_ship import NormalShip
from ships.ship import Ship
from ui.button import Button, ReactiveButton, TextButton
from board.cell import Cell


class Turn(Flag):
    PLAYER_ONE = 0
    PLAYER_TWO = 1


class AIDifficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


SCREEN = pygame.display.set_mode((1300, 800))
BG = pygame.image.load("assets/Background.png")
mixer.init()
miss_sound = pygame.mixer.Sound("assets/sounds/miss.ogg")
hit_sound = pygame.mixer.Sound("assets/sounds/hit.ogg")
click_sound = pygame.mixer.Sound("assets/sounds/ui-click.mp3")
fire_sound = pygame.mixer.Sound("assets/sounds/fire.ogg")

async_tasks = set()


class GameManager:
    """
    create two instances of board
    sends coords between boards
    passes turn
    """

    """
    manager will check if a miss is returned and flip boolean if no ships are hit
    0=game over 
    1= player1 
    2=player2
    """

    # singleton class
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    async def start_client(self, stop: asyncio.Event):
        print("manager attempting to start client")
        self.client = Client()
        await self.client.start(stop)

    def get_player(self, player_ID):
        if player_ID == 1:
            return self.__player1
        if player_ID == 2:
            return self.__player2
        else:
            return None

    def create_online_game(self, ship_count: int, board_size: int, creating_game: bool):
        if self.client == None:
            raise Exception("Multiplayer client must be started first!")
        print(f"{'Creating' if creating_game else 'Joining'} online game")
        self.game_over = False
        self.turn = Turn.PLAYER_ONE
        self.run = True
        self.won = None
        self.__player1 = Player(ship_count, board_size)
        self.__player2 = Opponent(ship_count, board_size)
        self.client.identify()
        if creating_game:
            self.client.create_game(ship_count, board_size)
        self.active_cell = None

    def create_ai_game(self, ship_count: int, board_size: int, ai_difficulty: AIDifficulty):
        print("creating AI game")
        self.game_over = False
        self.turn = Turn.PLAYER_ONE
        self.run = True
        self.won = None
        self.__player1 = Player(ship_count, board_size)
        match ai_difficulty:
            case AIDifficulty.EASY:
                self.__player2 = EasyAI(ship_count, board_size)
            case AIDifficulty.MEDIUM:
                self.__player2 = MedAI(ship_count, board_size)
            case AIDifficulty.HARD:
                self.__player2 = HardAI(ship_count, board_size, self.__player1)
            case _:
                print("Invalid AI Difficulty")
        self.active_cell = None

    def hard_ai_setup(self):
        """
        HardAI wil be able to peek into its opponent's array.

        However, it is instantiated before the opponentn places
        their ships. So after the oppoennt has placed their ships,
        invoke this method to tell the hardAI where they are

        *************PRECONDITION - IMPORTANT!!!!!!!
        This function will assume __player2 is a hardAI
        if this is not the case, I make no promises to what
        this function will do
        """
        if isinstance(self.__player2, HardAI):
            self.__player2.get_opp_ships()

    def update_boards(self):
        # draw my board
        self.__player1.board.draw_board(SCREEN)
        self.__player2.board.draw_board(SCREEN)
        # Draw active cell if it is not None
        if self.active_cell is not None:
            self.active_cell.draw_selected_cell(SCREEN)

    def update_placement(self):
        # Draw a larger board for the placement stage
        self.__player1.draw_large_board(SCREEN)
        if self.active_cell is not None:
            self.active_cell.draw_selected_cell(SCREEN)

    def preview_ship(self, num_left, vertical):
        """
        This function previews the ship that is about to be placed.

        A ship will be drawn as a collection of contiguous green cells
        if the selected location is a valid place to put the ship

        If there is a conflict, the ship cells will be drawn in red

        The parameter num_left tells us which ship in the array we
        should consider

        The parameter vertical tells us the orientation of the ship
        """
        s = self.__player1.board.get_ship(-num_left)

        cells = []

        for i in range(s.get_size()):
            if vertical:
                newcell = (
                    self.active_cell.coordinates[0],
                    self.active_cell.coordinates[1] + i,
                )
            else:
                newcell = (
                    self.active_cell.coordinates[0] + i,
                    self.active_cell.coordinates[1],
                )
            cells.append(newcell)

        """
        Check for conflicts.

        If there is a conflict,
            - set conflicts = True
            - remove the conflicting cell from the list

        I will need to iterate over a copy of the cells lsit.
        This is because we are potentially changing it as we loop,
        so the array will become messed up if we iterate 
        over the array while removing stuff from it
        """
        cellscopy = []
        for cell in cells:
            cellscopy.append(cell)

        conflicts = False

        for c in cellscopy:
            # is c out of bounds?
            # c[0] is the column. if c[0] >= the board size, we are out of bounds
            # c[1] is the row. if c[1] >= the board size, we are out of bounds
            if c[0] >= self.__player1.board.get_size():
                conflicts = True
                cells.remove(c)

            elif c[1] >= self.__player1.board.get_size():
                conflicts = True
                cells.remove(c)

            # does c already contain a ship?
            elif self.__player1.large_board.get_cell(c[0], c[1]).ship != None:
                conflicts = True

        """
        Now, draw the cells in the list 'cells'

        If conflicts = True, draw said cells in red

        Draw them in green otherwise.
        """

        for c in cells:
            color = "Red"
            if conflicts == False:
                color = "Green"

            self.__player1.large_board.get_cell(c[0], c[1]).draw_cell_color(SCREEN, color)

    def place_ship(self, num_left, vertical):
        """
        Create a list of cells that this ship would occupy

        let n = __player1. board.get_ship(-num_left)

        the list should be of length n.get_size()

        The first cell in the list will be active_cell
        then, proceed to add cells to the list in ascending
        order of column

        Maintain an array of cells which this ship will occupy.

        We can validate each cell before the ship is placed.
        A cell is invlid if:
            - another ship is placed there
            - its coordinates are out of bounds

        Then, place the ship into each of the cells iff all are valid

        NEW PARAMETER: vertical=True indiccates that this
        ship should be placed vertically. Set the cells as such
        """
        s = self.__player1.board.get_ship(-num_left)

        cells = []

        for i in range(s.get_size()):
            if vertical:
                newcell = (
                    self.active_cell.coordinates[0],
                    self.active_cell.coordinates[1] + i,
                )
            else:
                newcell = (
                    self.active_cell.coordinates[0] + i,
                    self.active_cell.coordinates[1],
                )
            cells.append(newcell)

        # validate each cell
        # if any cell is invalid, return False
        for c in cells:
            # is c out of bounds?
            # c[0] is the column. if c[0] >= the board size, we are out of bounds
            # c[1] is the row. if c[1] >= the board size, we are out of bounds
            if c[0] >= self.__player1.board.get_size():
                self.active_cell = None
                return False

            if c[1] >= self.__player1.board.get_size():
                self.active_cell = None
                return False
            # does c already contain a ship?
            if self.__player1.large_board.get_cell(c[0], c[1]).ship != None:
                self.active_cell = None
                return False

        # set the ship in each cell
        for c in cells:
            self.__player1.board.get_cell(c[0], c[1]).ship = s
            self.__player1.large_board.get_cell(c[0], c[1]).ship = s

        self.active_cell = None

        """
        if self.active_cell:
            self.active_cell.ship = s
            # place the ships onto the large board and then copy the ship to the small board


            self.__player1.board.get_cell(self.active_cell.coordinates[0],self.active_cell.coordinates[1]).ship = self.active_cell.ship
            self.active_cell = None
            return True
        """
        return True

    def randomize_ships(self):
        # place player1's ships randomly
        self.__player1.board.place_ships()

    def get_active_cell(self):
        return self.active_cell

    def set_active_cell(self, mouse):
        """
        returns false if mouse click is not on cell,
        returns true and sets the active cell otherwise
        """
        if self.__player2.board.get_cell_mouse(mouse) is not None:
            self.active_cell = self.__player2.board.get_cell_mouse(mouse)
            return True
        return False

    def set_active_cell_placement(self, mouse):
        if self.__player1.large_board.get_cell_mouse(mouse) is not None:
            self.active_cell = self.__player1.large_board.get_cell_mouse(mouse)
            return True
        return False

    async def change_turn(self):
        self.turn ^= Turn.PLAYER_TWO
        if self.turn == Turn.PLAYER_TWO:
            if isinstance(self.__player2, AI):
                x, y = self.__player2.guess()
                hit = await self.validate_shot(self.__player1.board.get_cell(x, y))
                await asyncio.sleep(0.5)
                if hit:
                    # if the cell is a hit, set last_hit to x, y
                    self.__player2.set_last_hit(x, y)

            elif self.client:
                print("[manager] get guess")
                self.client.get_guess()
                while self.client.opp_guess is None:
                    # wait for opponent to guess
                    await asyncio.sleep(0.1)
                coords = (self.client.opp_guess).split(",")
                self.client.opp_guess = None
                # should prob check if coords is valid, ie not of size 0
                result = await self.validate_shot(
                    self.__player1.board.get_cell(int(coords[0]), int(coords[1]))
                )
                await asyncio.sleep(0.1)
                self.client.send_result("True" if result else "False")
            self.turn ^= Turn.PLAYER_TWO

    async def fire_shot(self):
        """
        Returns true if the shot was fired successfully
        """
        # checks if it's the right persons turn then proceeds with action
        # play sounds

        if self.active_cell and self.turn == Turn.PLAYER_ONE:
            click_sound.play()
            fire_sound.play()
            if isinstance(self.__player2, Opponent) and self.client:
                coords = self.active_cell.coordinates
                self.client.send_guess(coords[0], coords[1])
                self.client.get_result()
                while self.client.my_result is None:
                    # wait for response
                    await asyncio.sleep(0.1)
                # print("result is", self.client.my_result)
                if self.client.my_result == "True":
                    print("HIT A SHIP!!!!")
                    self.active_cell.set_ship(NormalShip(1))
                self.client.my_result = None
            await self.validate_shot(self.active_cell)
            # self.active_cell.print_cell()
            self.active_cell = None
            return True
        return False

    def fire_shot_new(self):
        """
        Returns true if the shot was fired successfully
        """
        if self.active_cell and self.turn == Turn.PLAYER_ONE:
            click_sound.play()
            fire_sound.play()
            self.validate_shot_new(self.active_cell)
            self.active_cell = None
            return True
        return False

    def validate_shot_new(self, active_cell):
        """
        Marks the active cell as hit.
        Checks if there was a ship in the active cell.
        If ship, returns True, False otherwise.
        """
        if active_cell.hit():
            self.endgame()
            hit_sound.play()
            return True
        else:
            miss_sound.play(0, 2000)
            return False

    async def validate_shot(self, active_cell):
        """
        Marks the active cell as hit.
        Checks if there was a ship in the active cell.
        If ship, returns True, False otherwise.
        """
        if active_cell.hit():
            await asyncio.sleep(0.3)
            self.endgame()
            hit_sound.play()

            return True
        else:
            await asyncio.sleep(0.3)
            miss_sound.play(0, 2000)
            return False

    def endgame(self):
        """
        Checks if the game is over and update the state variables accordingly
        """
        if self.__player1.board.gameover():
            self.game_over = True
            self.won = False
        elif self.__player2.board.gameover():
            self.game_over = True
            self.won = True
        elif self.client and self.client.game_over:
            self.game_over = True
            self.won = self.client.won
