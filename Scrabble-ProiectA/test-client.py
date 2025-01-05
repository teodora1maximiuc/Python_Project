import socket
import tkinter as tk
import threading
import json

alphabet = ['A', 'B', 'C', 'D','E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Z']
letter_points = {
    'A': 1, 'B': 5, 'C': 3, 'D': 3, 'E': 1, 'F': 4, 'G': 6, 'H': 8, 
    'I': 1, 'J': 8, 'L': 2, 'M': 4, 'N': 2, 'O': 2, 'P': 2, 'R': 1, 
    'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 10, 'Z': 8
}
letter_counts = {
    'A': 10, 'B': 2, 'C': 5, 'D': 4, 'E': 9, 'F': 2, 'G': 2, 'H': 2, 
    'I': 11, 'J': 1, 'L': 5, 'M': 3, 'N': 6, 'O': 6, 'P': 4, 'R': 6, 
    'S': 6, 'T': 7, 'U': 5, 'V': 2, 'X': 1, 'Z': 1
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
special_tiles = {}
player_letters = []
temp_player_letters = []
current_letter = ""
current_letter_col = 0
current_word = {}
turn = False
client_socket = ""
score = 0
def done():
    global current_word
    current_word_str_keys = {f"{key[0]},{key[1]}": value for key, value in current_word.items()}
    data = {
        'reason' : "done",
        'current_word' : current_word_str_keys,
        'letters' : temp_player_letters,
    }
    client_socket.send(json.dumps(data).encode())
    current_word.clear()

ready = False
def ready():
    global ready
    ready_canvas = tk.Canvas(
        menu, width=600, height=140, bg="#a2d698", highlightthickness=0
    )
    ready_canvas.create_text(
        600 // 2, 140 // 2, text="You are ready", font=("Montserrat", 16), fill="black"
    )
    ready_canvas.place(x=0, y=140, width=600, height=140) 
    ready_button.config(state=tk.DISABLED, text="You are ready")
    info_label.config(text="Waiting for others...")
    ready = True

menu = tk.Tk()
menu.title("Scrabble")
menu.geometry("600x400")
menu.resizable(False, False)

title_label = tk.Label(
    menu,
    text="Scrabble",
    bg="white",
    justify="center",
    font=("Montserrat", 16, "bold"),
    anchor="center"
)
title_label.place(x=0, y=0, width=600, height=140)
ready_button = tk.Button(
    menu,
    text="Ready",
    bg="white",
    justify="center",
    font=("Montserrat", 16, "bold"),
    anchor="center",
    command=ready
)
ready_button.place(x=0, y=140, width=600, height=140)

info_label = tk.Label(
    menu,
    text="",
    bg="white",
    justify="center",
    font=("Montserrat", 10),
    anchor="center"
)
info_label.place(x=0, y=280, width=600, height=120)
def place_letter(row, col, letter):
    global board_frame, turn
    points = letter_points[letter]
    canvas = tk.Canvas(
        board_frame, width=40, height=40, bg="#dec5b6", highlightthickness=0
    )
    canvas.grid(row=row, column=col, sticky="nsew")
    canvas.create_text(
        40 // 2, 40 // 2, text=letter, font=("Montserrat", 16), fill="black"
    )
    canvas.create_text(
        40 - 5, 40 - 5, text=str(points), font=("Montserrat", 8), fill="black", anchor="se"
    )
"""SCRABBLE GAME - ELEMENTE"""
            # vvvv
def on_cell_click(row, col):
    global current_letter, turn
    if turn == True:
        if current_letter != "":
            place_letter(row, col, current_letter)
            current_word[(row, col)] = current_letter
            current_letter = ""
def place_special_tiles(): 
    print ("am intrat in place_special_tiles")
    cells = [[None for _ in range(15)] for _ in range(15)]
    cell_size = 600 // 15
    for row in range(15):
        for col in range(15):
            tile_type = special_tiles.get((row, col), "")
            # print(f"tile_type = {tile_type}; row = {row}, col = {col}")
            if tile_type == "x2_cuv":
                bg_color = "pink"
                text = "x2C"
            elif tile_type == "x3_litera":
                bg_color = "silver"
                text = "x3L"
            elif tile_type == "x2_litera":
                bg_color = "lightblue"
                text = "x2L"
            elif tile_type == "x3_cuv":
                bg_color = "#F08080"
                text = "x3C"
            elif tile_type == "stea":
                bg_color = "silver"
                text = "★" 
            elif tile_type != "":
                place_letter(row, col, tile_type)
                continue
            else:
                bg_color = "white"
                text = " "
            cell = tk.Button(
                board_frame, text=text, font=("Montserrat", 12), bg=bg_color, relief="ridge", width=cell_size, height=int(cell_size * 0.5),
                command=lambda r=row, c=col: on_cell_click(r, c)
            )
            cell.grid(row=row, column=col, sticky="nsew")
            cells[row][col] = cell
    root.update_idletasks()

    for i in range(15):
        board_frame.grid_rowconfigure(i, weight=1)
        board_frame.grid_columnconfigure(i, weight=1)

def on_letter_frame_click(c, color):
    global current_letter, prev_letter_col, temp_player_letters, turn, current_letter_col
    if turn == True:
        if current_letter == "":
            current_letter = temp_player_letters[c]
            current_letter_col = c
            temp_player_letters[c] = ""
            for col in range(7):
                letter = temp_player_letters[col]
                if letter == "":
                    points = "\n"
                    bg = "white"
                else:
                    points = letter_points[letter]
                    bg = "#dec5b6"
                btn = tk.Button(
                    letter_frame,
                    text=f"{letter}\n{points}",
                    font=("Montserrat", 12, "bold"),
                    bg=bg,
                    relief="ridge",
                    width=3,
                    height=3,
                    anchor="n",
                    justify="center",
                    command=lambda c=col, color=bg: on_letter_frame_click(c, color)
                )
                btn.grid(row=0, column=col, sticky="nsew")
        elif current_letter != "":
            clicked_letter = temp_player_letters[c]
            temp_player_letters[c] = current_letter
            points = letter_points[current_letter]
            bg = "#dec5b6"
            btn = tk.Button(
                letter_frame,
                text=f"{temp_player_letters[c]}\n{points}",
                font=("Montserrat", 12, "bold"),
                bg=bg,
                relief="ridge",
                width=3,
                height=3,
                anchor="n",
                justify="center",
                command=lambda c=c, color=bg: on_letter_frame_click(c, color)
            )
            btn.grid(row=0, column=c, sticky="nsew")
            if c != prev_letter_col:
                temp_player_letters[prev_letter_col] = clicked_letter
                if clicked_letter == "":
                    points = "\n"
                    bg = "white"
                else:
                    points = letter_points[clicked_letter]
                btn = tk.Button(
                    letter_frame,
                    text=f"{temp_player_letters[prev_letter_col]}\n{points}",
                    font=("Montserrat", 12, "bold"),
                    bg=bg,
                    relief="ridge",
                    width=3,
                    height=3,
                    anchor="n",
                    justify="center",
                    command=lambda c=prev_letter_col, color=bg: on_letter_frame_click(c, color)
                )
                btn.grid(row=0, column=prev_letter_col, sticky="nsew")
            current_letter = ""
        prev_letter_col = c

def letter_frame_config (temp_player_letters):
    for col in range(7):
        letter = temp_player_letters[col]
        points = letter_points[letter]
        
        btn = tk.Button(
            letter_frame,
            text=f"{letter}\n{points}",
            font=("Montserrat", 12, "bold"),
            bg="#dec5b6",
            relief="ridge",
            width=3,
            height=3,
            anchor="n",
            justify="center",
            command=lambda c=col, color="#dec5b6": on_letter_frame_click(c, color)
        )
        btn.grid(row=0, column=col, sticky="nsew")
def switch_letter():
    global current_letter, turn, player_letters, current_letter_col
    print(current_letter)
    if turn == True and current_letter!="":
        data_to_send = {
            "reason": f"switch {current_letter}, {current_letter_col}"
        }
        client_socket.send(json.dumps(data_to_send).encode('utf-8'))
        current_letter = ""
def undo():
    global temp_player_letters, player_letters, current_word
    current_word.clear()
    place_special_tiles()
    temp_player_letters = player_letters.copy()
    for col in range(7):
        letter = player_letters[col]
        if letter == "":
            points = "\n"
            bg = "white"
        else:
            points = letter_points[letter]
            bg = "#dec5b6"
        btn = tk.Button(
            letter_frame,
            text=f"{letter}\n{points}",
            font=("Montserrat", 12, "bold"),
            bg=bg,
            relief="ridge",
            width=3,
            height=3,
            anchor="n",
            justify="center",
            command=lambda c=col, color=bg: on_letter_frame_click(c, color)
        )
        btn.grid(row=0, column=col, sticky="nsew")
            # ^^^^^
"""SCRABBLE GAME - ELEMENTE"""
def show_board():
    # print("am intrat in show_board")
    global root, board_frame, letter_frame, turn_label, score_label
    root = tk.Tk()
    root.title("Scrabble")
    root.geometry("1000x600")
    root.resizable(False, False)
        
    board_frame = tk.Frame(root, bg="lightblue", width=600, height=600)
    board_frame.grid(row=0, column=0, padx=0, pady=0)
    board_frame.grid_propagate(False)

    text_frame = tk.Frame(root, bg="white", width=400, height=600)
    text_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
    text_frame.grid_propagate(False)

    letter_frame = tk.Frame(text_frame, bg="white", width=400, height=50)
    letter_frame.grid(row=0, column=0, padx=0, pady=0)
    letter_frame.grid_propagate(False)
    letter_frame_height = 40
    letter_frame_width = 280
    
    place_special_tiles()
    letter_frame_config(temp_player_letters)

    title_label = tk.Label(
        text_frame,
        text="Scrabble",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center"
    )
    title_label.place(x=0, y=0, width=400, height=100)
    def show_info_popup():
        popup = tk.Toplevel(root)
        popup.title("Informatii")
        scrabble_width = root.winfo_screenwidth()
        scrabble_height = root.winfo_screenheight()

        popup_width = 600
        popup_height = 400
        top = (scrabble_height//2) - (popup_height//2)
        right = (scrabble_width//2) - (popup_width//2)
        popup.geometry(f"{popup_width}x{popup_height}+{right}+{top}")
        text = "Cuvinte de 2 litere valide:\n"
        letter = "A"
        i=0
        while letter != "Z":
            text += valid_2_letter_words[i] + " "
            if letter != valid_2_letter_words[i][0]:
                text += "\n"
            letter = valid_2_letter_words[i][0]
            i += 1
        label = tk.Label(popup, text=text, font=("Montserrat",12), justify="left", anchor="nw")
        label.pack(padx= 10, pady=10, fill="both", expand=False)

    button_label = tk.Button(
        text_frame,
        text="Informatii",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center",
        command=show_info_popup
    )
    button_label.place(x=0, y=100, width=400, height=50)

    letter_frame.place(
        x=(400 - letter_frame_width) // 2,
        y=170,
        width=letter_frame_width,
        height=letter_frame_height
    )

    done_label = tk.Button(
        text_frame,
        text="Done",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center",
        command=done
    )
    done_label.place(x=0, y=230, width=400, height=50)
    switch_label = tk.Button(
        text_frame,
        text="Switch",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center",
        command=switch_letter
    )
    switch_label.place(x=0, y=280, width=400, height=50)

    undo_label = tk.Button(
        text_frame,
        text="Undo",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center",
        command=undo
    )
    undo_label.place(x=0, y=330, width=400, height=50)
    turn_label = tk.Label(
        text_frame,
        text="Wait for your turn..",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center"
    )
    turn_label.place(x=0, y=400, width=400, height=50)
    score_label = tk.Label(
        text_frame,
        text=f"Score: {score}",
        bg="white",
        justify="center",
        font=("Montserrat", 16, "bold"),
        anchor="center"
    )
    score_label.place(x=0, y=450, width=400, height=50)
    threading.Thread(target=game_rounds, daemon=True).start()
    root.mainloop()

def client():
    global ready, temp_player_letters, special_tiles, turn, turn_label, client_socket, player_letters
    ready = False
    host = "127.0.0.1"
    port = 5555
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(client_socket.recv(1800).decode())
    
    while ready == False:
        continue
    print("Ready")
    client_socket.send("ready".encode())
    data = client_socket.recv(1800).decode()
    if "special_tiles" in data and "letters" in data:
        parsed_data = json.loads(data)
        special_tiles = {
            tuple(map(int, key.split(','))): value
            for key, value in parsed_data['special_tiles'].items()
        }
        player_letters = parsed_data['letters']
        temp_player_letters = player_letters.copy()
        print (special_tiles)
        print (player_letters)
        show_board()
def game_rounds():
    global ready, temp_player_letters, special_tiles, turn, turn_label, player_letters, current_letter, score, score_label
    while True:
        data = client_socket.recv(1800).decode()
        print(data)
        if '}{' in data:
            messages = data.split('}{')
            messages[0] = messages[0] + '}'
            messages[-1] = '{' + messages[-1]
            parsed_data=json.loads(messages[-1])
        else:
            parsed_data=json.loads(data)
        print(parsed_data['reason'])
        
        if "It's your turn!" in data:
            turn = True
            turn_label.config(text="It's your turn!")
        elif "Player" in data:
            turn_label.config(text=parsed_data['reason'])
        elif parsed_data['reason'].isupper():
            temp_player_letters[current_letter_col] = parsed_data['reason']
            player_letters = temp_player_letters.copy()
            letter_frame_config(temp_player_letters)
            current_letter = ""
            turn = False
        elif parsed_data['reason'] == "check":
            print(parsed_data['status'])
            if parsed_data['status'] == "valid":
                player_letters = parsed_data['letters'].copy()
                temp_player_letters = parsed_data['letters'].copy()
                score += int(parsed_data['score'])
                score_label.config(text=f"Score: {parsed_data['score']}")
                special_tiles = {
                    tuple(map(int, key.split(','))): value
                    for key, value in parsed_data['special_tiles'].items()
                }
                place_special_tiles()
                letter_frame_config(temp_player_letters)
        elif parsed_data['reason'] == "update":
            special_tiles = {
                tuple(map(int, key.split(','))): value
                for key, value in parsed_data['special_tiles'].items()
            }
            print(special_tiles)
            place_special_tiles()
threading.Thread(target=client, daemon=True).start()
menu.mainloop()