import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # The server's IP (localhost for testing)
PORT = 9999

def receive_messages(client_socket):
    """Constantly listens for messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == 'NICK':
                # Server is asking for our nickname
                client_socket.send(nickname.encode('utf-8'))
            else:
                # Print the received message
                print(message)
        except Exception as e:
            # Handle disconnection or errors
            print("❌ An error occurred! Disconnected from server.")
            print(e)
            client_socket.close()
            break

def send_messages(client_socket):
    """Waits for user input and sends it to the server."""
    while True:
        try:
            # Get user input
            message = input() # This blocks until you press Enter
            
            # Format and send the message
            formatted_message = f"<{nickname}>: {message}"
            client_socket.send(formatted_message.encode('utf-8'))
        except EOFError:
            break
        except Exception as e:
            print(f"Error sending message: {e}")
            client_socket.close()
            break

def start_client():
    """Main function to start the chat client."""
    global nickname # Make nickname global so threads can access it
    
    nickname = input("Choose your nickname: ")
    
    # 1. Create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. Connect to the server
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("❌ Connection failed. Is the server running?")
        return

    print(f"✅ Connected to server as {nickname}!")
    
    # 3. Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    
    # 4. Start the main send loop (this will run in the main thread)
    send_messages(client)

if __name__ == "__main__":
    start_client()