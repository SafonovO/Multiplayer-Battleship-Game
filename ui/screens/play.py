import string
import pygame
from board.board import Board
from ui.colours import Colours
from ui.elements import make_button, make_text, confirm_button_image, quit_button_image
from ui.router import Element, Screen
from ui.sounds import click_sound


class Play(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.draw_background = True
        self.selected_coords = ()

        opponent_board_label = make_text("OPPONENT'S BOARD", (425, 100), 30, Colours.WHITE.value)
        my_board_label = make_text("MY BOARD", (1000, 325), 30, Colours.WHITE.value)
        select_text = make_text("YOU HAVE SELECTED:", (1000, 150), 15, Colours.WHITE.value)

        fire_button = make_button(1000, 250, "FIRE", 20, image=confirm_button_image)
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        for tuple in [opponent_board_label, my_board_label, select_text, None]:
            self.text_array.append(tuple)

        for button in [quit_button, fire_button]:
            self.button_array.append(button)

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
            displayed_coords = f"({string.ascii_uppercase[cell_coords[0]]}, {cell_coords[1] + 1})"
            coord_text = make_text(displayed_coords, (1000, 200), 15, Colours.WHITE.value)
            self.text_array[3] = coord_text

    def handle_event(self, event, mouse, router, manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if we clicked a cell or something else
            if not manager.set_active_cell(mouse):
                if self.button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    return router.navigate_to("main_menu")

                # if we hit confirm, fire with the manager
                if self.button_array[Element.FIRE_BUTTON.value].is_hovered(mouse):
                    if manager.active_cell != None:
                        change_turn = manager.fire_shot_new()
                        # update = True
                        self.text_array[3] = None
                        if manager.game_over:
                            return router.navigate_to("endgame")
                        # await asyncio.sleep(0.7)
