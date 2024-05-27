import socket
import threading

class SemaphoreServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.semaphores = {
            "semafor1": {"owner": None, "queue": []},
            "semafor2": {"owner": None, "queue": []},
            "semafor3": {"owner": None, "queue": []},
            "semafor4": {"owner": None, "queue": []},
            "semafor5": {"owner": None, "queue": []}
        }
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server-ul asculta pe {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        try:
            print(f"Client {address} conectat.")
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                command, sem_name = data.split()
                if command == "CERERE":
                    response = self.request_semaphore(sem_name, client_socket)
                    client_socket.send(response.encode())
                elif command == "ELIBERARE":
                    response = self.release_semaphore(sem_name, client_socket)
                    client_socket.send(response.encode())
        except ConnectionResetError:
            print(f"Conectarea cu {address} a fost pierduta.")
        except Exception as e:
            print(f"A avut loc o eroare cu {address}: {e}")
        finally:
            client_socket.close()
            print(f"Client {address} deconectat.")

    def request_semaphore(self, sem_name, client_socket):
        if sem_name in self.semaphores:
            sem = self.semaphores[sem_name]
            if sem["owner"] is None:
                sem["owner"] = client_socket
                return "APROBAT"
            else:
                sem["queue"].append(client_socket)
                return "IN ASTEPTARE"
        else:
            return "SEMAFORUL NU EXISTA"

    def release_semaphore(self, sem_name, client_socket):
        if sem_name in self.semaphores:
            sem = self.semaphores[sem_name]
            if sem["owner"] == client_socket:
                if sem["queue"]:
                    new_owner = sem["queue"].pop(0)
                    sem["owner"] = new_owner
                    new_owner.send("SEMAFOR ELIBERAT SI OCUPAT DE CLIENTUL IN ASTEPTARE".encode())
                else:
                    sem["owner"] = None
                return "SEMAFOR ELIBERAT"
            elif sem["owner"] is None:
                return "SEMAFORUL NU ESTE OCUPAT"
            else:
                return "CLIENTUL NU DETINE SEMAFORUL"
        else:
            return "SEMAFORUL NU EXISTA"

    def run(self):
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    server = SemaphoreServer('127.0.0.1', 5525)
    server.run()
