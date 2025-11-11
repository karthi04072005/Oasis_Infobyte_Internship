import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost. Use '0.0.0.0' to allow connections from other computers
PORT = 9999

# Lists to keep track of connected clients and their nicknames
clients = []
nicknames = []

def broadcast(message, _from_client=None):
    """Sends a message to all connected clients, except the sender if specified."""
    for client in clients:
        # Don't send the message back to the client who sent it
        if client != _from_client:
            try:
                client.send(message)
            except:
                # Handle broken connection
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket):
    """Handles a single client connection."""
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            if not message:
                # If no message, client disconnected
                break
                
            # Broadcast the received message to all other clients
            broadcast(message, client_socket)
            
        except Exception as e:
            # If an error occurs (e.g., client disconnects abruptly)
            print(f"Error handling client: {e}")
            break

    # When loop breaks, the client has disconnected
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
        
        nickname = nicknames[index]
        broadcast(f"--- {nickname} has left the chat. ---".encode('utf-8'))
        nicknames.remove(nickname)
        print(f"{nickname} disconnected.")

def start_server():
    """Main function to start the chat server."""
    # 1. Create a socket
    # AF_INET is for IPv4
    # SOCK_STREAM is for TCP (reliable connection)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Bind the socket to the address and port
    server.bind((HOST, PORT))
    
    # 3. Listen for incoming connections
    server.listen(5) # Allow up to 5 queued connections
    print(f"✅ Server is listening on {HOST}:{PORT}")

    while True:
        # 4. Accept a new connection
        # This blocks until a new client connects
        client_socket, address = server.accept()
        
        # 5. Ask client for a nickname
        client_socket.send('NICK'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        
        # Add new client to our lists
        nicknames.append(nickname)
        clients.append(client_socket)
        
        print(f"New connection from {address}. Nickname: {nickname}")
        client_socket.send("--- Welcome to the chat! ---".encode('utf-8'))
        broadcast(f"--- {nickname} has joined the chat! ---".encode('utf-8'), client_socket)
        
        # 6. Start a new thread to handle this client
        # This allows the server to handle multiple clients at once
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()