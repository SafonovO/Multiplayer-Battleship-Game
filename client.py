import asyncio
from time import sleep
import websockets

URI = "ws://24.199.115.192:8765"
URI = "ws://127.0.0.1:8765"


class Client:

    async def send(self, request):
        async with websockets.connect(URI) as websocket:
            await websocket.send(request)
            response = await websocket.recv()
            print(response)
            return response

    async def create_game(self):
        self.game_id = await self.send("00newgame-")
        self.player_id = '0'
        print("successfully created game")

    async def join_game(self):
        self.game_id = await self.send("00joingame")
        self.player_id = '1'
        print("successfully joined game")

    async def get_guess(self):
        return await self.send(f'{self.game_id}{self.player_id}getguess')
    
    async def send_result(self, result):
        await self.send(f'{self.game_id}{self.player_id}txresult{result}')

    async def send_guess(self, x, y):
        await self.send(f'{self.game_id}{self.player_id}txguess-{x},{y}')






