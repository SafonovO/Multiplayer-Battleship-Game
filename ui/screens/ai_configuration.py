import pygame
from game_manager import AIDifficulty
from ui.colours import Colours
from ui.elements import make_button, confirm_button_image
from ui.router import Element, Screen
from ui.sounds import click_sound
from ui.text import Text
from game_config import SHIP_COUNT, BOARD_SIZE


class AIConfiguration(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        text = Text("Difficulty", (650, 100), 50, Colours.GOLD.value)
        quit_button = make_button(650, 550, "Cancel", 75, reactive=True)
        easy_button = make_button(300, 175, "Easy", 20, image=confirm_button_image)
        med_button = make_button(650, 175, "Medium", 20, image=confirm_button_image)
        hard_button = make_button(1000, 175, "Hard", 20, image=confirm_button_image)

        for button in [quit_button, easy_button, med_button, hard_button]:
            self.button_array.append(button)

        for tuple in [text]:
            self.text_array.append(tuple)

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_array[Element.EASY_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                manager.create_ai_game(SHIP_COUNT, BOARD_SIZE, AIDifficulty.EASY)
                return router.navigate_to("placement")
            if self.button_array[Element.MED_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                manager.create_ai_game(SHIP_COUNT, BOARD_SIZE, AIDifficulty.MEDIUM)
                return router.navigate_to("placement")
            if self.button_array[Element.HARD_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                manager.create_ai_game(SHIP_COUNT, BOARD_SIZE, AIDifficulty.HARD)
                return router.navigate_to("placement")
            if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
