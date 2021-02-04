import socket
import threading

HEADER = 64
PORT = 5050
SERVER = (socket.gethostbyname(socket.gethostname()))   
#ADDR = (SERVER, PORT)                                   # ANVÄNDS I SERVER.BIND
print(socket.gethostbyname(socket.gethostname()))       #ip till vår maskin
print(socket.gethostname())                             #namet på vår maskin

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #streaming data, ipv4
server.bind(SERVER,PORT)                                   #de som ansluter till vår addr hanteras av vår socket

def handle_client(conn,addr):                          #lyssnar på browsern
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while True
        msg = conn.recv()



def start():                                           #startar socketen när vi får nya conn
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}") # hur många vi har connectade

print("[STARTING] server is starting...")
start()