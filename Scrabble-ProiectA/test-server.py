import tkinter as tk
from tkinter import messagebox
import time
import socket
import threading
import json
import random
import sys

if len(sys.argv) < 2:
    print("Trebuie file path dictionar..")
    sys.exit(1)

file_path = sys.argv[1]

alphabet = ['A', 'B', 'C', 'D','E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Z']
letter_points = {
    'A': 1, 'B': 5, 'C': 3, 'D': 3, 'E': 1, 'F': 4, 'G': 6, 'H': 8, 
    'I': 1, 'J': 8, 'L': 2, 'M': 4, 'N': 2, 'O': 2, 'P': 2, 'R': 1, 
    'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 10, 'Z': 8
}
letter_counts = {
    'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 0, 'F': 1, 'G': 1, 'H': 0, 
    'I': 0, 'J': 0, 'L': 1, 'M': 1, 'N': 1, 'O': 2, 'P': 1, 'R': 1, 
    'S': 0, 'T': 1, 'U': 1, 'V': 1, 'X': 0, 'Z': 0
}
valid_2_letter_words = [
    "AA", "AB", "AC", "AD", "AH", "AI", "AL", "AM", "AN", "AR", "AS", "AT", "AU", "AX", "AZ",
    "BA", "BI", "BU", "CA", "CE", "CI", "CO", "CU", "DA", "DE", "DI", "DO", "DU",
    "EA", "EC", "EE", "EH", "EI", "EL", "EN", "ET", "EU", "EV", "EX",
    "FA", "FI", "FU", "GA", "GO", "HA", "HE", "HI", "HM", "HO", "HU",
    "IA", "IC", "IE", "II", "IL", "IM", "IN", "IO", "IR", "IS", "IT", "IU", "IZ",
    "LA", "LE", "LI", "MA", "MI", "MU", "NA", "NE", "NI", "NO", "NU",
    "OA", "OF", "OH", "OI", "OL", "OM", "ON", "OP", "OR", "OS", "OT", "OU",
    "PA", "PE", "PI", "PU", "RA", "RE", "RO", "SA", "SE", "SI", "SO", "SS", "ST", "SU",
    "TA", "TE", "TI", "TT", "TU", "UD", "UF", "UI", "UN", "US", "UT", "UU", "UZ",
    "VA", "VI", "VU", "XU", "ZA", "ZI"
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


clients = []
players_letters = []
turns = []
scores = []
turn = 0
ready_count = 0
total_clients = 0
lock = threading.Lock()
"""
Variabile globale:
    - special_tiles: un dictionar unde este memorata board-ul curent al jocului, la inceput fiind initializat cu pozitiile prestabilite ale bonusurilor
    , iar mai apoi cu eventuale litere puse de clienti pe tabla. Bonusurile sunt aplicate doar odata, atunci cand un client pune o litera pe acel tile.
    - clients: tine intr-un vector toti clientii conectati
    - players_letters: memoreaza literele curente ale tuturor jucatorilor
    - turns: memoreaza pozitia tuturor jucatorilor pentru a determina randul sau
    - scores: memoreaza scorul jucatorilor
"""

def is_word_in_dict(word):
    """
    Functie care verifica daca un cuvant este in dictionar
    """
    global file_path
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == word:
                return True
    return False

def check_words_in_dict(words):
    # for word in words:
    #     if word not in valid_2_letter_words and not is_word_in_dict(word):
    #         print(word)
    #         return False
    return True

def check_orizontal_extension(row, startCol, endCol):
    """
    Functie care verifica daca in dreapta sau stanga cuvantului se afla alte litere adiacente
    Returneaza: 
        - coloana de unde incepe (i - int)
        - coloana unde se termina (j - int)
    """
    i = 0
    j = 0
    while special_tiles.get((row, startCol - i - 1), "").isupper():
        i += 1
    while special_tiles.get((row, endCol + j + 1), "").isupper():
        j += 1
    return i, j

def check_vertical_extension(startRow, endRow, col):
    """
    Functie care verifica daca deasupra sau dedesuptul cuvantului se afla alte litere adiacente
    Returneaza: 
        - randul de unde incepe (i - int)
        - randul unde se termina (j - int)
    """
    i = 0
    j = 0
    while special_tiles.get((startRow - i - 1, col), "").isupper():
        i += 1
    while special_tiles.get((endRow + j + 1, col), "").isupper():
        j += 1
    return i, j

def apply_bonus(row, col, current_word):
    """
    Functie care verifica daca litera a fost plasata pe un tile cu bonus. Daca da, aplicam acel bonus
    Parametrii:
        - row (int): linia unde se afla litera
        - col (int): coloana ...
        - current_word (dict): un dictionar format din chei tuplu ce reprezinta pozitia unei litere si item cu valoarea literei
    Returneaza:
        - cate puncte trebuie adaugate (word_points - int)
        - cate puncte trebuie sa inmulteasca tot cuvantul (to_multiply - int)
    """
    global special_tiles
    tile_type = special_tiles.get((row, col), "")
    word_points = letter_points[current_word[(row, col)]]
    to_multiply = 1
    if tile_type == "" or tile_type == "stea":
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
    """
    Functie care formeaza un cuvant pus orizontal dintr-un interval de coloane pus pe tabla, impreuna cu eventuale extensii
    Parametrii:
        - i (int): cate coloane in dreapta fata de literele puse pe tabla de client
        - j (int): cate coloane in stanga ...
        - row (int): linia unde se afla cuvantul
        - col (int): prima coloane unde se afla litera pusa de client
        - current_word (dict): un dictionar format din chei tuplu ce reprezinta pozitia unei litere si item cu valoarea literei
    Returneaza: 
        - cuvantul gasit in interval (word - string)
        - cate puncte valoreaza (word_points - int)
    """
    word_points = 0
    word = ""
    pos = col - i
    while pos != col + j + 1:
        if special_tiles.get((row, pos), "").isupper():
            word += special_tiles[(row, pos)]
            add = letter_points[special_tiles[((row, pos))]]
        elif (row, pos) in current_word: 
            word += current_word[(row, pos)]
            add, mul = apply_bonus(row, pos, current_word)
            word_points += add
        pos += 1
    return word, word_points

def get_vertical_word(i, j, row, col, current_word):
    """
    Functie care formeaza un cuvant pus vertical dintr-un interval de linii pus pe tabla, impreuna cu eventuale extensii
    Parametrii:
        - i (int): cate linii deasupra fata de literele puse pe tabla de client
        - j (int): cate linii dedesupt ...
        - row (int): prima linie unde se afla litera pusa de client
        - col (int): coloana pe care e cuvantul
        - current_word (dict): un dictionar format din chei tuplu ce reprezinta pozitia unei litere si item cu valoarea literei
    Returneaza: 
        - cuvantul gasit in interval (word - string)
        - cate puncte valoreaza (word_points - int)
    """
    word_points = 0
    word = ""
    pos = row - i
    while pos != row + j + 1:
        if special_tiles.get((pos, col), "").isupper():
            word += special_tiles[((pos, col))]
            add = letter_points[special_tiles[((pos, col))]]
            word_points += add
        elif (pos, col) in current_word:
            word += current_word[(pos, col)]
            add, mul = apply_bonus(pos, col, current_word)
            word_points += add
        pos += 1
    return word, word_points

def validate_word(current_word, player_letters):
    """
    Functie care primeste un cuvant de la client si verifica daca este corect
    Parametrii:
        - current_word (dictionar): un dictionar format din chei tuplu ce reprezinta pozitia unei litere si item cu valoarea literei
        - player_letters (vector cu string): literele curente ale unui client
    Functionalitati:
        - Verifica daca pozitia cuvantului este buna:
        1. La primul tur, o litera trebuie pusa pe tile-ul din mijloc
        2. Cuvantul trebuie sa aiba litere puse pe aceeasi coloana sau aceeasi linie (vertical sau orizontal)
        3. Verifica daca se conecteaza cu literele deja existente pe tabla (check_vertical_extension sau check_orizontal_extension)
        4. Verifica daca toate cuvintele care sunt formate sunt valide (get_vertical_word sau get_orizontal_word + check_words_in_dict)
        - In timpul verificarii cuvintelor este calculat si scorul dat de valoarea cuvintelor formate, impreuna cu bonusurile de pe tabla (apply_bonus)
        - Daca cuvantul este valid, se reatribuie literele lipsa
    Returneaza:
        - noile litere ale playerului (player_letters - vector string)
        - punctajul obtinut al cuvantului (score - int )
    """
    global turn, special_tiles
    valid = 1
    rows = [key[0] for key in current_word.keys()]
    columns = [key[1] for key in current_word.keys()]
    words_to_check = []
    word = ""
    word_points = 0
    if turn == 1:
        valid = 0
        for key in current_word.keys():
            if key[0] == 7 and key[1] == 7:
                valid = 1
                break
    if valid == 0:
        return [], 0
    # Verifica daca toate literele sunt ori pe acelasi rand, ori pe aceeasi coloana
    if all(x == rows[0] for x in rows) or all(x == columns[0] for x in columns): 
        if all(x == rows[0] for x in rows) and valid == 1: # cuvant orizontal  
            # Sortam literele sa fie in ordinea lor pe tabla (sunt cazuri cand clientul nu pune literele in ordinea lor de pe tabla)
            sorted_keys = sorted(current_word.keys(), key=lambda key: key[1])
            current_word = {key: current_word[key] for key in sorted_keys}
            columns = [key[1] for key in current_word.keys()]
            i = 0
            j = 0
            i, j = check_orizontal_extension(rows[0], columns[0], columns[len(columns)-1])
            print(f"{i} {j}")
            pos = columns[0] - i
            word_points = 0
            to_multiply = 1
            while pos != columns[len(columns)-1] + j + 1:
                if special_tiles.get((rows[0],pos), "").isupper():
                    word += special_tiles[(rows[0], pos)]
                    word_points += letter_points[special_tiles[(rows[0], pos)]]
                elif (rows[0], pos) in current_word: 
                    word += current_word[(rows[0], pos)]
                    add, mul = apply_bonus(rows[0], pos, current_word)
                    word_points += add
                    print(f"add = {add} & mul = {mul}")
                    to_multiply *= mul
                else: # nu sunt consecutive
                    valid = 0
                    return [], 0
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
                    return [], 0
                print(f"Total points: {word_points}")
        elif all(x == columns[0] for x in columns) and valid == 1: # cuvant vertical
            sorted_keys = sorted(current_word.keys(), key=lambda key: key[0])
            current_word = {key: current_word[key] for key in sorted_keys}
            rows = [key[0] for key in current_word.keys()]
            i = 0
            j = 0
            i, j = check_vertical_extension(rows[0], rows[len(rows)-1], columns[0])
            print(f"{i} si {j}")
            pos = rows[0] - i
            word_points = 0
            to_multiply = 1
            while pos != rows[len(rows)-1] + j + 1:
                if special_tiles.get((pos, columns[0]), "").isupper():
                    word += special_tiles[((pos, columns[0]))]
                    word_points += letter_points[special_tiles[((pos, columns[0]))]]
                elif (pos, columns[0]) in current_word:
                    word += current_word[(pos, columns[0])]
                    add, mul = apply_bonus(pos, columns[0], current_word)
                    print(f"add = {add} & mul = {mul}")
                    word_points += add
                    to_multiply *= mul
                else: # nu sunt consecutive
                    valid = 0
                    return [], 0
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
                    return [], 0
                print(f"Total points: {word_points}")
        else: 
            valid = 0
            return [], 0
    else: 
        valid = 0
        return [], 0
    if valid == 1:
        print("Valid word!")
        print(player_letters)
        i = 0
        for letter in player_letters:
            if letter == '': 
                available_letters = [letter for letter, count in letter_counts.items() if count > 0]
                if not available_letters:
                    print("No more letters")
                else:
                    random_letter = random.choice(available_letters)
                    player_letters[i] = random_letter
                    print(player_letters[i])
                    
                    letter_counts[random_letter] -= 1
            i += 1
        for key, item in current_word.items():
            special_tiles[key] = item
        print (player_letters)
        print(f"score: {word_points}")
        return player_letters, word_points
    elif valid == 0:
        print("Invalid word!")
        return [], 0

def bag_count():
    count = 0
    for x in letter_counts.keys:
        count += letter_counts[x]
    return count

def handle_client(client_socket, addr):
    """
    Functie pentru gestionarea fiecarui client. 
    Parametrii:
        - client_socket: Obiectul socket al clientului.
        - addr: Adresa clientului.
    Functionalitati:
        - Asteapta sa primeasca de la client mesajul "ready";
        - Daca un client este ready, acestuia i se vor genera 7 litere pentru joc, si se vor initializa variabile precum scorul si randul sau;
        - Daca toti clientii sunt ready, se trimite la fiecare client board-ul curent si literele sale, apoi incepe jocul (start_game).
    """
    global ready_count, total_clients, special_tiles
    print(f"New player: {addr}")
    client_socket.send("Wait for ready..".encode())
    
    ready = client_socket.recv(1800).decode().strip().lower()
    if ready == "ready":
        with lock:
            ready_count += 1
            clients.append(client_socket)
            turns.append(addr)
            scores.append(0)
            player_letters = []
            while len(player_letters) < 7:
                if all(letter_counts[x] == 0 for x in alphabet):
                    break
                random_letter = random.choice(alphabet)
                if letter_counts[random_letter] != 0:
                    player_letters.append(random_letter)
                    letter_counts[random_letter] -= 1
            players_letters.append(player_letters)
        print(f"Client {addr} ready. Total: {ready_count}/{total_clients}")

        if ready_count == total_clients:
            print(f"All ready! Starting the game...")
            special_tiles_str_keys = {f"{key[0]},{key[1]}": value for key, value in special_tiles.items()}
            for c in range(0, ready_count):
                data = {
                    'special_tiles': special_tiles_str_keys,
                    'letters': players_letters[c],
                }
                clients[c].sendall(json.dumps(data).encode('utf-8'))
            start_game()

def start_game():
    """
    Functie pentru gestionarea jocului si a turelor. 
    Functionalitati:
        - Se trimite catre clienti al cui rand este, si asteapta sa primeasca raspuns de la clientul curent pentru gestionarea miscarii sale.
        - Un client are doua comenzi care semnaleaza finalizarea unei ture, switch si done
        - Switch: atunci cand clientul vrea sa schimbe o litera, fara a pune un cuvant pe tabla
        - Done: punerea unui cuvant pe tabla ca mai apoi serverul sa verifice daca este valid (Daca nu este valid, turn-ul nu isi schimba valoarea pentru a ramane randul sau)
        - Randul unui client se schimba dupa ce a schimbat o litera sau a validat un cuvant cu succes
    """
    global turn, special_tiles
    current_turn = 0
    while True:
        with game_lock:
            turn += 1
            current_client = clients[current_turn]
            current_addr = turns[current_turn]
            print(current_turn)
        time.sleep(0.1)
        for c in clients:
            with game_lock:
                if c != current_client:
                    data_to_send = {
                        "reason": f"Player {current_turn + 1}'s turn!"
                    }
                    c.send(json.dumps(data_to_send).encode('utf-8'))
                else:
                    data_to_send = {
                        "reason": "It's your turn!"
                    }
                    c.send(json.dumps(data_to_send).encode('utf-8'))
        message = current_client.recv(1800).decode()
        print(f"am primit :{message}")
        parsed_message = json.loads(message)
        if "switch" in parsed_message['reason']:
            _, data = parsed_message['reason'].split(" ", 1)
            current_letter, current_letter_col = data.split(",")
            current_letter = current_letter.strip()
            current_letter_col = int(current_letter_col.strip())
            print(f"Current Letter: {current_letter}, Column: {current_letter_col}")
            if not all(letter_counts[x] == 0 for x in alphabet):
                random_letter = random.choice(alphabet)
                while letter_counts[random_letter] == 0:
                    random_letter = random.choice(alphabet)
                letter_counts[current_letter] +=1
                letter_counts[random_letter] -=1
                players_letters[current_turn][current_letter_col] = random_letter
                print(random_letter)
                data_to_send = {
                    "reason": random_letter
                }
                current_client.send(json.dumps(data_to_send).encode('utf-8'))
            else:
                data_to_send = {
                    "reason": "empty bag",
                }
                current_client.send(json.dumps(data_to_send).encode('utf-8'))
        elif "done" in parsed_message['reason']:
            current_word = {
                tuple(map(int, key.split(','))): value
                for key, value in parsed_message['current_word'].items()
            }
            score = 0
            letters, score = validate_word(current_word, parsed_message['letters'])
            if score == 0:
                data_to_send = {
                    "reason": "check",
                    "status": "invalid"
                }
                current_client.send(json.dumps(data_to_send).encode('utf-8'))
                current_turn -= 1
            else:
                players_letters[current_turn] = letters.copy()
                scores[current_turn] += score
                special_tiles_str_keys = {f"{key[0]},{key[1]}": value for key, value in special_tiles.items()}
                data_to_send = {
                    "reason": "check",
                    "status": "valid",
                    "letters": letters,
                    "score": score,
                    "special_tiles": special_tiles_str_keys
                }
                current_client.send(json.dumps(data_to_send).encode('utf-8'))
            for c in clients:
                if c != current_client:
                    special_tiles_str_keys = {f"{key[0]},{key[1]}": value for key, value in special_tiles.items()}
                    data_to_send = {
                        "reason": "update",
                        "special_tiles": special_tiles_str_keys
                    }
                    print (c)
                    c.send(json.dumps(data_to_send).encode('utf-8'))
        else:
            print(f"Message from {current_addr}: {parsed_message}")
        if not all(any(l != '' for l in player_letters) for player_letters in players_letters):
            max_score = max(scores)
            max_index = scores.index(max_score)
            for c in clients:
                with game_lock:
                    data_to_send = {
                        "reason": f"Player {max_index} won with {scores[max_index]} points!"
                    }
                    c.send(json.dumps(data_to_send).encode('utf-8'))
            return
        current_turn = (current_turn + 1) % total_clients

def server():
    """
    Porneste serverul si gestioneaza conexiunile clientilor, creand un thread pentru fiecare client.
    """
    global total_clients
    host = "127.0.0.1"
    port = 5555
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Host & port {host}:{port}...")
    
    while True:
        client_socket, addr = server_socket.accept()
        total_clients += 1
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()
game_lock = threading.Lock()
server()
