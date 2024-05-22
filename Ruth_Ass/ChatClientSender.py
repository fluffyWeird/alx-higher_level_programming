import socket
import argparse

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
def send_file_content(server_ip, server_port, input_filename):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock, open(input_filename, 'rb') as file:
        data = file.read(1024)
        while data:
            sock.sendto(data, (server_ip, server_port))
            data = file.read(1024)
        sock.sendto(b'EOF', (server_ip, server_port))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat Client Sender')
    parser.add_argument('-s', '--server', type=str, required=True, help='Server IP address')
    parser.add_argument('-p', '--port', type=int, required=True, help='Server port number')
    parser.add_argument('-f', '--filename', required=True, help='File to send')
    args = parser.parse_args()

    send_file_content(args.server, args.port, args.filename)