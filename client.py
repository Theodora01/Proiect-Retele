import socket
import threading
import time

class SemaphoreClient:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def request_semaphore(self, sem_name):
        request_msg = f"CERERE {sem_name}"
        self.client_socket.send(request_msg.encode())
        response = self.client_socket.recv(1024).decode()
        return response

    def release_semaphore(self, sem_name):
        release_msg = f"ELIBERARE {sem_name}"
        self.client_socket.send(release_msg.encode())
        response = self.client_socket.recv(1024).decode()
        return response

    def close(self):
        self.client_socket.close()

def client_command_interface():
    client = SemaphoreClient('127.0.0.1', 5525)
    try:
        while True:
            command = input("Introdu comanda (cerere/eliberare/exit) si numele semaforului: ").strip().split()
            if len(command) < 2:
                print("Comanda invalida. Utilizeaza: <comanda> <nume_semafor>")
                continue

            action, sem_name = command[0], command[1]
            if action.lower() == 'cerere':
                response = client.request_semaphore(sem_name)
                print(f"Raspuns: {response}")
            elif action.lower() == 'eliberare':
                response = client.release_semaphore(sem_name)
                print(f"Raspuns: {response}")
            elif action.lower() == 'exit':
                print("Iesire.")
                break
            else:
                print("Comanda necunoscuta. Te rog utilizeaza 'cerere', 'eliberare', sau 'exit'.")
    finally:
        client.close()

if __name__ == "__main__":
    client_command_interface()