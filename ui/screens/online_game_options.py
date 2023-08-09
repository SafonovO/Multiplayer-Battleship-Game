import pygame
from ui.elements import make_button
from ui.router import Element, Screen
from ui.sounds import click_sound
from game_config import SHIP_COUNT, BOARD_SIZE


class OnlineGameOptions(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
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
                manager.create_online_game(SHIP_COUNT, BOARD_SIZE, True)
                return router.navigate_to("online_create_pending")
            elif self.button_array[Element.JOIN_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                manager.create_online_game(SHIP_COUNT, BOARD_SIZE, False)
                return router.navigate_to("online_join")
            elif self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
