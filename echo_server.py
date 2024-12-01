import socket

def echo_server():
    # Get IP and port from user
    server_ip = input("Enter the IP address for the server to bind to (or 'localhost'): ")
    server_port = int(input("Enter the port number for the server to bind to: "))

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the provided IP address and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server started on {server_ip}:{server_port}, waiting for connections...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        client_ip, client_port = client_address  # Unpack the client address tuple

        print(f"Client connected from IP: {client_ip}, Port: {client_port}")

        while True:
            # Receive a message from the client
            message = client_socket.recv(1024)
            if not message:
                print(f"Connection with {client_ip}:{client_port} closed.")
                break

            decoded_message = message.decode()
            print(f"Received message from {client_ip}:{client_port}: {decoded_message}")

            # Convert the message to uppercase
            response_message = decoded_message.upper()

            # Send the uppercase message back to the client
            client_socket.sendall(response_message.encode())

        client_socket.close()


if __name__ == "__main__":
    echo_server()