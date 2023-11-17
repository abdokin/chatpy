import signal
import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running_event = threading.Event()
        self.running_event.set()  # Set the event to start initially
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rooms = {}  
        self.rooms["general"] = []

        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(5)  # Listen for incoming connections
        print(f"Server is listening on {self.host}:{self.port}")

        while self.running_event.is_set():
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} has been established!")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()           
            except KeyboardInterrupt:
                self.stop()
                print("\nKeyboardInterrupt received. Shutting down the server...")
            except OSError as e:
                if self.running_event.is_set():
                    print(f"Error accepting connection: {e}")
    def handle_client(self, client_socket):
        try:
            client_socket.send("Enter your name: \n".encode('utf-8'))
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            self.join_room("general", client_socket, client_name)
            client_socket.send("Enter '/exit' to exit: '/help' to print help\n".encode('utf-8'))

            while self.running_event.is_set():
                self.handle_commands(client_socket, client_name)

        except ConnectionResetError as cre:
            print(f"Connection reset by peer: {cre}")
        except ConnectionAbortedError as cae:
            print(f"Connection aborted: {cae}")
        except Exception as ex:
            print(f"Error: {ex}")



    def join_room(self, room_name, client_socket, client_name):
        print(f'{client_name} is Joining room {room_name} \n')
        self.leave_room(client_socket,client_name)
        if room_name not in self.rooms:
            self.rooms[room_name] = [{client_name: client_socket}]
        else:
            # Check if the client name already exists in the room
            client_names = [list(client.keys())[0] for client in self.rooms[room_name]]
            if client_name in client_names:
                try:
                    client_socket.send(f"Error: Client name '{client_name}' already exists in the room.\n".encode('utf-8'))
                    self.handle_client(client_socket)
                except Exception as e:
                    print(f"Error sending error message: {e}")
                return
            else:
                self.rooms[room_name].append({client_name: client_socket})
        try:
            client_socket.send(f"Joined room: {room_name}\n".encode('utf-8'))
        except Exception as e:
            print(f"Error joining room: {e}")


    def get_client_room(self, client_name):
        for room_name, room_clients in self.rooms.items():
            for room_client in room_clients:
                for name, client in room_client.items():
                    if name == client_name:
                        return room_name
        return None 
    def handle_commands(self, client_socket, client_name):
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                return
            if message.startswith('/join '):
                new_room_name = message.split(' ')[1]
                self.join_room(new_room_name, client_socket, client_name)
            elif message.startswith('/exit'):
                self.remove_client(client_name)
            elif message.startswith('/roominfo'):
                self.room_info(client_socket)
            else:
                print(f"Received message from {client_name}: {message}")
                self.broadcast(message, client_name)
        except Exception as e:
            print(f"Error while handling message: {e}")
    def leave_room(self, client_socket, client_name):
        left_room = False
        for _, room_clients in self.rooms.items():
            for room_client in room_clients:
                for name, client in room_client.items():
                    if client_socket == client and name == client_name:
                        # Remove the client from the room
                        room_clients.remove(room_client)
                        left_room = True
                        break  # Stop after leaving the room

        if left_room:
            try:
                client_socket.send(f"You have left the room.\n".encode('utf-8'))
            except Exception as e:
                print(f"Error notifying the client: {e}")
        else:
            try:
                client_socket.send("You are not currently in any room.\n".encode('utf-8'))
            except Exception as e:
                print(f"Error notifying the client: {e}")
    def room_info(self, client_socket):
        try:
            rooms_info = "Room Information:\n"
            for room_name, room_clients in self.rooms.items():
                rooms_info += f"Room: {room_name}, Clients: {[list(client.keys())[0] for client in room_clients]}\n"
            client_socket.send(rooms_info.encode('utf-8'))
        except Exception as e:
            print(f"Error while getting room info: {e}")
        

    def broadcast(self, message, client_name):
        room_name = self.get_client_room(client_name)
        if room_name in self.rooms:
            for room_client in self.rooms[room_name]:
                for name, client in room_client.items():
                    if name != client_name:
                        try:
                            client.send(f"{client_name}: {message}\n".encode('utf-8'))
                        except Exception as e:
                            print(f"Error broadcasting message to client: {e}")
                            self.remove_client(client_name, room_name)


    def stop(self):
        self.running_event.clear()  
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()

        exit()

    def remove_client(self, client_name, room_name):
        room_name = self.get_client_room(client_name)
        try:
            if room_name:
                if room_name in self.rooms:
                    for room_client in self.rooms[room_name]:
                        for name, client in room_client.items():
                            if client_name == name:
                                self.rooms[room_name].remove(room_client)
                                client.close()
                                print(f"{name} disconnected.")
                                return
            else:
                for room, room_clients in self.rooms.items():
                    for room_client in room_clients:
                        for name, client in room_client.items():
                            if client_name == name:
                                room_clients.remove(room_client)
                                client.close()
                                print(f"{name} disconnected.")
                                return
        except Exception as e:
            print(f"Error while removing client: {e}")




if __name__ == "__main__":
    HOST = '127.0.0.1'  
    PORT = 8080

    chat_server = ChatServer(HOST, PORT)

    chat_server.start()

    def signal_handler(sig, frame):
        print("\nShutting down the server...")
        chat_server.stop()

    signal.signal(signal.SIGINT, signal_handler)

