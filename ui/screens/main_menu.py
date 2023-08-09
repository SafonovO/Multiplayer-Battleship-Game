import pygame
from utilities import quit_game
from ui.colours import Colours
from ui.elements import make_button, make_text
from ui.router import Element, Screen
from ui.sounds import click_sound


class MainMenu(Screen):
    def __init__(self) -> None:
        super().__init__()
        text = make_text("BATTLESHIP", (650, 150), 100, Colours.GOLD.value)
        play_button = make_button(650, 350, "PLAY", 75, reactive=True)
        quit_button = make_button(650, 550, "QUIT", 75, reactive=True)

        for button in [quit_button, play_button]:
            self.button_array.append(button)

        for tuple in [text]:
            self.text_array.append(tuple)

    def handle_event(self, event, mouse, router, _manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.PLAY_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("select_opponent")
            if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                quit_game()
