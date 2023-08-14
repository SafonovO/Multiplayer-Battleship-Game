from game_config import MAX_VOLUME, MIN_VOLUME
import pygame
from ui.colours import Colours
from ui.elements import (
    make_back_button,
    make_button,
    small_dash_image,
    small_x_image,
)
from ui.router import Screen
from ui.sounds import click_sound
from ui.text import Text


class PlayHelp(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True

        title_text = Text("How to Play", (650, 100), 50, Colours.GOLD)
        self.text_array = [title_text]

        steps = [
            "1. Click on a cell on the OPPONENT'S BOARD to select.              ",
            "2. Click FIRE to confirm your guess.                                                ",
            "3. A shot that has hit an enemy ship will mark the cell with        ",
            "4. A shot that has missed an enemy ship will mark the cell with ",
            "5. First player to uncover all of the other player's ships wins!      ",
        ]

        x = 650
        y = 200
        for step in steps:
            self.text_array.append(Text(step, (x, y), 20, Colours.WHITE))
            y += 50

        self.back_button = make_back_button()
        x_button = make_button(920, 300, "", 0, image=small_x_image)
        dash_button = make_button(960, 350, "", 0, image=small_dash_image)
        self.button_array = [self.back_button, x_button, dash_button]

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
