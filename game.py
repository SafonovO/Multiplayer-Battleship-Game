import asyncio
import sys
import time
from client import Client

import pygame
from board.board import Board
from utilities.button import Button, ReactiveButton, TextButton
from utilities.fonts import get_font
from game_manager import BG, SCREEN, GameManager



pygame.init()
pygame.display.set_caption("Menu")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")

manager = GameManager()
ai_game = True
join = False
create = False
# run = False
server = None


async def placement(ship_count, game_size):
    # Track the orientation of the ship we are about to place
    # vertical = True by default
    vertical = True

    ships_left = ship_count
    playing_surface = pygame.Rect(100, 50, 1100, 700)

    # setup labels for the boards
    placement_board_label = get_font(30).render("Board Setup", True, "White")
    placement_board_label_rect = placement_board_label.get_rect(center=(425, 100))

    # create a game using the manager
    await manager.create_game(ai_game=ai_game,ship_count=ship_count,game_size= game_size, create=create, join=join)

    # Create a confirm button
    confirm_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 225))
    confirm_button = TextButton(confirm_button, text="Place", font=get_font(20))

    # Make a quit button
    quit_button = Button(image=pygame.image.load("assets/quit.png"), pos=(1000, 25))
    quit_button = TextButton(quit_button, text="QUIT", font=get_font(20))

    ships_left_label = get_font(30).render("Ships Left: " + str(ships_left), True, "White")
    ships_left_label_rect = ships_left_label.get_rect(center=(1000, 100))

    # make a rotate button
    vertical_orientation = True
    rotate_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 150))
    rotate_button = TextButton(rotate_button, text="Rotate", font=get_font(20))

    while ships_left > 0:
        mouse = pygame.mouse.get_pos()

        # Draw the backgroudn
        SCREEN.blit(BG, (0, 0))

        # Draw the playing surface as described above
        pygame.draw.rect(SCREEN, "#042574", playing_surface)

        # Draw the labels
        SCREEN.blit(placement_board_label, placement_board_label_rect)

        # Draw the amount of ships left

        SCREEN.blit(ships_left_label,ships_left_label_rect)

        manager.update_placement()

        # draw the confirm button
        confirm_button.render(SCREEN, mouse)
        rotate_button.render(SCREEN, mouse)
        quit_button.render(SCREEN, mouse)

        # active cell is teh cell we are clicking on
        if manager.get_active_cell() != None:
            '''
            We have selected a cell.

            First, display the cell as text on screen.

            If the user then clicks FIRE, we call the game
            manager to execute the fire

            Here, I want to draw all the cells that will be occupied
            by the ship i'm about to place.

            IF there is a conflict, i will draw  the ship's cells in red
            if there is no conflict, the ship will be drawn in green

            there is a conflict IF:
                - one or more cells that this ship will occupy is already
                occupied by some ship
                - one or more cells that this ship will occupy exceeds the
                boundaries of the board

            If the user attempts to place a ship in an invlaid position,
            simply do nothing
            '''
            manager.preview_ship(ships_left, vertical)


        pygame.display.flip()


        for event in pygame.event.get():
            # BUG: quit button is not responsive while waiting for AI to make move
            # probably due to sleep(1)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if we clicked a cell or something else
                if not manager.set_active_cell_placement(mouse):
                    if quit_button.is_hovered(mouse):
                        # return to main menu
                        await main_menu()

                    # if we hit confirm, fire with the manager
                    if manager.active_cell is not None and confirm_button.is_hovered(mouse):
                        successful_placement = manager.place_ship(ships_left, vertical)

                        # if the placement is successful, subtract the number of ships remaining.
                        if successful_placement:
                            ships_left -= 1

                        # update = True
                        coord_text = None
                        coord_text_rect = None
                        # update the count label
                        ships_left_label = get_font(30).render("Ships Left: " + str(ships_left), True, "White")

                    if rotate_button.is_hovered(mouse):
                        vertical = not vertical
    await play()


async def play():

    '''
    the screen is 1700 wide and 800 tall.

    First, draw a gigantic rectangle to represent the playing surface.
    This rectangle should be 1500 wide and 700 tall. The background
    should be symmetrical around it, so its position should be at
    (100, 50)
    '''

    playing_surface = pygame.Rect(100, 50, 1100, 700)

    # setup labels for the boards
    opponent_board_label = get_font(30).render("OPPONENT'S BOARD", True, "White")
    opponent_board_label_rect = opponent_board_label.get_rect(center=(425, 100))

    my_board_label = get_font(30).render("MY BOARD", True, "White")
    my_board_label_rect = my_board_label.get_rect(center=(1000, 325))

    # Create a confirm button
    confirm_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 250))
    confirm_button = TextButton(confirm_button, text="FIRE", font=get_font(20))

    # Create text
    select_text = get_font(15).render("YOU HAVE SELECTED:", True, "White")
    select_text_rect = select_text.get_rect(center=(1000, 150))

    # Coord text
    coord_text = None
    coord_text_rect = None


    # Make a quit button
    quit_button = Button(image=pygame.image.load("assets/quit.png"), pos=(1000, 25))
    quit_button = TextButton(quit_button, text="QUIT", font=get_font(20))

    change_turn = True if join else False
