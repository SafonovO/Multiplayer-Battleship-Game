import pygame
from ui.colours import Colours
from ui.elements import make_button
from ui.router import Screen
from ui.text import Text
from utilities import quit_game


class Error(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True

        error_title = Text(
            "Error",
            (650, 150),
            100,
            Colours.GOLD,
        )
        error_text = Text(manager.client.error, (650, 300), 50, Colours.WHITE)

        self.quit_button = make_button(650, 600, "QUIT", 75, reactive=True)

        self.text_array = [error_title, error_text]
        self.button_array = [self.quit_button]

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.is_hovered(mouse):
                quit_game()
