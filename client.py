import socket

HOST = '127.0.0.1'
PORT = 23456

def echo_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            options = client_socket.recv(1024)
            decoded_messgage = options.decode('utf-8')
            print(decoded_messgage)
            option = input("Select an option (type 'exit' to quit): ")
            if option.lower() == 'exit':
                print("Closing connection...")
                break

            # Send message to server
            client_socket.send(option.encode())

            # Receive and print the response from the server
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode()}\n")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def displayData(data):
    for d in data:
        print(d)

if __name__ == "__main__":
    echo_client()
