import socket                    # get socket constructor and constants
import os, time, sys, signal, signal

while True:
    myHost = ''              # server machine, '' means local host
    myPort = 12357           # listen on a non-reserved port number
    clientHost = 'zebroid.ida.liu.se'          # server name, or: 'starship.python.net'
    clientPort = 80                # non-reserved port used by the server

    try:
        sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP socket object
        sockobj.bind((myHost, myPort))               # bind it to server port number
        sockobj.listen(1)                            # listen, allow 5 pending connects

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP/IP socket object
        client.connect((clientHost, clientPort))

        while 1:                                     # listen until process killed
            (connection, address) = sockobj.accept()   # wait for next client connect
            print(f"Server connected by {address}")     # connection is a new socket
            data = connection.recv(1080)
            if not data: break
            client.sendall(data)
            while 1:
                print("test4")
                data1 = client.recv(1080)
                print("test3")             # receive from server: up to 1k
                data1 = data1.replace(b"Stockholm", b"Linkoping")
        # if(len(data1) > 0):
        #     connection.send(data1)
        # else:
        #     break
                connection.send(data1)
                if not data1:
                    print("färdig hämtat")
#                    connection.close()
                    break

#        client.close()
#        connection.close()
#        sockobj.close()
#        print("utanför loopen")

    except socket.error as error_msg:
        if sockobj:
            sockobj.close()
        if connection:
            connection.close()
        if client:
            client.close()

