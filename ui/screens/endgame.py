import pygame
from ui.colours import Colours
from ui.elements import make_button
from ui.router import Screen
from ui.text import Text


class Endgame(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True

        endgame_title = Text(
            "Congratulations, you won!" if manager.won else "You lost, try again..",
            (650, 150),
            100,
            Colours.GOLD,
        )

        self.main_menu_button = make_button(650, 600, "Main Menu", 75, reactive=True)

        self.text_array = [endgame_title]
        self.button_array = [self.main_menu_button]

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.main_menu_button.is_hovered(mouse):
                router.navigate_to("main_menu")
