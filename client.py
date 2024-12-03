import socket

HOST = '127.0.0.1'
PORT = 23456

def echo_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            # Receive the query options from the server
            options = client_socket.recv(1024)
            if not options:
                print("Server disconnected.")
                break

            # Decode and print the query options
            print(options.decode())

            # Prompt the user for input
            option = input("Select an option (type 'exit' to quit): ").strip()

            # Send the selected option to the server
            client_socket.send(option.encode())

            if option.lower() == 'exit':
                print("Closing connection...")
                break

            # Receive the response from the server
            response = client_socket.recv(1024)
            if not response:
                print("Server disconnected.")
                break
            print(f"\nResponse: {response.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    echo_client()
