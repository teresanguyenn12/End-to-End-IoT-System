import socket
import threading
import config.mongo as mongo
from pprint import pprint
HOST = '127.0.0.1'
PORT = 23456

def handle_client(client_socket, client_address):
    print(f"Client connected: {client_address}")
    try:
        while True:

            client_socket.send(f"Query Options:\n 1. What is the average moisture inside my kitchen fridge in the past three hours?\n 2. What is the average water consumption per cycle in my smart dishwasher?\n 3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n".encode())
            user_input = client_socket.recv(1024)
            if not user_input:
                print(f"Client disconnected: {client_address}")
                break

            option = user_input.decode()
            print(f"Received from {client_address}: {option}")

            if option == "1":
                print("Starting Option 1...")
                data = mongo.get_refrigerator_data()
                for document in data:
                    pprint(document, indent=4)
                    #client_socket.send(str(document).encode())
                # client_socket.send(data.encode())
            elif option == "2":
                print("Starting Option 2...")
                client_socket.send("Option 2\n".encode())
            elif option == "3":
                print("Starting Option 3...")
                client_socket.send("Option 3\n".encode())
            else:
                print("Invalid option...\n")
                client_socket.send("Invalid option\n".encode())
                continue
            
    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()

def echo_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 queued connections
    print(f"Server started on {HOST}:{PORT}, waiting for connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            # Handle each client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    echo_server()
