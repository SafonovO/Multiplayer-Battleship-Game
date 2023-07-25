import socket
import sys
import threading
import time

SERVER = "127.0.0.1"
PORT = 1234
BUFFER_SIZE = 1024


class Server(threading.Thread):

    def run(self):
        threading.Thread.__init__(self)
        self.player_count = 0
        self.rx_threads = [None, None]
        # self.sockets = [None, None]
        # self.returned = []
        self.listen = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("starting server")
        try:
            self.sock.bind((SERVER, PORT))
        except socket.error as exc:
            print(exc)
        # listen on the socket
        self.sock.listen(2)

        while self.player_count < 2:
            conn, addr = self.sock.accept()
            print("Connected: ", addr)
            # self.sockets[self.player_count] = conn
            # 1 receiver per player to respond to that player's requests
            self.rx_threads[self.player_count] = threading.Thread(
                target=self.receiver, args=(conn, self.player_count))
            self.rx_threads[self.player_count].start()
            self.player_count += 1

        print("got all players!!")
        return None

    def shut_down(self):
        self.listen = False
        # self.sock.shutdown(socket.SHUT_RDWR)

        for thread in self.rx_threads:
            if thread:
                print("closing receiver")
                thread.join()
                print("closed receiver")
        self.sock.close()


    def receiver(self, conn, rx_id):
        conn.send(str.encode("Connection established"))

        while self.listen:
            data = conn.recv(BUFFER_SIZE)
            msg = data.decode()
            # recv returns empty string if connection was interrupted
            if not data:
                print("Disconnecting...")
                self.listen = False
            else:
                # protocols for client info
                if msg == "testing":
                    conn.send(str.encode(str("hello")))
                elif msg == "close":
                    self.listen = False

        print("Connection lost...")
        conn.close()
        # self.sockets.pop(rx_id)
        # self.returned.append(rx_id)
        print("closed connection")
