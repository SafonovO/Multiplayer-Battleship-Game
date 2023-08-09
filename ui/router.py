from typing import Type
import pygame
from enum import Enum
from pygame.locals import *
from game_manager import GameManager
from ui.button import Button
from ui.colours import Colours
from ui.elements import make_button, make_text
from ui.fonts import get_font
from ui.input import Input
from utilities import quit_game


pygame.init()
pygame.display.set_caption("Battleship")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
quit_button_image = pygame.image.load("assets/quit.png")
confirm_button_image = pygame.image.load("assets/ConfirmButton.png")
PLAYING_SURFACE = pygame.Rect(100, 50, 1100, 700)

SCREEN = pygame.display.set_mode((1300, 800))
BG = pygame.image.load("assets/Background.png")

button_array = []
text_array = []


class Element(Enum):
    QUIT_BUTTON = 0
    PLAY_BUTTON = 1
    JOIN_BUTTON = 1
    EASY_BUTTON = 1
    MED_BUTTON = 2
    ROTATE_BUTTON = 1
    FIRE_BUTTON = 1
    AI_PLAY_BUTTON = 2
    CONFIRM_BUTTON = 2
    CREATE_BUTTON = 2
    HARD_BUTTON = 3


class Screen:
    def __init__(self, manager: GameManager) -> None:
        """Define layout in the constructor. Subclasses can define more layout after super()ing"""
        self.text_array = []
        self.button_array: list[Button] = []
        self.draw_background = False

    def render(self, manager: GameManager) -> None:
        """Define layout that depends on dynamic data from game manager"""
        pass

    #  "Router" (with quotes) is a forward reference to the class below to avoid cyclic reference
    def handle_event(
        self, event: pygame.Event, mouse: tuple[int, int], router: "Router", manager: GameManager
    ):
        """Contains the interactive logic for the screen"""
        pass


class Router:
    def __init__(self, manager: GameManager, screens: dict[str, Type[Screen]] = {}) -> None:
        self.routing_stack: list[Screen] = []
        self.manager = manager
        self.screens = screens

    def navigate_to(self, screen_name: str):
        screen_type = self.screens.get(screen_name)
        if screen_type == None:
            raise KeyError(f"No screen with name {screen_name}")
        screen = screen_type(self.manager)
        self.routing_stack.append(screen)

    def navigate_back(self):
        self.routing_stack.pop()

    def stack_is_empty(self):
        return len(self.routing_stack) == 0

    def render(self):
        if not self.stack_is_empty():
            mouse = pygame.mouse.get_pos()
            screen = self.routing_stack[-1]
            SCREEN.blit(BG, (0, 0))
            if screen.draw_background:
                pygame.draw.rect(SCREEN, Colours.NAVY_BLUE.value, PLAYING_SURFACE)
            for element in screen.text_array:
                if element == None:
                    continue
                SCREEN.blit(element[0], element[1])
            for button in screen.button_array:
                button.render(SCREEN, mouse)
            screen.render(self.manager)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                    return
                screen.handle_event(event, mouse, self, self.manager)
            pygame.display.update()


class Drawer:
    def __init__(self):
        pass

    coord_tuple = None

    def draw_screen(self, screen):
        if screen == "play":
            self.play()

    def error(self, error_msg: str):
        error_text = make_text(error_msg, (650, 375), 30, "#ffffff")
        quit_button = make_button(650, 550, "Quit", 50, reactive=True)

        for tuple in [error_text]:
            text_array.append(tuple)

        for button in [quit_button]:
            button_array.append(button)

    def play(self):
        # setup labels for the boards
        opponent_board_label = get_font(30).render("OPPONENT'S BOARD", True, "White")
        opponent_board_label_rect = opponent_board_label.get_rect(center=(425, 100))
        opponent_tuple = (opponent_board_label, opponent_board_label_rect)

        my_board_label = get_font(30).render("MY BOARD", True, "White")
        my_board_label_rect = my_board_label.get_rect(center=(1000, 325))
        my_board_tuple = (my_board_label, my_board_label_rect)

        fire_button = make_button(1000, 250, "FIRE", 20, image=confirm_button_image)
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        # Create text
        select_text = get_font(15).render("YOU HAVE SELECTED:", True, "White")
        select_text_rect = select_text.get_rect(center=(1000, 150))
        select_tuple = (select_text, select_text_rect)

        for tuple in [opponent_tuple, my_board_tuple, select_tuple]:
            text_array.append(tuple)

        for button in [quit_button, fire_button]:
            button_array.append(button)

    def render_screen(self, mouse, playing_surface=False):
        SCREEN.blit(BG, (0, 0))
        if playing_surface:
            pygame.draw.rect(SCREEN, Colours.NAVY_BLUE.value, PLAYING_SURFACE)
        if self.coord_tuple != None:
            SCREEN.blit(self.coord_tuple[0], self.coord_tuple[1])
        for element in text_array:
            SCREEN.blit(element[0], element[1])
        for button in button_array:
            button.render(SCREEN, mouse)

    def clear_array(self):
        button_array.clear()
        text_array.clear()
