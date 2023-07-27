import asyncio
import json
from time import sleep
import websockets

URI = "ws://24.199.115.192:8765"
URI = "ws://127.0.0.1:8765"


class Client:
    def create_message(self, request, game="", player="", details=""):
        return {
            "request": request,
            "game": game,
            "player": player,
            "details": details
        }

    async def send(self, request):
        async with websockets.connect(URI) as websocket:
            await websocket.send(request)
            response = await websocket.recv()
            print(response)
            return response

    async def create_game(self):
        message = self.create_message("newgame")
        self.game_id = await self.send(json.dumps(message))
        self.player_id = '0'
        print("successfully created game")

    async def join_game(self):
        message = self.create_message("joingame")
        self.game_id = await self.send(json.dumps(message))
        self.player_id = '1'
        print("successfully joined game")

    async def get_guess(self):
        message = self.create_message("getguess", self.game_id, self.player_id)
        return await self.send(json.dumps(message))
    
    async def get_result(self):
        message = self.create_message("getresult", self.game_id, self.player_id)
        return await self.send(json.dumps(message))
    
    async def send_result(self, result):
        message = self.create_message("setresult", self.game_id, self.player_id, result)
        await self.send(json.dumps(message))

    async def send_guess(self, x, y):
        message = self.create_message("setguess", self.game_id, self.player_id, f'{x},{y}')
        await self.send(json.dumps(message))






