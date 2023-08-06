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
from drawer import Drawer, button_array,Element

pygame.init()
pygame.display.set_caption("Battleship")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
quit_button_image = pygame.image.load("assets/quit.png")
confirm_button_image = pygame.image.load("assets/ConfirmButton.png")

manager = GameManager()
draw = Drawer()
ai_game = True
create = False
# run = False
ai_easy = None
mixer.init()
mixer.music.load('Sounds/bg.ogg')
click_sound = pygame.mixer.Sound('Sounds/ui-click.mp3')

PLAYING_SURFACE = pygame.Rect(100, 50, 1100, 700)


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
    draw.clear_array()
    # Track the orientation of the ship we are about to place
    # vertical = True by default
    vertical = True

    ships_left = ship_count

    

    # create a game using the manager
    print(ai_easy)
    await manager.create_game(
        ai_game=ai_game,
        ship_count=ship_count,
        game_size=game_size,
        create=create,
        easy_ai = ai_easy
    )
    draw.draw_screen('placement',ships_left=ships_left)
    

    while ships_left > 0:
        mouse = pygame.mouse.get_pos()

        
        draw.render_screen(mouse, playing_surface=True)
        manager.update_placement()
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
                    if button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                        click_sound.play()
                        # return to main menu
                        
                        await main()

                    # if we hit confirm, place with the manager
                    if manager.active_cell is not None and button_array[Element.CONFIRM_BUTTON.value].is_hovered(mouse):
                        click_sound.play()
                        successful_placement = await manager.place_ship(ships_left, vertical)
                        await asyncio.sleep(0.1)
                        # if the placement is successful, subtract the number of ships remaining.
                        if successful_placement:
                            ships_left -= 1

                        # update = True
                        draw.clear_coord()
                        # update the count label
                        draw.update_ships_left(ships_left)

                    if button_array[Element.ROTATE_BUTTON.value].is_hovered(mouse):
                        vertical = not vertical



async def select_opponent():
    draw.clear_array()
    draw.draw_screen('select_opponent')
    loop = True
    while loop:
        mouse = pygame.mouse.get_pos()
        # Draw the backgroudn
        draw.render_screen(mouse,playing_surface=True)
        pygame.display.flip()

        for event in pygame.event.get():
            # BUG: quit button is not responsive while waiting for AI to make move
            # probably due to sleep(1)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                global ai_game
                if button_array[Element.AI_PLAY_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    ai_game = True
                    loop = False
                elif button_array[Element.PLAY_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    ai_game = False
                    loop = False
                elif button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    quit_game()



async def human_settings():
    draw.clear_array()
    global ai_game, create
    draw.draw_screen('human_settings')
    loop = True
    while loop:
        
        mouse = pygame.mouse.get_pos()
        draw.render_screen(mouse)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_array[Element.CREATE_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    create = True
                    loop = False
                elif button_array[Element.JOIN_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    create = False
                    loop = False
                elif button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    quit_game()



async def AI_settings():
    draw.clear_array()
    global ai_easy
    draw.draw_screen('AI_settings')
    
    loop = True
    while loop:
        mouse = pygame.mouse.get_pos()
        # Draw the backgroudn
        draw.render_screen(mouse,playing_surface=True)
        pygame.display.flip()

        for event in pygame.event.get():
            # BUG: quit button is not responsive while waiting for AI to make move
            # probably due to sleep(1)
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_array[Element.EASY_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    ai_easy = True
                    loop = False
                elif button_array[Element.HARD_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    ai_easy = False
                    loop = False
                elif button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    quit_game()

async def play():
    draw.clear_array()
    """
    the screen is 1700 wide and 800 tall.

    First, draw a gigantic rectangle to represent the playing surface.
    This rectangle should be 1500 wide and 700 tall. The background
    should be symmetrical around it, so its position should be at
    (100, 50)
    """

    draw.draw_screen('play')

    change_turn = False if ai_game or create else True
    # BUG: game freezes after first move until next turn for multiplayer
    # BUG: type of cell does not match opponent's board after guess for multiplayer
    while True:
        mouse = pygame.mouse.get_pos()

        draw.render_screen(mouse,playing_surface=True)

        manager.update_boards()

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
            draw.draw_coord(num,letter)
        
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
                    if button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                        click_sound.play()
                        # return to main menu
                        await main()
                    
                    # if we hit confirm, fire with the manager
                    if button_array[Element.FIRE_BUTTON.value].is_hovered(mouse):
                        if manager.active_cell!=None:
                            change_turn = await manager.fire_shot()
                            # update = True
                            
                            if (change_turn):
                                winner = await manager.endgame()
                                print(winner)
                                if(winner!=0):
                                    print('passed')
                                    await endgame(winner)
                            draw.clear_coord()
                            await asyncio.sleep(0.3)

async def endgame(won):
    draw.clear_array()
    draw.draw_screen('endgame',winner=won)
    while True:
        mouse = pygame.mouse.get_pos()
        draw.render_screen(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()   

async def main_menu():
    draw.clear_array()
    # The loop for the main menu
    # render menu text, buttons
    draw.draw_screen('main')
    loop = True
    while loop:
        # Draw the background
        mouse = pygame.mouse.get_pos()
        draw.render_screen(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_array[Element.PLAY_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    loop = False
                if button_array[Element.QUIT_BUTTON.value].is_hovered(mouse):
                    click_sound.play()
                    quit_game()

        pygame.display.update()



async def main():
    global ai_game, ai_easy, create
    ai_game = True
    ai_easy = None
    create = False
    await main_menu()
    await select_opponent()
    if ai_game:
        await AI_settings()
    else:
        await human_settings()
    await placement(5, 5)
    await play() # loops forever




def quit_game():
    pygame.quit()
    sys.exit()

mixer.music.play(-1)
asyncio.run(main())

