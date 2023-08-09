import pygame
from ui.colours import Colours
from ui.elements import make_button, make_text, confirm_button_image
from ui.router import Element, Screen
from ui.sounds import click_sound


class AIConfiguration(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.draw_background = True
        text = make_text("Difficulty", (650, 100), 50, Colours.GOLD.value)
        quit_button = make_button(650, 550, "Cancel", 75, reactive=True)
        easy_button = make_button(400, 175, "Easy", 20, image=confirm_button_image)
        hard_button = make_button(900, 175, "Hard", 20, image=confirm_button_image)

        for button in [quit_button, easy_button, hard_button]:
            self.button_array.append(button)

        for tuple in [text]:
            self.text_array.append(tuple)

    def handle_event(self, event, mouse, router):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.EASY_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                ai_easy = True
                return router.navigate_to("ai_play")
            if self.button_array[Element.HARD_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                ai_easy = False
                return router.navigate_to("ai_play")
            if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
