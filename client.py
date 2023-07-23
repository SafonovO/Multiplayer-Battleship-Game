
import socket
import threading
from server import BUFFER_SIZE, PORT, SERVER 


class Client(threading.Thread):
    # connect to server
    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((SERVER, PORT))
            self.id = self.client.recv(BUFFER_SIZE).decode()
        except socket.error as exc:
            print(exc)
        print(self.id)


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(BUFFER_SIZE).decode()
        except socket.error as exc:
            print(exc)