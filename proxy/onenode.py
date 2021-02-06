import socket
import signal
import sys
import threading


class server:
    def init(self, config):
        signal.signal(signal.SIGINT, self.shutdown)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))
        self.serverSocket.listen(10)
        self.__clients = {}

def listenforclients(self):
    while True:
        (clientSocket, client_address) = self.serverSocket.accept()
        d = threading.Thread(name=self._getClientName(client_address),
                         target=self.proxy_thread, args=(clientSocket, client_address))
        d.setDaemon(True)
        d.start()
    self.shutdown(0,0)

def proxy_thread(self,conn,client_address):
    # get the request from browser
    request = conn.recv(config['MAX_REQUEST_LEN']) 

    # parse the first line
    first_line = request.split('\n')[0]

    # get url
    url = first_line.split(' ')[1]