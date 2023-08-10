import asyncio
import pygame
import signal
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
    OnlinePlacementPending,
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
            "online_placement_pending": OnlinePlacementPending,
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
