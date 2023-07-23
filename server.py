import socket
import threading
import time

SERVER = "127.0.0.1"
PORT = 1234
BUFFER_SIZE = 1024



class Server(threading.Thread):

    def run(self):
        threading.Thread.__init__(self)
        self.player_count = 0

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("starting server")
        try:
            sock.bind((SERVER, PORT))
        except socket.error as exc:
            str(exc)

        # listen on the socket
        sock.listen(2)

        while self.player_count < 2:
            print("Waiting...")
            conn, addr = sock.accept()
            print("Connected: ", addr)
            self.player_count += 1

        print("got all players!!")
        return None

