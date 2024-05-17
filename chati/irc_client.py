import socket
import threading

class IRCClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Conectado al servidor IRC.")
        
        self.socket.send(f"NICK {self.nickname}\n".encode())
        self.socket.send(f"USER {self.nickname} 0 * :{self.nickname}\n".encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self, message):
        self.socket.send(f"PRIVMSG #mi_canal :{message}\n".encode())

    def receive_messages(self):
        while True:
            message = self.socket.recv(1024).decode().strip()
            print(message)

if __name__ == "__main__":
    host = "127.0.0.1"  
    port = 8080
    nickname = "Culogordo"

    client = IRCClient(host, port, nickname)
    client.connect()

    while True:
        message = input()
        client.send_message(message)
