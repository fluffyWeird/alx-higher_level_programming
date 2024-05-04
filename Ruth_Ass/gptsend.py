#!/usr/bin/python3
'''
import socket

def send_messages(server_ip, server_port):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            # Prompt user for input
            message = input("Enter command or message: ")
            # Send the encoded message to the specified server and port
            sock.sendto(message.encode(), (server_ip, server_port))

if __name__ == "__main__":
    # Define the server IP and port
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    # Call the function to start sending messages
    send_messages(SERVER_IP, SERVER_PORT)
'''

import socket

def send_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            message = input("Enter command or message: ")
            sock.sendto(message.encode(), (server_ip, server_port))
            # Wait to receive a response from the server
            response, _ = sock.recvfrom(2048)
            print("Response from server:", response.decode())

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    send_messages(SERVER_IP, SERVER_PORT)
