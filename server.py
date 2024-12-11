import socket
import functions as func

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}...")

        conn, addr = server_socket.accept()
        print(f"Connected by {addr}, {conn}")
        with conn:
            while True:
                # Send the menu first
                conn.sendall(b"Select an option:\n"
                             b"1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                             b"2. What is the average water consumption per cycle in my smart dishwasher?\n"
                             b"3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n"
                             b"Type 'exit' to disconnect.\n")
                
                # Receive client's choice
                option = conn.recv(1024).decode().strip()
                
                if not option:  # Handle empty input
                    break

                # Process client's choice
                if option == "1":
                    result = func.compute_avg_moisture()
                    conn.sendall(f"The average moisture in the past 3 hours is: {result}\n".encode())
                elif option == "2":
                    result = func.compute_avg_water_consumption()
                    conn.sendall(f"The average water consumption per cycle is: {result} gallons.\n".encode())
                elif option == "3":
                    result = func.compute_max_electricity_consumption()
                    conn.sendall(f"The device that consumed the most electricity is: {result}\n".encode())
                elif option.lower() == "exit":
                    print(f"Client {conn} requested to exit.")
                    conn.sendall(b"Goodbye!\n")
                    break
                else:
                    conn.sendall(b"Invalid option. Please try again.\n")


if __name__ == "__main__":
    # host = str(input("Enter the host IP address: "))
    # port = int(input("Enter the port number: "))
    start_server()
