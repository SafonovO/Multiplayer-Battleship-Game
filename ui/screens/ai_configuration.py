import pygame
from game_manager import AIDifficulty
from ui.colours import Colours
from ui.elements import make_button, confirm_button_image
from ui.router import Screen
from ui.sounds import click_sound
from ui.text import Text
from game_config import SHIP_COUNT, BOARD_SIZE


class AIConfiguration(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        text = Text("Difficulty", (650, 100), 50, Colours.GOLD.value)
        self.quit_button = make_button(650, 550, "Cancel", 75, reactive=True)
        self.easy_button = make_button(300, 175, "Easy", 20, image=confirm_button_image)
        self.med_button = make_button(650, 175, "Medium", 20, image=confirm_button_image)
        self.hard_button = make_button(1000, 175, "Hard", 20, image=confirm_button_image)

        self.button_array = [self.quit_button, self.easy_button, self.med_button, self.hard_button]
        self.text_array = [text]

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.easy_button.is_hovered(mouse):
                click_sound.play()
                manager.create_ai_game(SHIP_COUNT, BOARD_SIZE, AIDifficulty.EASY)
                return router.navigate_to("placement")
            if self.med_button.is_hovered(mouse):
                click_sound.play()
                manager.create_ai_game(SHIP_COUNT, BOARD_SIZE, AIDifficulty.MEDIUM)
                return router.navigate_to("placement")
            if self.hard_button.is_hovered(mouse):
                click_sound.play()
                manager.create_ai_game(SHIP_COUNT, BOARD_SIZE, AIDifficulty.HARD)
                return router.navigate_to("placement")
            if self.quit_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
