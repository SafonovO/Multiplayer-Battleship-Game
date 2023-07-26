import asyncio
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

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.password = Game.generate_pw()

    def generate_pw():
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for i in range(16))

class Server:
    def __init__(self) -> None:
        self.games = []

    def unpack(self, packet):
        '''
        [.|.|........|.... ...]
        first 1 chars: game id (up to 10 games)
        next 1 char: player number (0 or 1)
        next 8 chars: request
        rest: details
        '''
        game_id = packet[:1]
        player = packet[1]
        request = packet[2:10]
        details = packet[10:]
        return int(game_id), int(player), request, details

    async def handle_request(self, websocket):
        packet = await websocket.recv()
        game_id, player_id, request, details = self.unpack(packet)
        match request:
            case "testing-":
                await websocket.send(f'{game_id}, {player_id}, {request}, {details}')
            case "newgame-":
                new_game_id = self.new_game()
                await websocket.send(str(new_game_id))
            case "invite--":
                await websocket.send(str(self.get_password(game_id)))
            case "joingame":
                # temp hard coding: fix later
                await websocket.send("0")
            case "getguess":
                guess = await self.get_guess(game_id, player_id ^ 1)
                await websocket.send(str(guess))
            case "txresult":
                self.set_result(game_id, player_id ^ 1, details)
                await websocket.send("ok")
            case "txguess-":
                self.set_guess(game_id, player_id, details)
                await websocket.send("ok")
            case other:
                print("invalid request")

    def new_game(self):
        '''
        game id is the game's index in the games list
        '''
        self.games.append(Game())
        return len(self.games) - 1

    def get_password(self, game_id):
        return self.games[game_id].password
    
    async def get_guess(self, game_id, player_id):
        while not self.games[game_id].players[player_id].next_guess:
            # wait for the player to guess
            await asyncio.sleep(0.1)
        return self.games[game_id].players[player_id].next_guess
    
    def set_result(self, game_id, player_id, result):
        self.games[game_id].players[player_id].result = result

    def set_guess(self, game_id, player_id, guess):
        self.games[game_id].players[player_id].next_guess = guess


async def main():
    server = Server()
    async with websockets.serve(server.handle_request, ADDRESS, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())