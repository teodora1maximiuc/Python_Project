import tkinter as tk
from tkinter import messagebox
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
for row in range(15):
    for col in range(15):
        if (row, col) not in special_tiles:
            special_tiles[(row, col)] = ""
current_word = {}
current_letter = ""
prev_letter_col = -1
turn = 1
def place_letter(row, col, letter):
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
def on_cell_click(row, col):
    global current_letter
    if current_letter != "":
        place_letter(row, col, current_letter)
        current_word[(row, col)] = current_letter
        current_letter = ""
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
    while special_tiles[(row, startCol - i - 1)].isupper():
        i += 1
    while special_tiles[(row, endCol + j + 1)].isupper():
        j += 1
    return i, j

def check_vertical_extension(startRow, endRow, col):
    i = 0
    j = 0
    while special_tiles[(startRow - i - 1, col)].isupper():
        i += 1
    while special_tiles[(endRow + j + 1, col)].isupper():
        j += 1
    return i, j

def apply_bonus(row, col):
    global special_tiles, current_word
    tile_type = special_tiles[(row, col)]
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

def get_orizontal_word(i, j, row, col):
    word_points = 0
    to_multiply = 1
    word = ""
    pos = col - i
    while pos != col + j + 1:
        if special_tiles[(row, pos)].isupper():
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

def get_vertical_word(i, j, row, col):
    word_points = 0
    to_multiply = 1
    word = ""
    pos = row - i
    while pos != row + j + 1:
        if special_tiles[(pos, col)].isupper():
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

def validate_word():
    global player_letters, temp_player_letters, root, turn, current_word
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
                if special_tiles[(rows[0], pos)].isupper():
                    word += special_tiles[(rows[0], pos)]
                    word_points += letter_points[special_tiles[(rows[0], pos)]]
                elif (rows[0], pos) in current_word: 
                    word += current_word[(rows[0], pos)]
                    add, mul = apply_bonus(rows[0], pos)
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
                        word, add = get_vertical_word(i, j, rows[0], column)
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
                    add, mul = apply_bonus(pos, columns[0])
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
                        word, add = get_orizontal_word(i, j, row, columns[0])
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
        player_letters = temp_player_letters.copy()
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
        print (player_letters)
        temp_player_letters = player_letters.copy()
        letter_frame_config(temp_player_letters)
        for key, item in current_word.items():
            special_tiles[key] = item
            print(f"key = {key}; item = {item}")
        current_word.clear()
    elif valid == 0:
        print("Invalid word!")
        popup = tk.Toplevel(root)
        popup.title("Invalid")
        scrabble_width = root.winfo_screenwidth()
        scrabble_height = root.winfo_screenheight()
        popup_width = 200
        popup_height = 50
        top = (scrabble_height//2) - (popup_height//2)
        right = (scrabble_width//2) - (popup_width//2)
        popup.geometry(f"{popup_width}x{popup_height}+{right}+{top}")
        text = "Cuvant invalid!\n"
        label = tk.Label(popup, text=text, font=("Montserrat",12), justify="left", anchor="nw")
        label.pack(padx=10, pady=10, fill="both", expand=True)
player_letters = []
computer_letters = []
while len(player_letters) < 7:
    random_letter = random.choice(alphabet)
    if letter_counts[random_letter] != 0:
        player_letters.append(random_letter)
        letter_counts[random_letter] -= 1
player_letters[2] = "J"
player_letters[3] = "E"
temp_player_letters = player_letters.copy()
while len(computer_letters) < 7:
    random_letter = random.choice(alphabet)
    if letter_counts[random_letter] != 0:
        computer_letters.append(random_letter)
        letter_counts[random_letter] -= 1

root = tk.Tk()
root.title("Scrabble")
root.geometry("1000x600")
root.resizable(False, False)

board_frame = tk.Frame(root, bg="lightblue", width=600, height=600)
board_frame.grid(row=0, column=0, padx=0, pady=0)
board_frame.grid_propagate(False)
def place_special_tiles(): 
    cells = [[None for _ in range(15)] for _ in range(15)]
    cell_size = 600 // 15
    for row in range(15):
        for col in range(15):
            tile_type = special_tiles.get((row, col), "")
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

    for i in range(15):
        board_frame.grid_rowconfigure(i, weight=1)
        board_frame.grid_columnconfigure(i, weight=1)
place_special_tiles()

text_frame = tk.Frame(root, bg="white", width=400, height=600)
text_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
text_frame.grid_propagate(False)

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
letter_frame = tk.Frame(text_frame, bg="white", width=400, height=50)
letter_frame.grid(row=0, column=0, padx=0, pady=0)
letter_frame.grid_propagate(False)
letter_frame_height = 40
letter_frame_width = 280

letter_frame.place(
    x=(400 - letter_frame_width) // 2,
    y=170,
    width=letter_frame_width,
    height=letter_frame_height
)
def on_letter_frame_click(c, color):
    global current_letter, prev_letter_col, temp_player_letters
    if current_letter == "":
        current_letter = temp_player_letters[c]
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
letter_frame_config(temp_player_letters)
done_label = tk.Button(
    text_frame,
    text="Done",
    bg="white",
    justify="center",
    font=("Montserrat", 16, "bold"),
    anchor="center",
    command=validate_word
)
done_label.place(x=0, y=230, width=400, height=50)
switch_label = tk.Button(
    text_frame,
    text="Switch",
    bg="white",
    justify="center",
    font=("Montserrat", 16, "bold"),
    anchor="center",
    command=show_info_popup
)
switch_label.place(x=0, y=280, width=400, height=50)
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
root.mainloop()
