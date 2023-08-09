import string
import pygame
from ui.colours import Colours
from ui.elements import make_button, quit_button_image
from ui.input import Input
from ui.router import Screen
from ui.sounds import click_sound
from ui.text import Text


class OnlineJoin(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        self.code_input = Input(max_length=9)

        self.quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        join_title = Text("Join game", (650, 300), 50, Colours.GOLD.value)
        join_desc = Text(
            "Enter an invite code to join a game", (650, 375), 30, Colours.WHITE.value
        )

        self.code_chars = Text("_________", (650, 425), 30, "#b68f40")

        self.join_button = make_button(650, 550, "Join", 50, reactive=True)

        self.text_array = [join_title, join_desc, self.code_chars]
        self.button_array = [self.quit_button, self.join_button]

    def render(self, _manager):
        self.code_chars.value = " ".join(self.code_input.value.ljust(9, "_"))

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
            if (
                self.join_button.is_hovered(mouse)
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
