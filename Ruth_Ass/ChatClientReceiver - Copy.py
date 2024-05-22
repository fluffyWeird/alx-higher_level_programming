#!/usr/bin/python3
'''
import socket

# Dictionary to keep track of usernames and their assigned IPs and ports
user_ports = {}
# Dictionary to track active connections between users
connections = {}
start_port = 50000
BUFFER_SIZE = 2048

def handle_client_message(data, client_address, sock):
    message = data.decode()
    client_ip, client_port = client_address

    # Identifying the sender by matching IP and port
    sender = next((user for user, (ip, port) in user_ports.items() if ip == client_ip and port == client_port), None)

    if message.startswith("NAME"):
        username = message.split()[1]
        if username not in user_ports:
            assigned_port = start_port + len(user_ports)
            user_ports[username] = (client_ip, assigned_port)
            response = f"Hello {username}, you have been registered."
        else:
            response = "Error: This NAME is already taken."
    elif message.strip() == "LIST":
        if user_ports:
            user_list = ", ".join([f"{user}/{ip}:{port}" for user, (ip, port) in user_ports.items()])
            response = f"OK LIST = {user_list}"
        else:
            response = "No users registered."
    elif message.strip().startswith("CONN"):
        target = message.split()[1]
        if target in user_ports or sender:
            # Establish a direct connection between sender and target
            connections[sender] = user_ports[target]
            response = f"You are now connected to {target}."
        else:
            response = "Error: Target user does not exist or invalid sender."
    elif message.strip() == "QUIT":
        if sender in connections:
            del connections[sender]
            response = "OK Bye"
        else:
            response = "You are not connected."
    elif sender and sender in connections:
        # Relay messages to the connected user
        target_ip, target_port = connections[sender]
        sock.sendto(data.encode(), (target_ip, target_port))
        # Display the relayed message to confirm it was sent
        print(f"Message relayed to {sender}: {message}")
        return  # Prevent echoing back the message
    else:
        response = message  # Echo back non-command messages

    sock.sendto(response.encode(), client_address)

def receive_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((server_ip, server_port))
        print(f"Server running on {server_ip}:{server_port}")
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(f"Received: {data.decode()}")  # Print message content for debugging
            handle_client_message(data, addr, sock)

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    receive_messages(SERVER_IP, SERVER_PORT)
'''
'''
import socket
import re
import time

# Global variables
user_ports = {}  # Tracks usernames and their assigned IPs and ports
connections = {}  # Tracks active connections between users
last_activity = {}  # Tracks last activity time for garbage collection
start_port = 50000
BUFFER_SIZE = 2048
INACTIVITY_TIMEOUT = 1800  # 30 minutes timeout for inactivity
output_file_path = "server_log.txt"  # Path to the output file

def log_to_file(message):
    """Function to log messages to an output file."""
    with open(output_file_path, "a") as file:
        file.write(message + "\n")

def handle_client_message(data, client_address, sock):
    global last_activity  # Ensure to declare usage of the global variable
    message = data.decode().strip()
    client_ip, client_port = client_address

    log_to_file(f"Received message from {client_ip}:{client_port}: {message}")  # Log to file

    # Update the last activity time for the client
    last_activity[client_ip, client_port] = time.time()

    if re.match(r"^NAME (\w+)$", message):
        username = re.match(r"^NAME (\w+)$", message).group(1)
        if username not in user_ports:
            assigned_port = start_port + len(user_ports)
            user_ports[username] = (client_ip, assigned_port)
            response = f"OK Hello {username}"
            log_to_file(f"Registered {username} at {client_ip}:{assigned_port}")  # Log to file
        else:
            response = "Error: This NAME is already taken."
    elif message == "LIST":
        user_list = ", ".join([f"{user}/{ip}:{port}" for user, (ip, port) in user_ports.items()])
        response = f"OK LIST = {user_list}" if user_ports else "No users registered."
    elif message.startswith("CONN"):
        target = message.split()[1]
        if target in user_ports:
            connections[client_ip, client_port] = user_ports[target]
            response = f"OK Relaying to {target} at /{user_ports[target][0]}:{user_ports[target][1]}"
        else:
            response = "Error: Target user does not exist or invalid address."
    elif message == ".":
        if (client_ip, client_port) in connections:
            del connections[client_ip, client_port]
            response = "OK Relay stopped."
        else:
            response = "You are not connected."
    elif (client_ip, client_port) in connections:
        target_ip, target_port = connections[client_ip, client_port]
        sock.sendto(data, (target_ip, target_port))
        return  # Skip further processing
    else:
        response = message  # Default echo

    sock.sendto(response.encode(), client_address)
    log_to_file(f"Sent response to {client_ip}:{client_port}: {response}")  # Log to file

def receive_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((server_ip, server_port))
            print(f"Server running on {server_ip}:{server_port}")
        except socket.error as e:
            print(f"Failed to bind socket on {server_ip}:{server_port} due to {e}")
            return  # Exit if we cannot bind the socket

        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            handle_client_message(data, addr, sock)

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    receive_messages(SERVER_IP, SERVER_PORT)
'''
'''
import socket
import re
import time

# Global variables
user_ports = {}  # Tracks usernames and their assigned IPs and ports
connections = {}  # Tracks active connections between users
last_activity = {}  # Tracks last activity time for garbage collection
start_port = 50000
BUFFER_SIZE = 2048
INACTIVITY_TIMEOUT = 1800  # 30 minutes timeout for inactivity
output_file_path = "server_log.txt"  # Path to the output file

def initialize_log_file():
    """Creates or clears the log file at the start of the server's execution."""
    with open(output_file_path, "w") as file:
        file.write("Server Log Initiated\n")

def log_to_file(message):
    """Function to log messages to an output file."""
    try:
        with open(output_file_path, "a") as file:
            file.write(message + "\n")
    except Exception as e:
        print(f"Failed to write to log file: {e}")

def handle_client_message(data, client_address, sock):
    global last_activity
    message = data.decode().strip()
    client_ip, client_port = client_address

    log_to_file(f"Received message from {client_ip}:{client_port}: {message}")

    last_activity[client_ip, client_port] = time.time()

    if re.match(r"^NAME (\w+)$", message):
        username = re.match(r"^NAME (\w+)$", message).group(1)
        if username not in user_ports:
            assigned_port = start_port + len(user_ports)
            user_ports[username] = (client_ip, assigned_port)
            response = f"OK Hello {username} at Port {assigned_port}"
            log_to_file(f"Registered {username} at {client_ip}:{assigned_port}")
        else:
            response = "Error: This NAME is already taken."
    elif message == "LIST":
        user_list = ", ".join([f"{user}/{ip}:{port}" for user, (ip, port) in user_ports.items()])
        response = f"OK LIST = {user_list}" if user_ports else "No users registered."
    elif message.startswith("CONN"):
        target = message.split()[1]
        if target in user_ports:
            connections[client_ip, client_port] = user_ports[target]
            response = f"OK Relaying to {target} at /{user_ports[target][0]}:{user_ports[target][1]}"
        else:
            response = "Error: Target user does not exist or invalid address."
    elif message == ".":
        if (client_ip, client_port) in connections:
            del connections[client_ip, client_port]
            response = "OK Relay stopped."
        else:
            response = "You are not connected."
    elif (client_ip, client_port) in connections:
        target_ip, target_port = connections[client_ip, client_port]
        sock.sendto(data, (target_ip, target_port))
        return  # Skip further processing
    else:
        response = message  # Default echo

    sock.sendto(response.encode(), client_address)
    log_to_file(f"Sent response to {client_ip}:{client_port}: {response}")

def garbage_collector():
    current_time = time.time()
    to_remove = [key for key, last_time in last_activity.items() if current_time - last_time > INACTIVITY_TIMEOUT]
    for key in to_remove:
        if key in last_activity:
            del last_activity[key]
        user = next((user for user, (ip, port) in user_ports.items() if ip == key[0] and port == key[1]), None)
        if user:
            del user_ports[user]
            del connections[user]

def receive_messages(server_ip, server_port):
    initialize_log_file()  # Ensure log file is created or reset on server start
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((server_ip, server_port))
            print(f"Server running on {server_ip}:{server_port}")
        except socket.error as e:
            print(f"Failed to bind socket on {server_ip}:{server_port} due to {e}")
            return  # Exit if we cannot bind the socket

        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            handle_client_message(data, addr, sock)
            garbage_collector()

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    receive_messages(SERVER_IP, SERVER_PORT)

'''
import socket
import re
import time
import random

