import pygame
from ui.colours import Colours
from ui.elements import make_button, quit_button_image
from ui.router import Screen
from ui.sounds import click_sound
from ui.text import Text


class OnlineCreatePending(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        self.quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        waiting_title = Text("Waiting for opponent", (650, 300), 50, Colours.GOLD.value)
        waiting_text = Text(
            "You can invite a friend to this game with the code below",
            (650, 375),
            30,
            Colours.WHITE.value,
        )

        self.code_text = Text("", (650, 425), 30, Colours.GOLD.value)

        self.text_array = [waiting_title, waiting_text, self.code_text]
        self.button_array = [self.quit_button]

    def render(self, manager) -> None:
        self.code_text.value = (
            manager.client.code
            if manager.client != None and manager.client.code != ""
            else "Loading... (If you keep seeing this, please check your internet connection)"
        )

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
