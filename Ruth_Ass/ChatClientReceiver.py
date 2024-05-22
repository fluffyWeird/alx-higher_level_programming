import socket
import argparse
import re
import time
import sys

# Constants
USER_PORTS = {}
CONNECTIONS = {}
LAST_ACTIVITY = {}
START_PORT = 50000
BUFFER_SIZE = 2048
INACTIVITY_TIMEOUT = 1800
OUTPUT_FILE_PATH = "./server_log.txt"

def initialize_log_file():
    """Initializes the log file at the start of the server's execution."""
    with open(OUTPUT_FILE_PATH, "w") as file:
        file.write("Server Log Started\n")

def log_to_file(message):
    """Logs messages to an output file."""
    with open(OUTPUT_FILE_PATH, "a") as file:
        file.write(f"{message}\n")

def handle_client_message(data, client_address, sock):
    """Handle incoming messages based on their command type."""
    global LAST_ACTIVITY
    message = data.decode().strip()
    client_ip, client_port = client_address

    log_to_file(f"Received message from {client_ip}:{client_port}: {message}")

    LAST_ACTIVITY[client_ip, client_port] = time.time()

    if re.match(r"^NAME (\w+)$", message):
        username = re.match(r"^NAME (\w+)$", message).group(1)
        if username not in USER_PORTS:
            assigned_port = START_PORT + len(USER_PORTS)
            USER_PORTS[username] = (client_ip, assigned_port)
            response = f"OK Hello {username} at Port {assigned_port}"
            log_to_file(f"Registered {username} at {client_ip}:{assigned_port}")
        else:
            response = "Error: This NAME is already taken."
    elif message == "LIST":
        if USER_PORTS:
            user_list = ", ".join([f"{user}/{ip}:{port}" for user, (ip, port) in USER_PORTS.items()])
            response = f"OK LIST = {user_list}"
            log_to_file("Current registered users: " + user_list)
        else:
            response = "No users registered."
    elif message.startswith("CONN"):
        target = message.split()[1]
        if target in USER_PORTS and (client_ip, client_port) in USER_PORTS.values():
            CONNECTIONS[client_ip, client_port] = USER_PORTS[target]
            response = f"OK Relaying to {target} at /{USER_PORTS[target][0]}:{USER_PORTS[target][1]}"
            log_to_file(f"Relaying from {client_ip}:{client_port} to {target}")
        else:
            response = "Error: Target user does not exist or invalid sender."
    elif message == ".":
        if (client_ip, client_port) in CONNECTIONS:
            del CONNECTIONS[client_ip, client_port]
            response = "OK Relay stopped."
            log_to_file(f"Relay stopped for {client_ip}:{client_port}")
        else:
            response = "You are not connected."
    elif (client_ip, client_port) in CONNECTIONS:
        target_ip, target_port = CONNECTIONS[client_ip, client_port]
        sock.sendto(data, (target_ip, target_port))
        return  # Skip further processing
    else:
        response = message  # Default echo

    sock.sendto(response.encode(), client_address)
    log_to_file(f"Sent response to {client_ip}:{client_port}: {response}")

def garbage_collector():
    """Remove inactive users and clear their associated connection and last activity tracking."""
    current_time = time.time()
    to_remove = [key for key, last_time in LAST_ACTIVITY.items() if current_time - last_time > INACTIVITY_TIMEOUT]
    for key in to_remove:
        if key in LAST_ACTIVITY:
            del LAST_ACTIVITY[key]
        user = next((user for user, (ip, port) in USER_PORTS.items() if ip == key[0] and port == key[1]), None)
        if user:
            del USER_PORTS[user]
            del CONNECTIONS[user]

def receive_messages(server_ip, server_port, output_file=None):
    """Set up the server to receive messages and handle them."""
    initialize_log_file()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((server_ip, server_port))
            print(f"Server running on {server_ip}:{server_port}")
        except socket.error as e:
            print(f"Failed to bind socket: {e}")
            return

        if output_file:
            with open(output_file, 'wb') as file:
                while True:
                    data, _ = sock.recvfrom(BUFFER_SIZE)
                    if data == b'EOF':
                        break
                    file.write(data)
        else:
            while True:
                data, _ = sock.recvfrom(BUFFER_SIZE)
                if data.decode() == 'EOF':
                    break
                print(data.decode())

def receive_data(server_ip, server_port, output_filename):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_ip, server_port))
        print(f"Server running on {server_ip}:{server_port}")

        with open(output_filename, 'wb') as file:
            while True:
                data, _ = sock.recvfrom(1024)
                if data == b'EOF':
                    print("File transfer completed.")
                    break
                file.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat Client Receiver')
    parser.add_argument('-s', '--server', type=str, required=True, help='Server IP address')
    parser.add_argument('-p', '--port', type=int, required=True, help='Server port number')
    parser.add_argument('-f', '--filename', required=True, help='Output file name')
    args = parser.parse_args()

    receive_data(args.server, args.port, args.filename)