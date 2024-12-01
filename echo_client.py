import socket

def echo_client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            # Get server IP, port, and message from the user
            server_ip = input("Enter the server IP address: ")
            server_port = int(input("Enter the server port number: "))
            client_socket.connect((server_ip, server_port))

            while True:
                message = input("Enter the message to send (or 'exit' to quit): ")

                if message.lower() == 'exit':
                    print("Exiting...")
                    break

                # Send the message to the server
                client_socket.sendall(message.encode())

                # Receive the server's response
                response = client_socket.recv(1024)
                print("Server response:", response.decode())

            break  # Break the outer loop after closing connection

        except ValueError:
            print("Error: Please enter a valid IP address or port number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    client_socket.close()


if __name__ == "__main__":
    echo_client()