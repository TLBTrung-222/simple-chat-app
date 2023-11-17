# Import required modules
import socket  # for communication
import threading  # for running concurrent thread


HOST = "127.0.0.1"
PORT = 1234  # you can choose between 0 to 65535
LISTENER_LIMIT = 5
active_clients = []


def listen_for_messages(connection, username):
    while 1:
        message = connection.recv(2048).decode("utf-8")

        if message != "":
            final_msg = username + "~" + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message from {username} is empty")
            continue


# Function to send any new message to all client that currently connecting to this server
def send_messages_to_all(message):
    for connection in active_clients:
        send_messages_to_client(connection[1], message)


def send_messages_to_client(connection, message):
    connection.sendall(message.encode())


# Function to receive username, think of it like authentication
def client_handler(connection):
    # Server will listen for client message that will contain the username
    while 1:
        # 2048: maximum size for message
        username = connection.recv(2048).decode("utf-8")
        if username != "":
            active_clients.append((username, connection))
            prompt_message = "SERVER~ " + f"{username} has joined the chat!"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty!")

    threading.Thread(
        target=listen_for_messages,
        args=(
            connection,
            username,
        ),
    ).start()


def main():
    # ? Creating the server socket class object
    # AF_INET: use IPv4 addresses
    # SOCK _STREAM: use TCP packets for communication (not UDP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ? Attach address (host + port) to server socket, so other socket can reach out to
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except:
        print(f"Unable to bind to host {HOST} with port {PORT}")

    # ? Specify maximum connection to server
    server.listen(LISTENER_LIMIT)

    # ? Server keep listening for any client connection
    while 1:
        # if server get any connection, it will return a new socket representing the connection and the address of the client (HOST + PORT)
        connection, address = server.accept()
        print(f"Successfully connected to client {address[0]}:{address[1]}")
        threading.Thread(target=client_handler, args=(connection,)).start()


# This sentence mean we only run main function if we run server.py, if we import this file as a module, the main function won't run automatically
if __name__ == "__main__":
    main()
