#!/usr/bin/env python

import asyncio
import websockets

URI = "ws://localhost:8765"

class Server:
    async def handle_request(websocket):
        request = await websocket.recv()
        match request:
            case "hello":
                await websocket.send("hi")


async def main():
    async with websockets.serve(Server.handle_request, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())