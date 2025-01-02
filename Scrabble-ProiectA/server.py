import socket
import threading

game_started = False
ready_count = 0
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(4)

def handle_client(client_socket): 
    global ready_count, game_started, clients
    try:
        if game_started:
            client_socket.sendall(b"Game already in progress!")
            client_socket.close()
            return
        while not game_started:
            data = client_socket.recv(1024).decode('utf-8')
            if data == "ready":
                ready_count += 1
                if ready_count == len(clients):
                    game_started = True
                    for client in clients:
                        client.sendall(b"Game has started!")
        while game_started:
            i = 1
    except (ConnectionResetError, BrokenPipeError):
        print("Client disconnected unexpectedly.")

while len(clients) < 4:
    if not game_started:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"New client connected. Total clients: {len(clients)}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()
