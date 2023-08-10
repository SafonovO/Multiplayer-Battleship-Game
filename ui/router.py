import pygame
from game_manager import GameManager
from pygame.locals import *
from typing import Type
from ui.button import Button
from ui.colours import Colours
from ui.text import Text
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


class Screen:
    def __init__(self, manager: GameManager) -> None:
        """Define layout in the constructor. Subclasses can define more layout after super()ing"""
        self.text_array: list[Text] = []
        self.button_array: list[Button] = []
        self.draw_background = False

    #  "Router" (with quotes) is a forward reference to the class below to avoid cyclic reference
    def render(self, mouse: tuple[int, int], router: "Router", manager: GameManager) -> None:
        """Define layout that depends on dynamic data from game manager"""
        pass

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
            screen.render(mouse, self, self.manager)
            for text in screen.text_array:
                text.render(SCREEN)
            for button in screen.button_array:
                button.render(SCREEN, mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                    return
                screen.handle_event(event, mouse, self, self.manager)
            pygame.display.update()
