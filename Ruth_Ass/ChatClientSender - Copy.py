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
'''
'''
import socket
import threading

def listen_for_messages(sock):
    while True:
        message, _ = sock.recvfrom(2048)
        print("Received:", message.decode())

def send_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Start listening for incoming messages
        threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

        while True:
            message = input("Enter command or message: ")
            if message.strip() == "QUIT":
                sock.sendto(message.encode(), (server_ip, server_port))
                break  # Exit the program after sending QUIT
            sock.sendto(message.encode(), (server_ip, server_port))

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    send_messages(SERVER_IP, SERVER_PORT)
'''
'''
import socket
import threading

def listen_for_messages(sock):
    """ Continuously listen for incoming messages from the server and print them. """
    while True:
        message, _ = sock.recvfrom(2048)  # Adjust buffer size if needed
        print("Received:", message.decode())

def send_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Start a thread to listen for messages asynchronously
        threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

        while True:
            message = input("Enter command or message: ").strip()
            if message == "QUIT":
                sock.sendto(message.encode(), (server_ip, server_port))
                print("Exiting...")
                break  # Exit after sending QUIT
            sock.sendto(message.encode(), (server_ip, server_port))

if __name__ == "__main__":
    SERVER_IP = 'localhost'  # Server IP address
    SERVER_PORT = 12345      # Server port number
    send_messages(SERVER_IP, SERVER_PORT)
'''
'''
import socket
import threading

def listen_for_messages(sock):
    """ Continuously listen for incoming messages from the server and print them. """
    global server_port  # Use the global variable to update the port if assigned
    while True:
        try:
            message, _ = sock.recvfrom(2048)  # Adjust buffer size if needed
            print("\nReceived:", message.decode())  # Displays messages received from the server

            # Check if this is a port assignment message
            if "OK Hello" in message.decode():
                # Attempt to parse the message to find a port number
                parts = message.decode().split()
                try:
                    # Assuming the server sends something like "OK Hello Username at Port XXXXX"
                    port_index = parts.index("Port") + 1  # Find the index of 'Port' and get the next item
                    new_port = int(parts[port_index])
                    server_port = new_port
                    print(f"Updated local port to {server_port}")
                except (ValueError, IndexError) as e:
                    print("Failed to parse port number:", e)
        except Exception as e:
            print("Error receiving message:", e)
            break

def send_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Start a thread to listen for messages asynchronously
        threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

        print("Type your messages below. Type 'QUIT' to exit.")
        while True:
            try:
                message = input("Enter command or message: ").strip()
                if message == "QUIT":
                    sock.sendto(message.encode(), (server_ip, server_port))
                    print("Exiting...")
                    break  # Exit after sending QUIT
                sock.sendto(message.encode(), (server_ip, server_port))
            except Exception as e:
                print("Error sending message:", e)
                break

if __name__ == "__main__":
    SERVER_IP = 'localhost'  # Server IP address
    SERVER_PORT = 12345      # Initial server port number
    send_messages(SERVER_IP, SERVER_PORT)
'''
import socket
import threading

def listen_for_messages(sock):
    """ Continuously listen for incoming messages from the server and print them. """
    global server_port  # Use the global variable to update the port if assigned
    while True:
        try:
            message, _ = sock.recvfrom(2048)  # Adjust buffer size if needed
            print("\nReceived:", message.decode())  # Displays messages received from the server

            # Check if this is a port assignment message
            if "OK Hello" in message.decode():
                parts = message.decode().split()
                if "Port" in parts:
                    port_index = parts.index("Port") + 1
                    new_port = int(parts[port_index])
                    server_port = new_port
                    print(f"Updated local port to {server_port}")
                else:
                    print("No port number found in the server response.")
        except Exception as e:
            print("Error receiving message:", e)
            break

def send_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Start a thread to listen for messages asynchronously
        threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

        print("Type your messages below. Type 'QUIT' to exit.")
        while True:
            try:
                message = input("Enter command or message: ").strip()
                if message == "QUIT":
                    sock.sendto(message.encode(), (server_ip, server_port))
                    print("Exiting...")
                    break  # Exit after sending QUIT
                sock.sendto(message.encode(), (server_ip, server_port))
            except Exception as e:
                print("Error sending message:", e)
                break

if __name__ == "__main__":
    SERVER_IP = 'localhost'  # Server IP address
    SERVER_PORT = 12345      # Initial server port number
    send_messages(SERVER_IP, SERVER_PORT)
