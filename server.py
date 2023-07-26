#!/usr/bin/env python

import asyncio
import websockets

ADDRESS = "127.0.0.1"
PORT = "8765"
URI = "ws://" + ADDRESS + ':' + PORT

class Server:
    async def handle_request(websocket):
        request = await websocket.recv()
        match request:
            case "hello":
                await websocket.send("hi")


async def main():
    async with websockets.serve(Server.handle_request, ADDRESS, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())