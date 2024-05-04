#!/usr/bin/python3

import socket
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)

    seq_num = 0
    message_base = "Hello, server! Message number "
# try:
#     for i in range(5):  # Send 5 messages
#         message = f"{seq_num} {message_base}{seq_num}".encode()
#         client_socket.sendto(message, server_address)
        
#         # Wait for acknowledgment
#         data, server = client_socket.recvfrom(1024)
#         print('Received:', data.decode())
        
#         if f"ACK {seq_num}" in data.decode():
#             seq_num += 1 
# # Increment sequence number only if correct ACK is received
# finally:
#     print('closing socket')
#     client_socket.close()
    while True:
            try:
                message= input("Enter a message ....")
                if  message.lower()=='exit':
                    break
                client_socket.sendto(message.encode(), server_address)
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    
if __name__== '__main__':
    main()