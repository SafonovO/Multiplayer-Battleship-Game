import pygame
from ui.elements import make_button
from ui.router import Element, Screen
from ui.sounds import click_sound


class OnlineGameOptions(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.draw_background = True
        create_button = make_button(650, 150, "Create Game", 50, reactive=True)
        join_button = make_button(650, 350, "Join Game", 50, reactive=True)
        quit_button = make_button(650, 550, "Back", 75, reactive=True)

        for button in [quit_button, join_button, create_button]:
            self.button_array.append(button)

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.CREATE_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("online_create_pending")
            elif self.button_array[Element.JOIN_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("online_join")
            elif self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
