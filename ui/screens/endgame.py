import pygame
from ui.colours import Colours
from ui.elements import make_button, make_text
from ui.router import Screen
from utilities import quit_game


class Endgame(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.draw_background = True

        endgame_title = make_text("", (650, 150), 100, Colours.GOLD.value)

        quit_button = make_button(650, 600, "QUIT", 75, reactive=True)

        for tuple in [endgame_title]:
            self.text_array.append(tuple)

        for button in [quit_button]:
            self.button_array.append(button)

    def render(self, manager) -> None:
        endgame_title = make_text(
            "Congratulations, you won!" if manager.won else "You lost, try again..",
            (650, 150),
            100,
            Colours.GOLD.value,
        )
        self.text_array[0] = endgame_title

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[0].is_hovered(mouse):
                quit_game()
