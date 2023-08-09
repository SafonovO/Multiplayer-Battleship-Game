import pygame
from ui.elements import make_button
from ui.router import Screen
from ui.sounds import click_sound
from game_config import SHIP_COUNT, BOARD_SIZE


class OnlineGameOptions(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        self.create_button = make_button(650, 150, "Create Game", 50, reactive=True)
        self.join_button = make_button(650, 350, "Join Game", 50, reactive=True)
        self.quit_button = make_button(650, 550, "Back", 75, reactive=True)

        self.button_array = [self.quit_button, self.join_button, self.create_button]

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.create_button.is_hovered(mouse):
                click_sound.play()
                manager.create_online_game(SHIP_COUNT, BOARD_SIZE, True)
                return router.navigate_to("online_create_pending")
            elif self.join_button.is_hovered(mouse):
                click_sound.play()
                manager.create_online_game(SHIP_COUNT, BOARD_SIZE, False)
                return router.navigate_to("online_join")
            elif self.quit_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
