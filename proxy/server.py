# # first of all import the socket library
# import socket

# # next create a socket object
# s = socket.socket()
# print ("Socket successfully created") 

# # reserve a port on your computer in our
# # case it is 12345 but it can be anything
# port = 12345

# # Next bind to the port
# # we have not typed any ip in the ip field
# # instead we have inputted an empty string
# # this makes the server listen to requests
# # coming from other computers on the network
# s.bind(('', port))  
# print ("socket binded to %s" %(port))

# # put the socket into listening mode
# s.listen(5)
# print ("socket is listening")

# # a forever loop until we interrupt it or
# # an error occurs
# while True:

# # Establish connection with client.
#  c, addr = s.accept()
#  print ('Got connection from', addr ) 

# # send a thank you message to the client.
#  c.send('Thank you for connecting')

# # Close the connection with the client
#  c.close()

# import socket
# import sys

# HOST = "zebroid.ida.liu.se"
# PORT = 12345
# ipaddr = socket.gethostbyname(HOST)
# print(socket.gethostbyname(HOST))

import socket                    # get socket constructor and constants
import os, time, sys, signal, signal

myHost = ''                             # server machine, '' means local host

myPort = 12346                          # listen on a non-reserved port number

 
sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP socket object

sockobj.bind((myHost, myPort))               # bind it to server port number

sockobj.listen(5)                            # listen, allow 5 pending connects

 

while 1:                                     # listen until process killed

    connection, address = sockobj.accept()   # wait for next client connect

    print('Server connected by'), address     # connection is a new socket

    while 1:

        data = connection.recv(1024)         # read next line on client socket

        if not data: break                   # send a reply line to the client

        connection.send('Echo=>' + data)     # until eof when socket closed

    connection.close()