import tkinter as tk
from tkinter import messagebox
import random
import string
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
}
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
    letter = "A"
    place_letter(row, col, letter)
def is_word_in_dict(word):
    file_path = r"C:\\Users\\Raluci\\OneDrive\\Desktop\\python\\Maximiuc_Teodora_3B2\\Scrabble-ProiectA\\ro_RO.dic"
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == word:
                return True
    return False
player_letters = []
computer_letters = []
while len(player_letters) < 7:
    random_letter = random.choice(alphabet)
    if letter_counts[random_letter] != 0:
        player_letters.append(random_letter)
        letter_counts[random_letter] -= 1
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
def on_letter_frame_click():
    i = 1
def letter_frame_config (player_letters):
    for col in range(7):
        letter = player_letters[col]
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
            command=lambda : on_letter_frame_click()
        )
        btn.grid(row=0, column=col, sticky="nsew")
letter_frame_config(player_letters)
root.mainloop()
