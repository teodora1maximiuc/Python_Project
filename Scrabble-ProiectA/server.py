import tkinter as tk
from tkinter import messagebox
import time
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

def is_word_in_dict(word):
    file_path = r"C:\\Users\\Raluci\\OneDrive\\Desktop\\python\\Maximiuc_Teodora_3B2\\Scrabble-ProiectA\\ro_RO.dic"
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == word:
                return True
    return False

def check_words_in_dict(words):
    for word in words:
        if word not in valid_2_letter_words and not is_word_in_dict(word):
            print(word)
            return False
    return True

def check_orizontal_extension(row, startCol, endCol):
    i = 0
    j = 0
    while special_tiles.get((row, startCol - i - 1), "").isupper():
        i += 1
    while special_tiles.get((row, endCol + j + 1), "").isupper():
        j += 1
    return i, j

def check_vertical_extension(startRow, endRow, col):
    i = 0
    j = 0
    while special_tiles.get((startRow - i - 1, col), "").isupper():
        i += 1
    while special_tiles.get((endRow + j + 1, col), "").isupper():
        j += 1
    return i, j

def apply_bonus(row, col, current_word):
    global special_tiles
    tile_type = special_tiles.get((row, col), "")
    word_points = 0
    to_multiply = 1
    if tile_type == "":
        word_points = letter_points[current_word[(row, col)]]
    elif tile_type == "x2_cuv":
        to_multiply = 2
    elif tile_type == "x3_litera":
        word_points = letter_points[current_word[(row, col)]] * 3
    elif tile_type == "x2_litera":
        word_points = letter_points[current_word[(row, col)]] * 2
    elif tile_type == "x3_cuv":
        to_multiply = 3
    return word_points, to_multiply

def get_orizontal_word(i, j, row, col, current_word):
    word_points = 0
    to_multiply = 1
    word = ""
    pos = col - i
    while pos != col + j + 1:
        if special_tiles.get((row, pos), "").isupper():
            word += special_tiles[(row, pos)]
            add = letter_points[special_tiles[((row, pos))]]
        elif (row, pos) in current_word: 
            word += current_word[(row, pos)]
            add, mul = apply_bonus(row, pos)
            word_points += add
            to_multiply *= mul
        pos += 1
    word_points *= to_multiply
    return word, word_points

def get_vertical_word(i, j, row, col, current_word):
    word_points = 0
    to_multiply = 1
    word = ""
    pos = row - i
    while pos != row + j + 1:
        if special_tiles.get((pos, col), "").isupper():
            word += special_tiles[((pos, col))]
            add = letter_points[special_tiles[((pos, col))]]
        elif (pos, col) in current_word:
            word += current_word[(pos, col)]
            add, mul = apply_bonus(pos, col)
            word_points += add
            to_multiply *= mul
        pos += 1
    word_points *= to_multiply
    return word, word_points

def validate_word(player_id, player_letters, current_word):
    global turn
    valid = 1
    rows = [key[0] for key in current_word.keys()]
    columns = [key[1] for key in current_word.keys()]
    words_to_check = []
    word = ""
    sorted_keys = sorted(current_word.keys(), key=lambda key: key[0])
    current_word = {key: current_word[key] for key in sorted_keys}
    if all(x == rows[0] for x in rows) or all(x == columns[0] for x in columns): 
        if all(x == rows[0] for x in rows): # orizontal            
            columns = [key[1] for key in current_word.keys()]
            i = 0
            j = 0
            i, j = check_orizontal_extension(rows[0], columns[0], columns[len(columns)-1])
            print(f"{i} {j}")
            pos = columns[0] - i
            word_points = 0
            to_multiply = 1
            while pos != columns[len(columns)-1] + j + 1:
                if special_tiles.get((rows[0], pos), "").isupper():
                    word += special_tiles[(rows[0], pos)]
                    word_points += letter_points[special_tiles[(rows[0], pos)]]
                elif (rows[0], pos) in current_word: 
                    word += current_word[(rows[0], pos)]
                    add, mul = apply_bonus(rows[0], pos, current_word)
                    word_points += add
                    to_multiply *= mul
                else: # nu sunt consecutive
                    valid = 0
                    break
                pos += 1
            if valid != 0:
                print(f"{word_points} x {to_multiply}")
                word_points *= to_multiply
                words_to_check.append(word)
                for column in columns:
                    i, j = check_vertical_extension(rows[0], rows[0], column)
                    if i!=0 or j!=0 :
                        word, add = get_vertical_word(i, j, rows[0], column, current_word)
                        print(f"add = {add}")
                        words_to_check.append(word)
                        word_points += add
                if len(current_word) == 1 and len(words_to_check) != 1:
                    words_to_check = words_to_check[1:]
                print(words_to_check)
                if not check_words_in_dict(words_to_check):
                    valid = 0
                print(f"Total points: {word_points}")
        elif all(x == columns[0] for x in columns): # vertical
            rows = [key[0] for key in current_word.keys()]
            i = 0
            j = 0
            i, j = check_vertical_extension(rows[0], rows[len(rows)-1], columns[0])
            print(f"{i} si {j}")
            pos = rows[0] - i
            word_points = 0
            to_multiply = 1
            while pos != rows[len(rows)-1] + j + 1:
                if special_tiles[(pos, columns[0])].isupper():
                    word += special_tiles[((pos, columns[0]))]
                    word_points += letter_points[special_tiles[((pos, columns[0]))]]
                elif (pos, columns[0]) in current_word:
                    word += current_word[(pos, columns[0])]
                    add, mul = apply_bonus(pos, columns[0], current_word)
                    print(f"add = {add}")
                    word_points += add
                    to_multiply *= mul
                else: # nu sunt consecutive
                    valid = 0
                    break
                pos += 1
            if valid != 0:
                word_points *= to_multiply
                words_to_check.append(word)
                for row in rows:
                    i, j = check_orizontal_extension(row, columns[0], columns[0])
                    if i!=0 or j!=0 :
                        word, add = get_orizontal_word(i, j, row, columns[0], current_word)
                        print(f"add = {add}")
                        words_to_check.append(word)
                        word_points += add
                if len(current_word) == 1 and len(words_to_check) != 1:
                    words_to_check = words_to_check[1:]
                print(words_to_check)
                if not check_words_in_dict(words_to_check):
                    valid = 0
                print(f"Total points: {word_points}")
        else: valid = 0
    else: valid = 0
    if valid == 1:
        print("Valid word!")
        print(player_letters)
        i = 0
        for letter in player_letters:
            if letter == '': 
                if all(letter_counted == 0 for letter_counted in letter_counts):
                    print("No more letters")
                else:
                    random_letter = random.choice(alphabet)
                    while letter_counts[random_letter] == 0:
                        random_letter = random.choice(alphabet)
                    player_letters[i] = random_letter
                    
                    letter_counts[random_letter] -= 1
            i += 1
        players_letters[player_id] = player_letters.copy()
        for key, item in current_word.items():
            special_tiles[key] = item
            print(f"key = {key}; item = {item}")
        current_word.clear()
        return 1
    elif valid == 0:
        print("Invalid word!")
        return 0

