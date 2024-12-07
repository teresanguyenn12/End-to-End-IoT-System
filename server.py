import socket
import functions as func

def start_server(host='127.0.0.1', port=65432):
    questions = {
        "1": "1. What is the average moisture inside my kitchen fridge in the past three hours?\n",
        "2": "2. What is the average water consumption per cycle in my smart dishwasher?\n",
        "3": "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n"
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}...")
        
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}, {conn}")
        with conn:
            while True:
                conn.sendall(b"Select an option:\n1. What is the average moisture inside my kitchen fridge in the past three hours?\n2. What is the average water consumption per cycle in my smart dishwasher?\n3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\nType 'exit' to disconnect.\n")
                option = conn.recv(1024).decode().strip()
                
                if not option:
                    break
                print(option)
                print("===============")

                # MESSAGE to client
                if option == "1":
                    result = func.compute_avg_moisture()  
                    conn.sendall(f"{result}\n".encode())
                elif option == "2":
                    result = func.compute_avg_water_consumption() 
                    conn.sendall(f"{result}\n".encode())
                elif option == "3":
                    result = func.compute_max_electricity_consumption()
                    conn.sendall(f"{result}\n".encode())
                elif option.lower() == "exit":
                    print(f"Client {conn} requested to exit.")
                    break
                else:
                    conn.sendall("Invalid option. Please select a valid option.\n")


if __name__ == "__main__":
    # host = str(input("Enter the host IP address: "))
    # port = int(input("Enter the port number: "))
    start_server()
