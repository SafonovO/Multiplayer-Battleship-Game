import string
import pygame
from ui.colours import Colours
from ui.elements import make_button, make_text, quit_button_image
from ui.fonts import get_font
from ui.input import Input
from ui.router import Element, Screen
from ui.sounds import click_sound


class OnlineJoin(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.draw_background = True
        self.code_input = Input(max_length=9)

        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        join_title = make_text("Join game", (650, 300), 50, Colours.GOLD.value)
        join_desc = make_text(
            "Enter an invite code to join a game", (650, 375), 30, Colours.WHITE.value
        )

        code_chars = make_text("_________", (650, 425), 30, "#b68f40")

        join_button = make_button(650, 550, "Join", 50, reactive=True)

        for tuple in [join_title, join_desc, code_chars]:
            self.text_array.append(tuple)

        for button in [quit_button, join_button]:
            self.button_array.append(button)

    def render(self, _manager):
        code_chars = make_text(
            " ".join(self.code_input.value.ljust(9, "_")), (650, 425), 30, Colours.GOLD.value
        )
        self.text_array[2] = code_chars

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
            if (
                self.button_array[Element.JOIN_BUTTON.value].is_hovered(mouse)
                and len(self.code_input.value) == 9
            ):
                click_sound.play()
                manager.client.join_game(self.code_input.value)
                return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.code_input.backspace()
            elif event.unicode in string.ascii_letters + string.digits:
                self.code_input.input(event.unicode.upper())
