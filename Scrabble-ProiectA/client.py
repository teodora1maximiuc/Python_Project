import socket
import tkinter as tk
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

game_started = False

def ready():
    global game_started
    client_socket.sendall(b"ready")
    ready_canvas = tk.Canvas(
        menu, width=600, height=140, bg="#a2d698", highlightthickness=0
    )
    ready_canvas.create_text(
        600 // 2, 140 // 2, text="You are ready", font=("Montserrat", 16), fill="black"
    )
    ready_canvas.place(x=0, y=140, width=600, height=140)
    ready_button.config(state=tk.DISABLED, text="You are ready")
    info_label.config(text="Waiting for others...")
    
    threading.Thread(target=check_game_start, daemon=True).start()

def check_game_start():
    global game_started
    while not game_started:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data == "Game has started!":
                info_label.config(text="Game has started!")
                print("Game started")
                game_started = True
                break
        except (ConnectionResetError, ConnectionAbortedError) as e:
            info_label.config(text="Game already in progress.")
            print("Connection lost. Please try again later.")
            break

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

menu.mainloop()
