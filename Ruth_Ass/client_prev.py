#!/usr/bin/python3
import socket 

# This line creates a new socket object, client_socket. 
# It specifies the use of IPv4 addressing (socket.AF_INET) and a datagram-based protocol (socket.SOCK_DGRAM), 
# which is used for UDP. This line sets up the basic network communication abilities for the client.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

''' 
This line defines the server's address. Here, 
'localhost' refers to the local machine (i.e., the 
computer the script is running on), which is useful for testing. 
The number 12345 is the port number on which the server is listening.
 This line tells your client where to send the data.
'''
server_address= ('localhost', 12345)
'''
The recvfrom(1024) method is used to receive data from the socket. The number 1024 specifies the buffer size in bytes, 
indicating the maximum amount of data to be received at once. It's a parameter that can be adjusted based on the expected size of incoming messages. 
Using recvfrom allows the client to know which server (address and port) the data came from, which is critical in handling communications from multiple sources or in a networked environment.
'''
seq_num=0

'''
sequence number is sequential integer used to keep track of the messages 
'''