# BUG: game freezes after first move until next turn for multiplayer
# BUG: type of cell does not match opponent's board after guess for multiplayer
# BUG: game does not notify winner after winning. need to end game.
    while True:
        mouse = pygame.mouse.get_pos()

        # Draw the backgroudn
        SCREEN.blit(BG, (0, 0))

        # Draw the playing surface as described above
        pygame.draw.rect(SCREEN, "#042574", playing_surface)

        # Draw the labels
        SCREEN.blit(opponent_board_label, opponent_board_label_rect)
        SCREEN.blit(my_board_label, my_board_label_rect)

        SCREEN.blit(select_text, select_text_rect)

        manager.update_boards()

        # draw the confirm button
        confirm_button.render(SCREEN, mouse)

        quit_button.render(SCREEN, mouse)

        # draw the coord text if it is not None
        if coord_text != None and coord_text_rect != None:
            SCREEN.blit(coord_text, coord_text_rect)

        # active cell is teh cell we are clicking on
        if manager.get_active_cell() != None:
            '''
            We have selected a cell.

            First, display the cell as text on screen.

            If the user then clicks FIRE, we call the game
            manager to execute the fire
            '''
            cell_coords = manager.get_active_cell().coordinates
            letter = Board.letters[cell_coords[0]]
            num = cell_coords[1] + 1

            coord_text = get_font(15).render("({}, {})".format(letter, num), True, "White")
            coord_text_rect = coord_text.get_rect(center=(1000, 200))

        pygame.display.flip()

        if manager.client:
            await asyncio.sleep(0.1)

        if change_turn:
            change_turn = False
            await manager.change_turn()
            continue

        for event in pygame.event.get():
            # BUG: quit button is not responsive while waiting for AI to make move
            # probably due to sleep(1)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if we clicked a cell or something else
                if not manager.set_active_cell(mouse):
                    if quit_button.is_hovered(mouse):
                        # return to main menu
                        await main_menu()

                    # if we hit confirm, fire with the manager
                    if confirm_button.is_hovered(mouse):
                        change_turn = await manager.fire_shot()
                        # update = True
                        coord_text = None
                        coord_text_rect = None

'''
def setup():
    # Ship setup screen

    # Render text
    text = get_font(70).render("SETUP YOUR SHIPS", True, "White")
    text_rect = text.get_rect(center=(650, 100))

    # Placeholder text for now
    placeholder1_text = get_font(24).render("This function has not been implemented yet for this prototype.", True,
                                            "White")
    placeholder2_text = get_font(24).render("Please continue to game.", True, "White")
    placeholder3_text = get_font(24).render("All ships will be 1x1 and placed randomly", True, "White")

    placeholder1_rect = placeholder1_text.get_rect(center=(650, 300))
    placeholder2_rect = placeholder2_text.get_rect(center=(650, 350))
    placeholder3_rect = placeholder3_text.get_rect(center=(650, 400))

    # Continue to gameplay button
    continue_button = Button(image=base_button_image, pos=(650, 550))
    continue_button = TextButton(continue_button, text="CONTINUE", font=get_font(60))

    while True:
        # paint background
        SCREEN.blit(BG, (0, 0))

        # get mouse position
        mouse = pygame.mouse.get_pos()

        SCREEN.blit(text, text_rect)

        SCREEN.blit(placeholder1_text, placeholder1_rect)
        SCREEN.blit(placeholder2_text, placeholder2_rect)
        SCREEN.blit(placeholder3_text, placeholder3_rect)

        continue_button.render(SCREEN, mouse)

        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            # if we clicked, find out if we clicked on a button and execute that buttons action
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.is_hovered(mouse):
                    placement(ship_count=5, game_size = 5)

        pygame.display.update()

'''

async def main_menu():
    # The loop for the main menu
    # render menu text, buttons
    text = get_font(100).render("BATTLESHIP", True, "#b68f40")
    text_rect = text.get_rect(center=(650, 100))

    play_button = Button(image=base_button_image, pos=(650, 250))
    play_button = ReactiveButton(play_button, hover_surface=hovered_button_image,
                                 active_surface=hovered_button_image)
    play_button = TextButton(play_button, text="PLAY", font=get_font(75))

    quit_button = Button(image=base_button_image, pos=(650, 550))
    quit_button = ReactiveButton(quit_button, hover_surface=hovered_button_image,
                                 active_surface=hovered_button_image)
    quit_button = TextButton(quit_button, text="QUIT", font=get_font(75))

    while True:
        # Draw the background
        SCREEN.blit(BG, (0, 0))

        # Get mouse position
        mouse = pygame.mouse.get_pos()

        # draw meny text, buttons
        SCREEN.blit(text, text_rect)

        for button in [play_button, quit_button]:
            button.render(SCREEN, mouse)

        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            
            if event.type == pygame.KEYDOWN:
                global ai_game, create, join
                if event.key == pygame.K_c:
                    ai_game = False
                    create = True
                    join = False
                if event.key == pygame.K_j:
                    ai_game = False
                    join = True
                    create = False

            # if we clicked, find out if we clicked on a button and execute that buttons action
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_hovered(mouse):
                    await placement(8, 8)

                if quit_button.is_hovered(mouse):
                    quit_game()

        pygame.display.update()


def quit_game():
    pygame.quit()
    sys.exit()

asyncio.run(main_menu())
# main_menu()
