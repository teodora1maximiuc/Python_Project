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

def client():
    global ready
    host = "127.0.0.1"
    port = 5555
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(client_socket.recv(1024).decode())
    
    while ready == False:
        continue
    print("Ready")
    client_socket.send("ready".encode())

    while True:
        message = client_socket.recv(1024).decode()
        print(message)
        
        if "It's your turn!" in message:
            msg_to_send = input("Message: ")
            client_socket.send(msg_to_send.encode())
threading.Thread(target=client, daemon=True).start()
menu.mainloop()