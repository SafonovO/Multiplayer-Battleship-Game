import asyncio
import sys
import time
from client import Client

import pygame
from pygame.locals import *
from pygame import mixer
from board.board import Board
from utilities.button import Button, ReactiveButton, TextButton
from utilities.fonts import get_font
from game_manager import BG, SCREEN, GameManager

pygame.init()
pygame.display.set_caption("Battleship")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
quit_button_image = pygame.image.load("assets/quit.png")
confirm_button_image = pygame.image.load("assets/ConfirmButton.png")


mixer.init()
mixer.music.load('Sounds/bg.ogg')
click_sound = pygame.mixer.Sound('Sounds/ui-click.mp3')

PLAYING_SURFACE = pygame.Rect(100, 50, 1100, 700)
BOARD_SIZE = 2
NUM_SHIPS = 2

def make_button(x, y, text, font_size, reactive=False, image=base_button_image):
    button = Button(image=image, pos=(x, y))
    if reactive:
        button = ReactiveButton(
            button,
            hover_surface=hovered_button_image,
            active_surface=hovered_button_image,
        )
    return TextButton(button, text=text, font=get_font(font_size))

async def placement(ship_count, game_size):
    # Track the orientation of the ship we are about to place
    # vertical = True by default
    vertical = True

    ships_left = ship_count

    # setup labels for the boards
    placement_board_label = get_font(30).render("Board Setup", True, "White")
    placement_board_label_rect = placement_board_label.get_rect(center=(425, 100))

    print(ai_easy)

    confirm_button = make_button(1000, 225, "Place", 20, image=confirm_button_image)
    quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)
    rotate_button = make_button(1000, 150, "Rotate", 20, image=confirm_button_image)

    ships_left_label = get_font(30).render("Ships Left: " + str(ships_left), True, "White")
    ships_left_label_rect = ships_left_label.get_rect(center=(1000, 100))

    while ships_left > 0:
        mouse = pygame.mouse.get_pos()
        # Draw the backgroudn
        SCREEN.blit(BG, (0, 0))
        # Draw the playing surface as described above
        pygame.draw.rect(SCREEN, "#042574", PLAYING_SURFACE)
        # Draw the labels
        SCREEN.blit(placement_board_label, placement_board_label_rect)
        # Draw the amount of ships left
        SCREEN.blit(ships_left_label, ships_left_label_rect)

        manager.update_placement()

        # draw the confirm button
        confirm_button.render(SCREEN, mouse)
        rotate_button.render(SCREEN, mouse)
        quit_button.render(SCREEN, mouse)

        # active cell is teh cell we are clicking on
        if manager.get_active_cell() != None:
            """
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
            """
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
                        click_sound.play()
                        # return to main menu
                        
                        await main()

                    # if we hit confirm, place with the manager
                    if manager.active_cell is not None and confirm_button.is_hovered(mouse):
                        click_sound.play()
                        successful_placement = await manager.place_ship(ships_left, vertical)
                        await asyncio.sleep(0.1)
                        # if the placement is successful, subtract the number of ships remaining.
                        if successful_placement:
                            ships_left -= 1

                        # update = True
                        coord_text = None
                        coord_text_rect = None
                        # update the count label
                        ships_left_label = get_font(30).render(
                            "Ships Left: " + str(ships_left), True, "White"
                        )

                    if rotate_button.is_hovered(mouse):
                        vertical = not vertical



async def select_opponent():
    play_button_ai = make_button(650, 150, "Play vs. AI", 50, reactive=True)
    play_button_human = make_button(650, 350, "Play vs. Human", 50, reactive=True)
    quit_button = make_button(650, 550, "QUIT", 75, reactive=True)

    loop = True
    while loop:
        mouse = pygame.mouse.get_pos()
        # Draw the backgroudn
        SCREEN.blit(BG, (0, 0))
        pygame.draw.rect(SCREEN, "#042574", PLAYING_SURFACE)
        play_button_ai.render(SCREEN, mouse)
        play_button_human.render(SCREEN, mouse)
        quit_button.render(SCREEN, mouse)
        pygame.display.flip()

        for event in pygame.event.get():
            # BUG: quit button is not responsive while waiting for AI to make move
            # probably due to sleep(1)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                global ai_game
                if play_button_ai.is_hovered(mouse):
                    click_sound.play()
                    ai_game = True
                    loop = False
                elif play_button_human.is_hovered(mouse):
                    click_sound.play()
                    ai_game = False
                    loop = False
                elif quit_button.is_hovered(mouse):
                    click_sound.play()
                    quit_game()



async def human_settings():
    global ai_game, create
    create_button = make_button(650, 150, "Create Game", 50, reactive=True)
    join_button = make_button(650, 350, "Join Game", 50, reactive=True)
    quit_button = make_button(650, 550, "QUIT", 75, reactive=True)

    loop = True
    while loop:
        mouse = pygame.mouse.get_pos()
        create_button.render(SCREEN, mouse)
        join_button.render(SCREEN, mouse)
        quit_button.render(SCREEN, mouse)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if create_button.is_hovered(mouse):
                    click_sound.play()
                    create = True
                    loop = False
                elif join_button.is_hovered(mouse):
                    click_sound.play()
                    create = False
                    loop = False
                elif quit_button.is_hovered(mouse):
                    click_sound.play()
                    quit_game()



