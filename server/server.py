import asyncio
import json
import logging
import random
import signal
import string
import uuid
import websockets.server
import websockets.exceptions

ADDRESS = "0.0.0.0"
PORT = "8765"
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s - %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Player:
    def __init__(self):
        self.guessed = []
        self.ships = []
        self.next_guess = None
        self.result = None
        self.socket: websockets.server.WebSocketServerProtocol | None = None


class Game:
    def __init__(self, ship_count: int, board_size: int):
        self.logger = logging.getLogger("battleship.game")
        self.id = str(uuid.uuid4())
        self.players: tuple[Player, Player] = (Player(), Player())
        self.password = Game.generate_pw()
        self.ship_count = ship_count
        self.board_size = board_size
        self.logger.info(f"Game created, id {self.id} password {self.password}")
        self.turn = 0

    def generate_pw():
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for i in range(9))
    
    def is_empty(self):
        return self.players[0].socket == None and self.players[1].socket == None


class Server:
    """
    {
        "request": request,
        "game": game,
        "player": player,
        "details": details
    }
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("battleship.server")
        self.games: dict[str, Game] = {}
        self.queues: list[asyncio.Queue] = []
        self.tasks = []
        self.clients = set()
        self.socket_to_player: dict[websockets.server.WebSocketServerProtocol, Player] = {}
        self.code_to_game: dict[str, Game] = {}
        self.player_to_game: dict[Player, Game] = {}

    def create_message(self, request="ok", response="ok"):
        return {"request": request, "response": response}

    async def handler(self, websocket: websockets.server.WebSocketServerProtocol):
        self.logger.info("Incoming client")
        self.clients.add(websocket)
        try:
            # each worker has it's own queue
            new_worker = asyncio.Queue()
            worker_id = len(self.queues)
            task = asyncio.create_task(self.worker(websocket, worker_id))
            self.tasks.append(task)
            self.queues.append(new_worker)
            while True:
                self.logger.debug("Ready to handle next request from client")
                packet = await websocket.recv()
                self.queues[worker_id].put_nowait(packet)
        except websockets.exceptions.ConnectionClosedOK:
            self.logger.info("Client quit")
        except websockets.exceptions.ConnectionClosedError:
            self.logger.info("Client quit unexpectedly")
        finally:
            self.logger.info("Removing client")
            self.clients.remove(websocket)
            socket_player = self.socket_to_player.get(websocket)
            if socket_player:
                socket_player.socket = None
                del self.socket_to_player[websocket]
                game = self.player_to_game.get(socket_player)
                if game != None:
                    del self.player_to_game[socket_player]

    async def worker(self, websocket: websockets.server.WebSocketServerProtocol, workerID: int):
        while True:
            self.logger.debug(f"worker {workerID} is awaiting task")
            packet = await self.queues[workerID].get()
            self.logger.debug(f"worker id: {workerID} packet: {packet}")
            msg: dict = json.loads(packet)
            request = msg.get("request")
            player = self.socket_to_player.get(websocket)
            if player != None:
                game = self.player_to_game.get(game)
            details = msg.get("details")
            match request:
                # create a new game
                case "new_game":
                    game = Game(msg.get("ship_count"), msg.get("board_size"))
                    game.players[0].socket = websocket
                    self.socket_to_player[websocket] = game.players[0]
                    self.games[game.id] = game
                    self.code_to_game[game.password] = game
                    self.player_to_game[game.players[0]] = game
                    response = {
                        "request": "new_game",
                        "game_id": game.id,
                        "password": game.password,
                    }
                    await websocket.send(json.dumps(response))

                case "join_game":
                    game = self.code_to_game.get(msg.get("game_code"))
                    if game == None:
                        self.logger.debug("No such game")
                        await websocket.send(json.dumps({"request": "new_game", "error": "Invalid invite code"}))
                        return
                    if game.players[0].socket != None and game.players[1].socket != None:
                        self.logger.debug("Game is full")
                        return
                    available_slot = -1
                    if game.players[1].socket == None:
                        available_slot = 1
                    if game.players[0].socket == None:
                        available_slot = 0
                    self.socket_to_player[websocket] = game.players[available_slot]
                    game.players[available_slot].socket = websocket
                    response = {
                        "request": "new_game",
                        "game_id": game.id,
                        "password": game.password,
                    }
                    await websocket.send(json.dumps(response))
                    if game.players[0].socket != None and game.players[1].socket != None:
                        self.logger.debug("Game starting, notifying clients")
                        response = {"request": "ready_for_placement"}
                        response_json = json.dumps(response)
                        await game.players[0].socket.send(response_json)
                        await game.players[1].socket.send(response_json)
                    else:
                        self.logger.debug("Still waiting for both players...")

                case "set_placement":
                    pass

                # join first empty game
                # might need to return error if no empty games, then create game instead
                case "joinrandom":
                    pass

                case "getguess":
                    guess = await self.get_guess(game_id, player_id ^ 1)
                    response = self.create_message("getguess", guess)
                    await websocket.send(json.dumps(response))

                case "getresult":
                    result = await self.get_result(game_id, player_id)
                    response = self.create_message("getresult", result)
                    await websocket.send(json.dumps(response))
                    self.games[game_id].players[player_id].result = None

                case "setresult":
                    self.games[game_id].players[player_id ^ 1].result = details
                    response = self.create_message()
                    await websocket.send(json.dumps(response))

                case "setguess":
                    self.games[game_id].players[player_id].next_guess = details
                    print("set guess as", details)
                    response = self.create_message()
                    await websocket.send(json.dumps(response))

                case "broadcast":
                    broadcast = self.create_message("broadcast")
                    for player in self.games[game_id].players:
                        await player.socket.send(json.dumps(broadcast))

                case "endgame":
                    # tell player_id ^ 1 that they lost
                    # games[game_id] = None
                    broadcast = self.create_message("endgame")
                    for player in self.games[game_id].players:
                        await player.socket.send(json.dumps(broadcast))

                case "identify":
                    await websocket.send(json.dumps({"request": "identify", "response": "hello"}))

                case _:
                    self.logger.debug("Invalid request")

            self.queues[workerID].task_done()

    async def get_guess(self, game_id, player_id):
        while not self.games[game_id].players[player_id].next_guess:
            # wait for the player to guess
            await asyncio.sleep(0.1)
        return self.games[game_id].players[player_id].next_guess

    async def get_result(self, game_id, player_id):
        while self.games[game_id].players[player_id].result == None:
            # wait for the opponent to validate the guess
            await asyncio.sleep(0.1)
        return self.games[game_id].players[player_id].result


async def main():
    server = Server()

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)

    async with websockets.server.serve(server.handler, ADDRESS, PORT, ping_interval=None):
        await stop  # run forever

    logging.info("Cancelling worker tasks...")
    # Cancel our worker tasks.
    for task in server.tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*server.tasks, return_exceptions=True)


if __name__ == "__main__":
    logging.info("Starting server...")
    asyncio.run(main())
