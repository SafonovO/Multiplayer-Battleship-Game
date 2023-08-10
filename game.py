import asyncio
import pygame
import signal
from board.board import Board
from game_manager import GameManager
from pygame.locals import *
from ui.screens.all import (
    AIConfiguration,
    Endgame,
    Error,
    MainMenu,
    OnlineCreatePending,
    OnlineGameOptions,
    OnlineJoin,
    Placement,
    Play,
    SelectOpponent,
)
from ui.router import Router

MAX_FRAME_RATE = 80

pygame.init()
pygame.display.set_caption("Battleship")

pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/bg.ogg")


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
            pass
    # outside of while not manager.game_over
    if manager.client:
        manager.client.end_game(manager.won)


async def game_loop(stop: asyncio.Future, router: Router):
    try:
        while not stop.done():
            await router.render()
            # the following line is required to allow asyncio operations to proceed alongside the game loop
            await asyncio.sleep(1 / MAX_FRAME_RATE)
    except SystemExit:
        pass


async def main():
    loop = asyncio.get_event_loop()
    start_client = asyncio.Event()
    stop = loop.create_future()

    manager = GameManager()
    router = Router(
        manager,
        start_client,
        stop,
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
            "error": Error,
        },
    )
    router.navigate_to("main_menu")

    loop.add_signal_handler(signal.SIGINT, router.quit_game)

    try:
        asyncio.create_task(game_loop(stop, router))
        await start_client.wait()
        if not stop.done():
            asyncio.create_task(manager.start_client(stop))
            await stop
    finally:
        loop.remove_signal_handler(signal.SIGINT)


if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    asyncio.run(main())