async def AI_settings():
    global ai_easy

    text = get_font(50).render("Difficulty", True, "#b68f40")
    text_rect = text.get_rect(center=(650, 100))
    quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
    easy_button = make_button(400, 175, "Easy", 20, image=confirm_button_image)
    hard_button = make_button(900, 175, "Hard", 20, image=confirm_button_image)

    loop = True
    while loop:
        mouse = pygame.mouse.get_pos()
        # Draw the backgroudn
        SCREEN.blit(BG, (0, 0))
        pygame.draw.rect(SCREEN, "#042574", PLAYING_SURFACE)
        easy_button.render(SCREEN, mouse)
        hard_button.render(SCREEN, mouse)
        quit_button.render(SCREEN, mouse)

        SCREEN.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            # BUG: quit button is not responsive while waiting for AI to make move
            # probably due to sleep(1)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_hovered(mouse):
                    click_sound.play()
                    ai_easy = True
                    loop = False
                elif hard_button.is_hovered(mouse):
                    click_sound.play()
                    ai_easy = False
                    loop = False
                elif quit_button.is_hovered(mouse):
                    click_sound.play()
                    quit_game()



async def play():
    """
    the screen is 1700 wide and 800 tall.

    First, draw a gigantic rectangle to represent the playing surface.
    This rectangle should be 1500 wide and 700 tall. The background
    should be symmetrical around it, so its position should be at
    (100, 50)
    """

    # setup labels for the boards
    opponent_board_label = get_font(30).render("OPPONENT'S BOARD", True, "White")
    opponent_board_label_rect = opponent_board_label.get_rect(center=(425, 100))

    my_board_label = get_font(30).render("MY BOARD", True, "White")
    my_board_label_rect = my_board_label.get_rect(center=(1000, 325))

    confirm_button = make_button(1000, 250, "FIRE", 20, image=confirm_button_image)
    quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

    # Create text
    select_text = get_font(15).render("YOU HAVE SELECTED:", True, "White")
    select_text_rect = select_text.get_rect(center=(1000, 150))

    # Coord text
    coord_text = None
    coord_text_rect = None

    change_turn = False if ai_game or create else True
    # BUG: game freezes after first move until next turn for multiplayer
    # BUG: type of cell does not match opponent's board after guess for multiplayer
    # BUG: game does not notify winner after winning. need to end game.
    while not manager.game_over:
        mouse = pygame.mouse.get_pos()

        # Draw the backgroudn
        SCREEN.blit(BG, (0, 0))

        # Draw the playing surface as described above
        pygame.draw.rect(SCREEN, "#042574", PLAYING_SURFACE)

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
            """
            We have selected a cell.

            First, display the cell as text on screen.

            If the user then clicks FIRE, we call the game
            manager to execute the fire
            """
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
                        click_sound.play()
                        # return to main menu
                        await main()
                    
                    # if we hit confirm, fire with the manager
                    if confirm_button.is_hovered(mouse):
                        if manager.active_cell!=None:
                            change_turn = await manager.fire_shot()
                            # update = True
                            coord_text = None
                            coord_text_rect = None
                            # await asyncio.sleep(0.7)
    # outside of while not manager.game_over
    if manager.client:
        manager.client.end_game(manager.won)

async def main_menu():
    # The loop for the main menu
    # render menu text, buttons
    text = get_font(100).render("BATTLESHIP", True, "#b68f40")
    text_rect = text.get_rect(center=(650, 150))

    play_button = make_button(650, 350, "PLAY", 75, reactive=True)
    quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
    loop = True
    while loop:
        # Draw the background
        SCREEN.blit(BG, (0, 0))
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(text, text_rect)

        for button in [play_button, quit_button]:
            button.render(SCREEN, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_hovered(mouse):
                    click_sound.play()
                    loop = False
                if quit_button.is_hovered(mouse):
                    click_sound.play()
                    quit_game()

        pygame.display.update()



def endgamescreen(won):
    text = get_font(100).render(
        "Congratulations, you won!" if won else "You lost, try again...",
        True,
        "#b68f40",
    )
    text_rect = text.get_rect(center=(650, 100))
    quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(text, text_rect)
        for button in [quit_button]:
            button.render(SCREEN, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_hovered(mouse):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()



async def main():
    global ai_game, ai_easy, create, manager
    ai_game = True
    ai_easy = None
    create = False
    manager = GameManager()

    await main_menu()
    await select_opponent()
    if ai_game:
        await AI_settings()
    else:
        await human_settings()
    await manager.create_game(
        ai_game=ai_game,
        ship_count=NUM_SHIPS,
        game_size=BOARD_SIZE,
        create=create,
        easy_ai = ai_easy
    )
    await asyncio.sleep(0.1)
    await placement(NUM_SHIPS, BOARD_SIZE)
    await play() # loops forever
    endgamescreen(manager.won)




def quit_game():
    pygame.quit()
    sys.exit()

mixer.music.play(-1)
asyncio.run(main())

