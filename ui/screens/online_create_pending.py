import pygame
from ui.colours import Colours
from ui.elements import make_button, make_text, quit_button_image
from ui.fonts import get_font
from ui.router import Element, Screen
from ui.sounds import click_sound


class OnlineCreatePending(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        waiting_title = make_text("Waiting for opponent", (650, 300), 50, Colours.GOLD.value)
        waiting_text = make_text(
            "You can invite a friend to this game with the code below",
            (650, 375),
            30,
            Colours.WHITE.value,
        )

        code = get_font(30).render("", True, Colours.GOLD.value)
        code_rect = code.get_rect(center=(650, 425))
        code_tuple = (code, code_rect)

        for tuple in [waiting_title, waiting_text, code_tuple]:
            self.text_array.append(tuple)

        for button in [quit_button]:
            self.button_array.append(button)

    def render(self, manager) -> None:
        code = (
            manager.client.code
            if manager.client != None and manager.client.code != ""
            else "Loading... (If you keep seeing this, please check your internet connection)"
        )
        code_rendered = get_font(30).render(code, True, Colours.GOLD.value)
        code_rect = code_rendered.get_rect(center=(650, 425))
        code_tuple = (code_rendered, code_rect)

        self.text_array[2] = code_tuple

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
