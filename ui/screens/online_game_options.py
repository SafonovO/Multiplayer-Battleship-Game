import pygame
from ui.elements import make_button
from ui.router import Screen
from ui.sounds import click_sound


class OnlineGameOptions(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        self.should_start_client = True

        self.create_button = make_button(650, 150, "Create Game", 50, reactive=True)
        self.join_button = make_button(650, 350, "Join Game", 50, reactive=True)
        self.quit_button = make_button(650, 550, "Back", 75, reactive=True)

        self.button_array = [self.quit_button, self.join_button, self.create_button]

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.create_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("size")
            elif self.join_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("online_join")
            elif self.quit_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()