import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

DARK_GREY = "#121212"
MEDIUM_GREY = "#1F1B24"
OCEAN_BLUE = "#464EB8"
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


def add_message(message):
    message_textbox.config(state=tk.NORMAL)
    message_textbox.insert(tk.END, message + "\n")
    message_textbox.config(state=tk.DISABLED)


def connect():
    print("Button is working")


def send_message():
    print("Sending message")


# create the main window object
root = tk.Tk()
root.geometry("600x600")
root.title("Messenger client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(
    top_frame, text="Enter username: ", font=FONT, bg=DARK_GREY, fg=WHITE
)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

user_name = tk.Button(
    top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, command=connect
)
user_name.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=45)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(
    bottom_frame, text="Send", bg=OCEAN_BLUE, font=BUTTON_FONT, command=send_message
)
message_button.pack(side=tk.LEFT)

message_box = scrolledtext.ScrolledText(
    middle_frame,
    font=SMALL_FONT,
    bg=MEDIUM_GREY,
    width=67,
    height=34,
    highlightcolor=WHITE,
    foreground=WHITE,
    state=tk.DISABLED,
)
message_box.pack(side=tk.TOP)

HOST = "127.0.0.1"
PORT = 1234  # you can choose between 0 to 65535


def send_messages_to_server(client):
    while 1:
        message = input("Message: ")
        if message != "":
            client.sendall(message.encode())
        else:
            print("Empty message!")
            exit(0)


# listen for messages from server
def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode("utf-8")
        if message != "":
            username, message_content = message.split("~")[0], message.split("~")[1]
            print(f"[{username}] {message_content}")
        else:
            print("Message received from server is empty")


def communicate_to_server(client):
    username = input("Enter user name: ")
    if username != "":
        client.sendall(username.encode())
    else:
        print("User name can not empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    send_messages_to_server(client)


def main():
    root.mainloop()

    # Creating client socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        client.connect(
            (HOST, PORT)
        )  # now the client represent the connection to server
        print("Successfully connect to server")
        communicate_to_server(client)

    except:
        print(f"Unable to connect to the server {HOST}:{PORT}")


if __name__ == "__main__":
    main()
