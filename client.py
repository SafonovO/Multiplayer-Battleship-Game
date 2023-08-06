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
        self.requests = []
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
                self.consumer_handler(websocket),
                self.producer_handler(websocket),
            )

    async def consumer_handler(self, websocket):
        async for message in websocket:
            self.handle_response(message)

    async def producer_handler(self, websocket):
        while True:
            message = await self.producer()
            print(message)
            await websocket.send(message)

    async def producer(self):
        while not self.requests:
            await asyncio.sleep(0.5)
        request = self.requests[0]
        self.requests.pop(0)
        return request

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
        self.requests.append(json.dumps(message))
        self.player_id = "0"
        print("creating game")

    def join_game(self):
        message = self.create_message("joingame")
        self.requests.append(json.dumps(message))
        self.player_id = "1"
        print("joining game")

    def get_guess(self):
        message = self.create_message("getguess")
        self.requests.append(json.dumps(message))

    def get_result(self):
        message = self.create_message("getresult")
        self.requests.append(json.dumps(message))

    def send_result(self, result):
        message = self.create_message("setresult", result)
        self.requests.append(json.dumps(message))

    def send_guess(self, x, y):
        message = self.create_message("setguess", f"{x},{y}")
        self.requests.append(json.dumps(message))

    def end_game(self, won):
        message = self.create_message("endgame", won)
        self.requests.append(json.dumps(message))
        print("ending game")
        print(* self.requests)

    def broadcast(self):
        message = self.create_message("broadcast")
        self.requests.append(json.dumps(message))
