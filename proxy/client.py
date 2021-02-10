import sys
import socket             # portable socket interface plus constants

serverHost = ''          # server name, or: 'starship.python.net'
serverPort = 12346                # non-reserved port used by the server

message = ['Hello network world']           # text to send to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP/IP socket object
client.connect((serverHost, serverPort))   # connect to serve and port

for line in message:
    client.send(line)                      # send line to server over socket
    data = client.recv(1024)               # receive from server: up to 1k
    print('Client received:', 'data')

client.close()