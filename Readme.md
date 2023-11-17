Sure, here's a README file for the provided server and client scripts:

### Chat

This server script creates a basic chat server allowing multiple clients to connect, join different rooms, exchange messages, and exit.

#### Usage:

1. **Server Setup:**
    - Ensure Python 3.x is installed.
    - Run the `server.py` file.

2. **Connecting Clients:**
    - Run the provided `client.py` file on the client-side.
    - Input a username to join the chat.
    - Use commands such as `/join room_name` to join a specific room, `/exit` to exit the chat, and `/roominfo` to see the room information.
    - Messages typed in the console will be sent to the server and broadcasted to other clients in the same room.

#### Requirements:
- Python 3.x

#### Server Setup:

1. **Server Initialization:**
    - Instantiate a `ChatServer` object with the server's IP address and port.
    - The server will listen for incoming connections on the specified IP address and port.
    - By default, it starts with a 'general' room and awaits client connections.

2. **Handling Client Connections:**
    - Upon a client's connection, a thread is spawned to handle the client.
    - The client enters their name and can join different rooms, send messages, or exit the chat.

3. **Client Handling:**
    - The server manages multiple rooms and clients within those rooms.
    - Clients can join specific rooms, receive room information, and leave the chat.

#### Client

The client script allows users to connect to the provided chat server, exchange messages, and perform basic commands.

#### Usage:

1. **Client Setup:**
    - Ensure Python 3.x is installed.
    - Run the `client.py` file.

2. **Connecting to the Server:**
    - Input a username when prompted to join the chat.
    - Type messages in the console, which will be sent to the server and broadcasted to other clients in the same room.
    - Use the `/exit` command to leave the chat server.
    - Use the `/join <room_name>` command to join room in the chat server.
    - Use the `/roominfo` command to display the current room you joined in the chat server.
    - Use the `/message <message_text>` command to send message to the current room in the chat server.

#### Requirements:
- Python 3.x

#### Client Features:

1. **Connecting to the Server:**
    - Create a socket connection to the server using the specified IP address and port.
    - Messages received from other clients are displayed in the console.
    - Users can type messages and send them to the server, which are then broadcasted.

2. **Client Management:**
    - Users can input a username and exchange messages with other connected clients.
    - The client script handles socket connections, sending and receiving messages, and allows users to exit the chat gracefully.

Feel free to modify and extend these scripts according to your specific use case and requirements!# chatpy
