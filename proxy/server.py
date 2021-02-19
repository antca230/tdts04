import socket                    # get socket constructor and constants
import os, time, sys, signal, signal, logging

def getURL(data):
    first_line = data.split(b'\n')[0]
    url = first_line.split(b' ')[1]

    http_pos = url.find(b"://") # find pos of ://
    if (http_pos==-1):
        temp = url
    else:
        temp = url[(http_pos+3):] # get the rest of url
    port_pos = temp.find(b":") # find the port pos (if any)
    # find end of web server
    webserver_pos = temp.find(b"/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
    webserver = ""
    port = -1
    if (port_pos==-1 or webserver_pos < port_pos): 
        # default port 
        port = 80 
        webserver = temp[:webserver_pos] 
    else: # specific port 
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]
    webserver[1:]
    return webserver

while True:
    myHost = ''              # server machine, '' means local host
    myPort = 12358           # listen on a non-reserved port number
    clientHost = 'zebroid.ida.liu.se'          # server name, or: 'starship.python.net'
    clientPort = 80                # non-reserved port used by the server
    try:
        sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP socket object
        sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sockobj.bind((myHost, myPort))               # bind it to server port number
        sockobj.listen()                            # listen, allow 5 pending connects
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # make a TCP/IP socket object
        (connection, address) = sockobj.accept()

        while True:                                     # listen until process killed
            print(f"Server connected by {address}")     # connection is a new socket
            request = connection.recv(1080)
            if not request: break
            clientHost = getURL(request)
            client.connect((clientHost, clientPort))
            client.sendall(request)
            while True:
                response = client.recv(1080) # receive from server: up to 1k      
                response = response.replace(b"Stockholm", "Linköping".encode('utf-8'))
                response = response.replace(b"/smiley.jpg", b"/trolly.jpg")
                response = response.replace(b"Smiley", b"Trolly")
                response = response.replace("/Linköping-spring.jpg".encode('utf-8'), b"/Stockholm-spring.jpg")
                if not response:
                    print("färdig hämtat")
                    break
                connection.send(response)         
    except socket.error as error_msg:
        if sockobj:
            sockobj.close()
        if connection:
            connection.close()
        if client:
            client.close()

