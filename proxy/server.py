import socket                    # get socket constructor and constants
import os, time, sys, signal, signal

myHost = ''              # server machine, '' means local host
myPort = 12350           # listen on a non-reserved port number
clientHost = 'zebroid.ida.liu.se'          # server name, or: 'starship.python.net'
clientPort = 80                # non-reserved port used by the server

sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP socket object
sockobj.bind((myHost, myPort))               # bind it to server port number
sockobj.listen(1)                            # listen, allow 5 pending connects

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP/IP socket object
client.connect((clientHost, clientPort)) 


while 1:                                     # listen until process killed
    connection, address = sockobj.accept()   # wait for next client connect
    print('Server connected by'), address     # connection is a new socket
    while 1:
        data = connection.recv(2000)         # read next line on client socket
       # connect to serve and port

        client.sendall(data)                      # send line to server over socket
        data1 = client.recv(90000)               # receive from server: up to 1k
       # print('Client received:', data1)

        client.close()
        connection.sendall(data1)
        break
        if not data: break                   # send a reply line to the client
        #connection.send('Echo=>' + data)     # until eof when socket closed
    connection.close()
    break

