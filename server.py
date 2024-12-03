import socket
import threading
from pprint import pprint
import functions as func
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#HOST = str(os.getenv('HOST'))
#PORT = int(os.getenv('PORT'))


def handle_client(client_socket, client_address):
    print(f"Client connected: {client_address}")
    try:
        while True:

            query_message = (
                "Query Options:\n"
                "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                "2. What is the average water consumption per cycle in my smart dishwasher?\n"
                "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n"
                "Type 'exit' to disconnect.\n"
            )
            # MESSAGE to client 
            client_socket.send(query_message.encode())
            
            # RESPONSE from client
            user_input = client_socket.recv(1024)
            if not user_input:
                print(f"Client disconnected: {client_address}")
                break
            
            # Decode the user input
            option = user_input.decode().strip()
            print(f"Received from {client_address}: {option}")

            # MESSAGE to client
            if option == "1":
                print("Processing Option 1...")
                result = func.compute_avg_moisture()  
                client_socket.send(f"{result}\n".encode())
            elif option == "2":
                print("Processing Option 2...")
                result = func.compute_avg_water_consumption() 
                client_socket.send(f"{result}\n".encode())
            elif option == "3":
                print("Processing Option 3...")
                result = func.compute_max_electricity_consumption()
                client_socket.send(f"{result}\n".encode())
            elif option.lower() == "exit":
                print(f"Client {client_address} requested to exit.")
                break
            else:
                client_socket.send(
                    "Invalid option. Please try one of the following:\n"
                    "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                    "2. What is the average water consumption per cycle in my smart dishwasher?\n"
                    "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n".encode()
                    )
            
    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()


def echo_server():
    # Prompt for server IP and port
    HOST = input("Enter the server's IP address: ").strip()
    PORT = int(input("Enter the server's port: ").strip())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}, waiting for connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    echo_server()
