import asyncio
from server import URI
import websockets

class Client:
    async def send(request):
        async with websockets.connect(URI) as websocket:
            await websocket.send(request)
            greeting = await websocket.recv()
            print(greeting)

