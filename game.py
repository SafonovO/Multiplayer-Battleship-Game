import asyncio
import signal
import sys

import pygame
from pygame.locals import *
from pygame import mixer
from board.board import Board
from ui.button import Button, ReactiveButton, TextButton
from ui.fonts import get_font
from ui.input import Input
from ui.screens.all import (
    AIConfiguration,
    Endgame,
    MainMenu,
    OnlineCreatePending,
    OnlineGameOptions,
    OnlineJoin,
    Placement,
    Play,
    SelectOpponent,
)
from game_manager import BG, SCREEN, GameManager
from ui.router import button_array, Element, Router
from utilities import quit_game

MAX_FRAME_RATE = 80

pygame.init()
pygame.display.set_caption("Battleship")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
quit_button_image = pygame.image.load("assets/quit.png")
confirm_button_image = pygame.image.load("assets/ConfirmButton.png")

mixer.init()
mixer.music.load("assets/sounds/bg.ogg")
click_sound = pygame.mixer.Sound("assets/sounds/ui-click.mp3")

PLAYING_SURFACE = pygame.Rect(100, 50, 1100, 700)
BOARD_SIZE = 5
NUM_SHIPS = 5


def make_button(x, y, text, font_size, reactive=False, image=base_button_image):
    button = Button(image=image, pos=(x, y))
    if reactive:
        button = ReactiveButton(
            button,
            hover_surface=hovered_button_image,
            active_surface=hovered_button_image,
        )
    return TextButton(button, text=text, font=get_font(font_size))


async def play():
    draw.clear_array()
    """
    the screen is 1700 wide and 800 tall.

    First, draw a gigantic rectangle to represent the playing surface.
    This rectangle should be 1500 wide and 700 tall. The background
    should be symmetrical around it, so its position should be at
    (100, 50)
    """

    draw.draw_screen("play")

    change_turn = False if ai_game or create else True

    # if hardAI game, allow it to peek into your array
    if ai_game and ai_level == 2:
        manager.hard_ai_setup()

    # BUG: game freezes after first move until next turn for multiplayer
    # BUG: type of cell does not match opponent's board after guess for multiplayer
    # BUG: game does not notify winner after winning. need to end game.
    while not manager.game_over:
        mouse = pygame.mouse.get_pos()

        draw.render_screen(mouse, playing_surface=True)

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
            draw.draw_coord(num, letter)

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
                        if manager.active_cell != None:
                            change_turn = await manager.fire_shot()
                            # update = True
                            draw.clear_coord()
                            # await asyncio.sleep(0.7)
    # outside of while not manager.game_over
    if manager.client:
        manager.client.end_game(manager.won)


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


async def old_main():
    global manager

    # FIXME: migrate to new UI structure and remove this chunk of dead code
    # await main_menu()
    # await select_opponent()
    # if ai_game:
    #     await AI_settings()
    # else:
    #     await human_settings()
    # await manager.create_game(
    #     ai_game=ai_game, ship_count=NUM_SHIPS, game_size=BOARD_SIZE, create=create, easy_ai=ai_easy
    # )
    # await asyncio.sleep(0.1)
    # if not ai_game:
    #     if create:
    #         await human_game_pending()
    #     else:
    #         code = await human_game_join()
    #         manager.client.join_game(code)
    # await asyncio.sleep(0.1)  # everything breaks if you remove this line
    # await placement(NUM_SHIPS, BOARD_SIZE)
    # await play()  # loops forever
    # endgamescreen(manager.won)


async def game_loop(stop: asyncio.Event, router: Router):
    while not stop.is_set():
        router.render()
        # the following line is required to allow asyncio operations to proceed alongside the game loop
        await asyncio.sleep(1 / MAX_FRAME_RATE)


async def main():
    manager = GameManager()
    router = Router(
        manager,
        {
            "main_menu": MainMenu,
            "select_opponent": SelectOpponent,
            "ai_configuration": AIConfiguration,
            "online_game_options": OnlineGameOptions,
            "online_create_pending": OnlineCreatePending,
            "online_join": OnlineJoin,
            "placement": Placement,
            "play": Play,
            "endgame": Endgame,
        },
    )
    router.navigate_to("main_menu")

    loop = asyncio.get_event_loop()
    stop = asyncio.Event()
    loop.add_signal_handler(signal.SIGINT, keyboard_interrupt, stop)

    try:
        await asyncio.gather(manager.start_client(stop), game_loop(stop, router))
    except asyncio.CancelledError:
        pass
    except SystemExit:
        pass
    finally:
        loop.remove_signal_handler(signal.SIGINT)


def keyboard_interrupt(stop: asyncio.Event):
    stop.set()
    quit_game()


if __name__ == "__main__":
    mixer.music.play(-1)
    asyncio.run(main())
