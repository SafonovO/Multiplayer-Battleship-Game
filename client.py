import asyncio
import json
from time import sleep
import websockets

URI = "ws://24.199.115.192:8765"
URI = "ws://127.0.0.1:8765"
# URI = "ws://209.87.58.21:8765"


class Client:
    def __init__(self) -> None:
        self.game_id = None
        self.player_id = None
        self.requests = asyncio.Queue()
        self.response = []
        self.opp_guess = None
        self.my_result = None
        self.won = False
        self.game_over = False

    def create_message(self, request, details=""):
        return {
            "request": request,
            "game": self.game_id if self.game_id is not None else "-1",
            "player": self.player_id if self.player_id is not None else "-1",
            "details": details,
        }

    async def start(self):
        print("connecting to server")
        async with websockets.connect(URI) as websocket:
            print("Connected to server")
            await asyncio.gather(
                self.response_handler(websocket),
                self.request_sender(websocket),
            )

    async def response_handler(self, websocket):
        async for message in websocket:
            self.handle_response(message)

    async def request_sender(self, websocket):
        while True:
            message = await self.requests.get()
            print(message)
            await websocket.send(message)
            self.requests.task_done()

    def handle_response(self, response):
        """{
            request:
            response:
        }"""
        print(response)
        msg = json.loads(response)
        match msg["request"]:
            case "newgame":
                self.game_id = str(msg["response"])
                # print("set game id to", self.game_id)
            case "getguess":
                self.opp_guess = msg["response"]
                # print("set opponents guess to", self.opp_guess)
            case "getresult":
                self.my_result = msg["response"]
                # print("set my result to", self.my_result)
            case "broadcast":
                print("broadcasting...")
            case "endgame":
                self.won = msg["response"]
                self.game_over = True
            case "ok":
                pass
                # print("ok")
            case other:
                print("invalid response")

    def create_game(self):
        message = self.create_message("newgame")
        self.requests.put_nowait(json.dumps(message))
        self.player_id = "0"
        print("creating game")

    def join_game(self):
        message = self.create_message("joingame")
        self.requests.put_nowait(json.dumps(message))
        self.player_id = "1"
        print("joining game")

    def get_guess(self):
        message = self.create_message("getguess")
        self.requests.put_nowait(json.dumps(message))

    def get_result(self):
        message = self.create_message("getresult")
        self.requests.put_nowait(json.dumps(message))

    def send_result(self, result):
        message = self.create_message("setresult", result)
        self.requests.put_nowait(json.dumps(message))

    def send_guess(self, x, y):
        message = self.create_message("setguess", f"{x},{y}")
        self.requests.put_nowait(json.dumps(message))

    def end_game(self, won):
        message = self.create_message("endgame", won)
        self.requests.put_nowait(json.dumps(message))
        print("ending game")

    def broadcast(self):
        message = self.create_message("broadcast")
        self.requests.put_nowait(json.dumps(message))
