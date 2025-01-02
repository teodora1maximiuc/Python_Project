import socket
import threading
import json
import random

alphabet = ['A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 
    'I', 'J', 'L', 'M', 
    'N', 'O', 'P', 'R',
    'S', 'T', 'U', 'V', 'X', 'Z']
letter_points = {
    'A': 1, 'B': 5, 'C': 3, 'D': 3,
    'E': 1, 'F': 4, 'G': 6, 'H': 8, 
    'I': 1, 'J': 8, 'L': 2, 'M': 4, 
    'N': 2, 'O': 2, 'P': 2, 'R': 1, 
    'S': 1, 'T': 1, 'U': 1, 'V': 4,
    'X': 10, 'Z': 8
}
letter_counts = {
    'A': 10, 'B': 2, 'C': 5, 'D': 4,
    'E': 9, 'F': 2, 'G': 2, 'H': 2, 
    'I': 11, 'J': 1, 'L': 5, 'M': 3, 
    'N': 6, 'O': 6, 'P': 4, 'R': 6, 
    'S': 6, 'T': 7, 'U': 5, 'V': 2,
    'X': 1, 'Z': 1
}
valid_2_letter_words = [
    "AA", "AB", "AC", "AD", "AH", "AI", "AL", "AM", "AN", "AR", "AS", "AT", "AU", "AX", "AZ",
    "BA", "BI", "BU",
    "CA", "CE", "CI", "CO", "CU",
    "DA", "DE", "DI", "DO", "DU",
    "EA", "EC", "EE", "EH", "EI", "EL", "EN", "ET", "EU", "EV", "EX",
    "FA", "FI", "FU",
    "GA", "GO",
    "HA", "HE", "HI", "HM", "HO", "HU",
    "IA", "IC", "IE", "II", "IL", "IM", "IN", "IO", "IR", "IS", "IT", "IU", "IZ",
    "LA", "LE", "LI",
    "MA", "MI", "MU",
    "NA", "NE", "NI", "NO", "NU",
    "OA", "OF", "OH", "OI", "OL", "OM", "ON", "OP", "OR", "OS", "OT", "OU",
    "PA", "PE", "PI", "PU",
    "RA", "RE", "RO",
    "SA", "SE", "SI", "SO", "SS", "ST", "SU",
    "TA", "TE", "TI", "TT", "TU",
    "UD", "UF", "UI", "UN", "US", "UT", "UU", "UZ",
    "VA", "VI", "VU",
    "XU",
    "ZA", "ZI"
]
special_tiles = {
    # x2 CUV
    (1, 1): "x2_cuv",
    (2, 2): "x2_cuv",
    (3, 3): "x2_cuv",
    (4, 4): "x2_cuv",
    (10, 10): "x2_cuv",
    (11, 11): "x2_cuv",
    (12, 12): "x2_cuv",
    (13, 13): "x2_cuv",
    (1, 13): "x2_cuv",
    (2, 12): "x2_cuv",
    (3, 11): "x2_cuv",
    (4, 10): "x2_cuv",
    (13, 1): "x2_cuv",
    (12, 2): "x2_cuv",
    (11, 3): "x2_cuv",
    (10, 4): "x2_cuv",
    # x3 LITERA
    (5, 1): "x3_litera",
    (9, 1): "x3_litera",
    (9, 5): "x3_litera",
    (5, 5): "x3_litera",
    (5, 9): "x3_litera",
    (5, 13): "x3_litera",
    (9, 13): "x3_litera",
    (9, 9): "x3_litera",
    (1, 5): "x3_litera",
    (1, 9): "x3_litera",
    (13, 5): "x3_litera",
    (13, 9): "x3_litera",
    # x2 LITERA
    (2, 6): "x2_litera",
    (3, 7): "x2_litera",
    (2, 8): "x2_litera",
    (0, 3): "x2_litera",
    (0, 11): "x2_litera",
    (6, 6): "x2_litera",
    (6, 8): "x2_litera",
    (8, 6): "x2_litera",
    (8, 8): "x2_litera",
    (14, 3): "x2_litera",
    (14, 11): "x2_litera",
    (11, 14): "x2_litera",
    (11, 0): "x2_litera",
    (3, 0): "x2_litera",
    (3, 14): "x2_litera",
    (12, 6): "x2_litera",
    (11, 7): "x2_litera",
    (12, 8): "x2_litera",
    (6, 2): "x2_litera",
    (7, 3): "x2_litera",
    (8, 2): "x2_litera",
    (6, 12): "x2_litera",
    (7, 11): 'x2_litera',
    (8, 12): "x2_litera",
    # x3 CUV
    (0, 0): "x3_cuv",
    (7, 0): "x3_cuv",
    (7, 14): "x3_cuv",
    (0, 7): "x3_cuv",
    (14, 7): "x3_cuv",
    (14, 0): "x3_cuv",
    (0, 14): "x3_cuv",
    (14, 14): "x3_cuv",
    # STEA
    (7, 7): "stea",
    # (6, 7): "M",
    # (7, 7): "A",
    # (8, 7): "S",
    # (9, 7): "A",
}
special_tiles_str_keys = {f"{key[0]},{key[1]}": value for key, value in special_tiles.items()}
turn = 0
game_started = False
ready_count = 0
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(4)

def handle_client(client_socket, player_id): 
    global ready_count, game_started, clients
    print(clients)
    try:
        if game_started:
            client_socket.sendall(b"Game already in progress!")
            client_socket.close()
            return
        while not game_started:
            data = client_socket.recv(1600).decode('utf-8')
            if data == "ready":
                ready_count += 1
                print(f"{ready_count} = {len(clients)}?")
                if ready_count == len(clients):
                    game_started = True
                    player_letters = []
                    while len(player_letters) < 7:
                        random_letter = random.choice(alphabet)
                        if letter_counts[random_letter] != 0:
                            player_letters.append(random_letter)
                            letter_counts[random_letter] -= 1
                    data = {
                        'message': "Game has started!",
                        'special_tiles': special_tiles_str_keys,
                        'letters': player_letters
                    }
                    print("sending...")
                    for client in clients:
                        client.sendall(json.dumps(data).encode('utf-8'))
        handle_player_game(client_socket, player_id)
    except (ConnectionResetError, BrokenPipeError):
        print("Client disconnected unexpectedly.")

def handle_player_game(client_socket, player_id):
    global turn
    while True:
        try: 
            i = 1
        except (ConnectionResetError, BrokenPipeError):
            print(f"Player {player_id} disconnected.")
            break

while len(clients) < 4:
    if not game_started:
        client_socket, client_address = server.accept()
        player_id = len(clients)
        clients.append(client_socket)
        print(f"New client connected. Total clients: {len(clients)}")
        threading.Thread(target=handle_client, args=(client_socket, player_id)).start()
