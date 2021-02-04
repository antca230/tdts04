# import socket

# # Create a socket object
# s = socket.socket()

# # Define the port on which you want to connect
# port = 12345

# # connect to the server on local computer
# s.connect(('127.0.0.1', port))

# # receive data from the server
# print (s.recv(1024) ) 
# # close the connection
# s.close()

# import socket

# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 12345        # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))

import sys

import socket             # portable socket interface plus constants

serverHost = ''          # server name, or: 'starship.python.net'

serverPort = 12346                # non-reserved port used by the server

 

message = ['Hello network world']           # text to send to server

sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP/IP socket object

sockobj.connect((serverHost, serverPort))   # connect to serve and port

 

for line in message:

    sockobj.send(line)                      # send line to server over socket

    data = sockobj.recv(1024)               # receive from server: up to 1k

    print('Client received:', 'data')

 

sockobj.close()