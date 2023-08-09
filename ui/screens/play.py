import string
import pygame
from ui.colours import Colours
from ui.elements import make_button, confirm_button_image, quit_button_image
from ui.router import Screen
from ui.sounds import click_sound
from ui.text import Text


class Play(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True
        self.selected_coords = ()

        opponent_board_label = Text("OPPONENT'S BOARD", (425, 100), 30, Colours.WHITE.value)
        my_board_label = Text("MY BOARD", (1000, 325), 30, Colours.WHITE.value)
        select_text = Text("YOU HAVE SELECTED:", (1000, 150), 15, Colours.WHITE.value)
        self.coord_text = Text("", (1000, 200), 15, Colours.WHITE.value)

        self.fire_button = make_button(1000, 250, "FIRE", 20, image=confirm_button_image)
        self.quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        self.text_array = [opponent_board_label, my_board_label, select_text, self.coord_text]
        self.button_array = [self.quit_button, self.fire_button]

    def render(self, manager):
        manager.update_boards()
        if manager.get_active_cell() != None:
            """
            We have selected a cell.

            First, display the cell as text on screen.

            If the user then clicks FIRE, we call the game
            manager to execute the fire
            """
            cell_coords = manager.get_active_cell().coordinates
            self.coord_text.value = f"({string.ascii_uppercase[cell_coords[0]]}, {cell_coords[1] + 1})"

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if we clicked a cell or something else
            if not manager.set_active_cell(mouse):
                if self.quit_button.is_hovered(mouse):
                    click_sound.play()
                    return router.navigate_to("main_menu")

                # if we hit confirm, fire with the manager
                if self.fire_button.is_hovered(mouse):
                    if manager.active_cell != None:
                        change_turn = manager.fire_shot_new()
                        self.coord_text.value = ""
                        if manager.game_over:
                            return router.navigate_to("endgame")
