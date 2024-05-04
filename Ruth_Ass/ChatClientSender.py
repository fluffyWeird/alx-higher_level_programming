#from fileinput import filename

from socket import *

import sys

import zlib

# Default values
filename = None

address = None
port = None

timeout_val = 1
SeqNum = 0
# Parse command-line arguments
for i in range(1, len(sys.argv), 2):

    if sys.argv[i] == "-t" and i + 1 < len(sys.argv):
        filename = sys.argv[i + 1]

    elif sys.argv[i] == "-s" and i + 1 < len(sys.argv):
        address = sys.argv[i + 1]

    elif sys.argv[i] == "-p" and i + 1 < len(sys.argv):
        port = int(sys.argv[i + 1])
# Check if filename, address, and port are provided
if filename is None or address is None or port is None:

    print("Error: Filename, server address, and port number are required.")
    sys.exit(1)
# Check if packet is corrupt
def is_corrupt(data):

    # Extract checksum from the data
    packet_checksum = int(data[:5])

    
    # Compare extracted checksum with computed checksum

    if packet_checksum == calculate_checksum(data[5:]):
        return False

    else:
        return True

# Correct sequence number check
def correct_seq_number(data):

    # Extract sequence number from data
    seq_no = int(data[0])

    
    # Compare extracted sequence number with expected sequence number

    if seq_no == SeqNum:

        return True
    else:

        return False


# Define packet

def calculate_checksum(data):
    checksum = 0

    for char in data:
        checksum += ord(char)

        checksum = checksum & 0xFFFF  # truncates bits over 16

    return checksum

#def fetch_checksum(data):

    return str(zlib.crc32(data))


def create_packet(data):
    global SeqNum  # Declare SeqNum as global

    packet_data = f"{SeqNum}:{data}"  # Add a delimiter between checksum and packet data
    checksum = calculate_checksum(packet_data)  # Calculate checksum over entire packet data

    packet = f"{checksum}:{packet_data}"
    SeqNum += 1

    return packet



def send_packet_and_wait_for_ack(packet, address, port, timeout_val):
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    clientSocket.sendto(packet.encode(), (address, port))
    clientSocket.settimeout(timeout_val)

    while True:
        try:

            received_data, _ = clientSocket.recvfrom(1024)
            packet_checksum = str(calculate_checksum(packet))

            if received_data.decode() == f"ACK{packet_checksum}":
                clientSocket.close()

                return True
            break  # Break loop after receiving ACK

        except timeout:
            clientSocket.sendto(packet.encode(), (address, port))  # Resend packet

            #break  # Break loop after resending
            continue  # Continue loop after resending

    clientSocket.close()
    return False


# UDP Sender
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(timeout_val)  # Set timeout before sending the packet
message = "NAME Sender"

try:
    clientSocket.sendto(message.encode(), (address, port))

except timeout:
    # Handle timeout if necessary

    print("Timeout occurred while sending the packet.")

while True:

    try:
        print("sending data from sender")

        received_data, _ = clientSocket.recvfrom(1024)

        if received_data.decode().startswith("OK"):
            break

    except timeout:
        clientSocket.sendto(message.encode(), (address, port))  # Resend message


print("Name registered as Sender")
message = "CONN Receiver"

#packet = create_packet(message)

clientSocket.sendto(message.encode(), (address, port))
clientSocket.settimeout(timeout_val)


while True:
    try:

        received_data, _ = clientSocket.recvfrom(1024)

        if received_data.decode().startswith("OK"):
            break

    except timeout:
        clientSocket.sendto(message.encode(), (address, port))  # Resend packet


print("connection established")

#Step 3 - Sending out file data to the receiver


# Step 3.1 - Sending out file name to the receiver
message = create_packet(filename)

clientSocket.sendto(message, (address, port))
clientSocket.settimeout(timeout_val)

while True:
    try:

        received_data, _ =

clientSocket.recvfrom(1024)
        if not(is_corrupt(received_data)) and correct_seq_number(received_data):

            SeqNum += 1 
            break

    except timeout:
        clientSocket.sendto(message.encode(), (address, port))




# step 3.2 - Sending out the actual file contents to the receiver
# Step 3.2 - Sending out the actual file contents to the receiver

with open(filename, 'rb') as file:
    while True:

        data_chunk = file.read(1024)  # Read 1024 bytes from the file
        if not data_chunk:  # If no more data to read, break the loop

            break
        packet = create_packet(data_chunk)  # Create a packet containing the data chunk

        clientSocket.sendto(packet, (address, port))  # Send the packet over the socket
        clientSocket.settimeout(timeout_val)  # Set timeout for receiving ACK

        while True:
            try:

                received_data, _ = clientSocket.recvfrom(1024)
                if received_data.decode().startswith("ACK"):  # Check if ACK received

                    break  # Exit loop if ACK received
            except timeout:

                clientSocket.sendto(packet, (address, port))  # Resend packet on timeout

clientSocket.close()