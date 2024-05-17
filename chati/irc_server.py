import socket
import threading

class IRCServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"Servidor IRC escuchando en {self.host}:{self.port}...")

            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Nueva conexión de {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")

    def handle_client(self, client_socket):
        self.clients.append(client_socket)
        client_socket.send("Bienvenido al servidor IRC!\n".encode())

        while True:
            try:
                message = client_socket.recv(1024).decode().strip()
                if message:
                    print(f"Mensaje recibido: {message}")
                    self.broadcast(message, client_socket)
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, sender_socket):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(f"{message}\n".encode())
                except Exception as e:
                    print(f"Error al enviar mensaje: {e}")
                    self.clients.remove(client_socket)
                    client_socket.close()

if __name__ == "__main__":
    server = IRCServer("0.0.0.0", 8080)  
    server.start()

