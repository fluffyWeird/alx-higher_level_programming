#!/usr/bin/python3 
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))

expected_seq_num = 0

while True:
    data, addr = server_socket.recvfrom(1024)
    # received_seq_num = int(data.decode().split()[0])
    # print(f"Received message: {data}, Sequence Number: {received_seq_num}")
    print(f"{data.decode()}")
    # if received_seq_num == expected_seq_num:
    #     ack_message = f"ACK {received_seq_num}".encode()
    #     expected_seq_num += 1
    # else:
    #     ack_message = f"ACK {expected_seq_num - 1}".encode()
    
    # server_socket.sendto(ack_message, addr)