turn_lock = threading.Lock()

def handle_player_game(client_socket):
    global turn
    player_id_num = player_id[client_socket]

    while game_started:
        with turn_lock:
            if turn != player_id_num:
                data = {
                    'message': f"{turn + 1}'s turn",
                    'special_tiles': special_tiles_str_keys,
                    'letters': players_letters[player_id_num],
                }
                client_socket.sendall(json.dumps(data).encode('utf-8'))
                continue

            data = {
                'message': 'Your turn',
                'special_tiles': special_tiles_str_keys,
                'letters': players_letters[player_id_num],
            }
            client_socket.sendall(json.dumps(data).encode('utf-8'))

            try:
                answer = client_socket.recv(1600).decode('utf-8')
                current_word_str_key = json.loads(answer)
                current_word = {
                    tuple(map(int, key.split(','))): value
                    for key, value in current_word_str_key.items()
                }
                print(current_word)

                while validate_word(player_id_num, players_letters[player_id_num], current_word) == 0:
                    client_socket.sendall(json.dumps({'message': 'invalid'}).encode('utf-8'))
                    answer = client_socket.recv(1600).decode('utf-8')
                    current_word_str_key = json.loads(answer)
                    current_word = {
                        tuple(map(int, key.split(','))): value
                        for key, value in current_word_str_key.items()
                    }

                if validate_word(player_id_num, players_letters[player_id_num], current_word) == 1:
                    client_socket.sendall(json.dumps({'message': 'correct'}).encode('utf-8'))

                turn = (turn + 1) % len(clients)

            except Exception as e:
                print(f"Error processing player {player_id_num}'s move: {e}")


def accept_clients():
    global game_started, ready_count, player_id
    while len(clients) < 4:
        client_socket, client_address = server.accept()
        player_id[client_socket] = len(clients)
        clients.append(client_socket)
        print(f"New client connected. Total clients: {len(clients)}")

        threading.Thread(target=handle_client_ready, args=(client_socket,)).start()

def handle_client_ready(client_socket):
    print("hi")
    global game_started, ready_count, player_id
    while not game_started:
        try:
            data = client_socket.recv(1600).decode('utf-8')
            if data == "ready":
                ready_count += 1
                print(f"{ready_count} / {len(clients)} players ready.")
                if ready_count == len(clients):
                    game_started = True
                    print("All ready")
                    
                    for client in clients:
                        player_letters = []
                        while len(player_letters) < 7:
                            if all(letter_counts[x] == 0 for x in alphabet):
                                break
                            random_letter = random.choice(alphabet)
                            if letter_counts[random_letter] != 0:
                                player_letters.append(random_letter)
                                letter_counts[random_letter] -= 1
                        players_letters[player_id[client]] = player_letters

                    handle_player_game(client_socket)

        except (ConnectionResetError, BrokenPipeError):
            print("Player disconnected, readinees.")
            break

player_id = {}
players_letters = {}
accept_clients()