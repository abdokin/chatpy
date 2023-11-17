import socket
import threading

MAX_RETRIES = 5
running = True  # Variable to control the retrying thread

def receive_messages(client_socket):
    global running
    retries = 0
    while retries < MAX_RETRIES and running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"{message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            retries += 1
    if retries == MAX_RETRIES:
        print(f"Failed to receive messages after {MAX_RETRIES} retries. Closing connection.")
    client_socket.close()

def main():
    global running
    server_host = '127.0.0.1'  # Replace with the server's IP address or 'localhost'
    server_port = 8080  # Use the same port number as the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        print("Connected to the chat server!")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while running:
            try:
                username = input(">>")
                client_socket.send(username.encode('utf-8'))
            except KeyboardInterrupt:
                print("\nExiting...")
                running = False  # Set running to False to stop the retrying thread
                client_socket.close()
                return  # Exit the program on KeyboardInterrupt
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
