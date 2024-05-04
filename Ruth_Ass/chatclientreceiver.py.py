from socket import *
import sys


# Default values
address = None

port = None
timeout_val = 1

SeqNum = 0

# Parse command-line arguments

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-s" and i + 1 < len(sys.argv):

        address = sys.argv[i + 1]
        print(address)

    elif sys.argv[i] == "-p" and i + 1 < len(sys.argv):
        port = int(sys.argv[i + 1])

        print(port)

# Check if address and port are provided

if address is None or port is None:
    print("Error: Server address and port number are required.")

    sys.exit(1)

# Define packet

def calculate_checksum(data):
    checksum = 0

    for char in data:
        checksum += ord(char)

        checksum = checksum & 0xFFFF  # truncates bits over 16
    return checksum


def create_packet(data):
    global SeqNum  # Declare SeqNum as global

    packet_data = f"{SeqNum}{data}"
    checksum = calculate_checksum(data)

     # Have some sort of placeholder like a ":" between checksum and packetdata so that when you parse it, it's easy to separate out the checcksum
    packet = f"{checksum}{packet_data}"

    SeqNum += 1
    return packet


def send_acknowledgment(clientSocket, address, port, received_packet):
    global expected_seq_num

    packet_seq_num = int(received_packet[0])
    if packet_seq_num == expected_seq_num:

        packet_checksum = str(calculate_checksum(received_packet[1:]))
        ack_packet = f"ACK{packet_checksum}"

        clientSocket.sendto(ack_packet.encode(), (address, port))
        expected_seq_num += 1

    else:
        # Optionally, you can handle out-of-order packets here

        print("Error: Out-of-order packet received")


# UDP Receiver

clientSocket = socket(AF_INET, SOCK_DGRAM)



message = "NAME Receiver"

#packet = create_packet(message)
clientSocket.sendto(message.encode(), (address, port))

clientSocket.settimeout(timeout_val)


while True:
    try:

        print("Im sending data")
        received_data, _ = clientSocket.recvfrom(1024)

        if received_data.decode().startswith("OK"):
            break

    except timeout:
        clientSocket.sendto(message.encode(), (address, port))  # Resend message



print("Name registered as Receiver")

message = "CONN Sender"

#packet = create_packet(message)
clientSocket.sendto(message.encode(), (address, port))

clientSocket.settimeout(timeout_val)

while True:

    try:
        received_data, _ = clientSocket.recvfrom(1024)

        if received_data.decode().startswith("OK"):
            break

    except timeout:
        clientSocket.sendto(message.encode(), (address, port))



print("connection established")
while True:

    received_packet, client_address = clientSocket.recvfrom(1024)
    received_data = received_packet.decode()


    packet_checksum = int(received_data[:5])
    data = received_data[5:]


    if calculate_checksum(data) == packet_checksum:
        send_acknowledgment(clientSocket, client_address[0], client_address[1], received_data)


        #A little unsure about this. This assumes that there is a "." character that the sender sends and only then are we terminating. Verify this.
        if data.strip() == ".":

            print("Received: End of transmission")
            break

        print("Received:", data)
    else:

        print("Error: Packet corrupted")


while True:
    try:

        received_data, _ = clientSocket.recvfrom(1024)

        if received_data.decode().startswith("OK"):
            break

    except timeout:
        clientSocket.sendto(packet.encode(), (address, port))  # Resend packet


clientSocket.close()