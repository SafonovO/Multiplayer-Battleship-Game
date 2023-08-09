import pygame
from ui.colours import Colours
from ui.elements import make_button
from ui.router import Screen
from ui.text import Text
from utilities import quit_game


class Endgame(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True

        endgame_title = Text(
            "Congratulations, you won!" if manager.won else "You lost, try again..",
            (650, 150),
            100,
            Colours.GOLD.value,
        )

        quit_button = make_button(650, 600, "QUIT", 75, reactive=True)

        for tuple in [endgame_title]:
            self.text_array.append(tuple)

        for button in [quit_button]:
            self.button_array.append(button)

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[0].is_hovered(mouse):
                quit_game()
