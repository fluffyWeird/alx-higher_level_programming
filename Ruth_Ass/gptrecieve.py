#!/usr/bin/python3
import socket

import socket

user_ports = {}
connections = {}
start_port = 50000
BUFFER_SIZE = 2048

def handle_client_message(data, client_address, sock):
    message = data.decode()
    client_ip, client_port = client_address

    if message.startswith("NAME"):
        username = message.split()[1]
        if username not in user_ports:
            assigned_port = start_port + len(user_ports)
            user_ports[username] = (client_ip, assigned_port)
            response = f"Hello {username}, you have been registered."
        else:
            response = "Error: This NAME is already taken."
    elif message.strip().startswith("PORT"):
        username = message.split()[1]
        if username in user_ports:
            _, port = user_ports[username]
            response = f"{username} is registered at port {port}."
        else:
            response = "Error: Username is wrong or unregistered."
    elif message.strip().startswith("CONN"):
        target = message.split()[1]
        if target in user_ports:
            connections[client_ip, client_port] = user_ports[target]
            response = f"You are now connected to {target}."
        else:
            response = "Error: Target user does not exist."
    elif message.strip() == "QUIT":
        if (client_ip, client_port) in connections:
            del connections[client_ip, client_port]
            response = "OK Bye"
        else:
            response = "You are not connected."
    else:
        response = message  # Echo back non-command messages

    sock.sendto(response.encode(), client_address)

def receive_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((server_ip, server_port))
        print(f"Server running on {server_ip}:{server_port}")
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(data.decode())
            handle_client_message(data, addr, sock)

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    receive_messages(SERVER_IP, SERVER_PORT)