# Constants
USER_PORTS = {}
CONNECTIONS = {}
LAST_ACTIVITY = {}
START_PORT = 50000
BUFFER_SIZE = 2048
INACTIVITY_TIMEOUT = 1800  # 30 minutes
OUTPUT_FILE_PATH = "./server_log.txt"  # Path for the output file
SERVER_IP = 'localhost'
SERVER_PORT = 8888  # Default port as per requirement

def initialize_log_file():
    """Initializes the log file at the start of the server's execution."""
    with open(OUTPUT_FILE_PATH, "w") as file:
        file.write("Server Log Started\n")

def log_to_file(message):
    """Logs messages to an output file."""
    with open(OUTPUT_FILE_PATH, "a") as file:
        file.write(f"{message}\n")

def handle_client_message(data, client_address, sock):
    global LAST_ACTIVITY
    message = data.decode().strip()
    client_ip, client_port = client_address

    log_to_file(f"Received message from {client_ip}:{client_port}: {message}")

    # Simulate unreliability in the messaging channel
    if random.random() < 0.2:  # 20% chance to drop the packet
        log_to_file("Packet dropped due to unreliability simulation.")
        return

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
        user_list = ", ".join([f"{user}/{ip}:{port}" for user, (ip, port) in USER_PORTS.items()])
        response = f"OK LIST = {user_list}"
        log_to_file("Current registered users: " + user_list)
    elif message.startswith("CONN"):
        target = message.split()[1]
        if target in USER_PORTS:
            CONNECTIONS[client_ip, client_port] = USER_PORTS[target]
            response = f"OK Relaying to {target} at /{USER_PORTS[target][0]}:{USER_PORTS[target][1]}"
            log_to_file(f"Relaying from {client_ip}:{client_port} to {target}")
        else:
            response = "Error: Target user does not exist or invalid address."
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
    current_time = time.time()
    to_remove = [key for key, last_time in LAST_ACTIVITY.items() if current_time - last_time > INACTIVITY_TIMEOUT]
    for key in to_remove:
        if key in LAST_ACTIVITY:
            del LAST_ACTIVITY[key]
        user = next((user for user, (ip, port) in USER_PORTS.items() if ip == key[0] and port == key[1]), None)
        if user:
            del USER_PORTS[user]
            if user in CONNECTIONS:
                del CONNECTIONS[user]

def receive_messages(server_ip, server_port):
    initialize_log_file()  # Ensure log file is created
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((server_ip, server_port))
            print(f"Server running on {server_ip}:{server_port}")
        except socket.error as e:
            print(f"Failed to bind socket: {e}")
            return

        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            handle_client_message(data, addr, sock)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP Chat Client Receiver')
    parser.add_argument('-s', '--server', type=str, required=True, help='Server IP address')
    parser.add_argument('-p', '--port', type=int, required=True, help='Server port number')
    args = parser.parse_args()

    receive_messages(args.server, args.port)
