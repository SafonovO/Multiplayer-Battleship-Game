import asyncio
import json
from time import sleep
import websockets
import random
import string

ADDRESS = "127.0.0.1"
PORT = "8765"

class Player:
    def __init__(self):
        self.guessed = []
        self.ships = []
        self.next_guess = None
        self.result = None
        self.socket = None

class Game:
    def __init__(self):
        self.players = (Player(), Player())
        self.password = Game.generate_pw()

    def generate_pw():
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for i in range(16))

class Server:
    '''
    {
        "request": request,
        "game": game,
        "player": player,
        "details": details
    }
    '''
    def __init__(self) -> None:
        self.games = []

    def create_message(self, request="ok", response="ok"):
        return {
            "request": request,
            "response": response
        }

    async def handle_request(self, websocket):
        while True:
            packet = await websocket.recv()
            print(packet)
            msg = json.loads(packet)
            game_id = int(msg["game"]) if msg["game"] else None
            player_id = int(msg["player"]) if msg["player"] else None
            request = msg["request"]
            details = msg["details"]
            match request:
                # create a new game
                case "newgame":
                    self.games.append(Game())
                    new_game_id = len(self.games) - 1
                    self.games[new_game_id].players[0].socket = websocket
                    response = self.create_message("newgame", str(new_game_id))
                    print(response)
                    await websocket.send(json.dumps(response))

                # get a code to share so your friend can join your game
                case "invite":
                    response = self.create_message("invite", self.games[game_id].password)
                    await websocket.send(json.dumps(response))

                # join a game 
                # we're going to want to pass in a game password later
                case "joingame":
                    # BUG: temp hard coding: fix later
                    self.games[0].players[1].socket = websocket
                    response = self.create_message("newgame", "0")
                    await websocket.send(json.dumps(response))

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

                case other:
                    print("invalid request")


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
    async with websockets.serve(server.handle_request, ADDRESS, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())