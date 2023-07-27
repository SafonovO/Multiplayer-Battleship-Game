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
        self.players = [Player(), Player()]
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

    async def handle_request(self, websocket):
        packet = await websocket.recv()
        msg = json.loads(packet)
        game_id = int(msg["game"]) if msg["game"] else None
        player_id = int(msg["player"]) if msg["player"] else None
        request = msg["request"]
        details = msg["details"]
        
        match request:
            # for testing purposes
            case "testing":
                await websocket.send(f'{game_id}, {player_id}, {request}, {details}')
            # create a new game
            case "newgame":
                new_game_id = self.new_game()
                self.games[new_game_id].players[0].socket = websocket
                await websocket.send(str(new_game_id))
            # get a code to share so your friend can join your game
            case "invite":
                await websocket.send(str(self.get_password(game_id)))
            # join a game 
            # we're going to want to pass in a game password later
            case "joingame":
                # temp hard coding: fix later
                self.games[0].players[1].socket = websocket
                await websocket.send("0")
            # join first empty game
            # might need to return error if no empty games, then create game instead
            case "joinrandom":
                pass
            case "getguess":
                guess = await self.get_guess(game_id, player_id ^ 1)
                await websocket.send(str(guess))
            case "getresult":
                result = await self.get_result(game_id, player_id)
                await websocket.send(str(result))
                self.games[game_id].players[player_id].result = None
            case "setresult":
                self.set_result(game_id, player_id ^ 1, details)
                await websocket.send("ok")
            case "setguess":
                self.set_guess(game_id, player_id, details)
                await websocket.send("ok")
            case "gameover":
                self.end_game(game_id, player_id, details)
                await websocket.send("ok")
            case other:
                print("invalid request")

    def new_game(self):
        self.games.append(Game())
        return len(self.games) - 1

    def get_password(self, game_id):
        return self.games[game_id].password
    
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


    def set_result(self, game_id, player_id, result):
        self.games[game_id].players[player_id].result = result

    def set_guess(self, game_id, player_id, guess):
        self.games[game_id].players[player_id].next_guess = guess

    def end_game(self, game_id, player_id, details):
        # tell player_id ^ 1 that they lost
        # games[game_id] = None
        pass


async def main():
    server = Server()
    async with websockets.serve(server.handle_request, ADDRESS, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())