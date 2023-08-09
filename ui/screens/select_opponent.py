import pygame
from ui.elements import make_button
from ui.router import Element, Screen
from ui.sounds import click_sound


class SelectOpponent(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.draw_background = True
        play_button_ai = make_button(650, 150, "Play vs. AI", 50, reactive=True)
        play_button_human = make_button(650, 350, "Play vs. Human", 50, reactive=True)
        quit_button = make_button(650, 550, "Back", 75, reactive=True)

        for button in [quit_button, play_button_human, play_button_ai]:
            self.button_array.append(button)

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.AI_PLAY_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("ai_configuration")
            if self.button_array[Element.PLAY_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_to("online_game_options")
            if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
