import socket
import threading

HEADER = 64
PORT = 12345
SERVER = (socket.gethostbyname(socket.gethostname()))   
ADDR = (SERVER, PORT)                                   # ANVÄNDS I SERVER.BIND
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
print(socket.gethostbyname(socket.gethostname()))       #ip till vår maskin
print(socket.gethostname())                             #namet på vår maskin

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #streaming data, ipv4
server.bind(ADDR)                                   #de som ansluter till vår addr hanteras av vår socket
                                                    # TAR BARA 1 ARG DÄRFÖR ADDR
def handle_client(conn,addr):                          #lyssnar på browsern
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Text to client".encode(FORMAT)) # skickar till clienten
    conn.close()

def start():                                           #startar socketen när vi får nya conn
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}") # hur många vi har connectade


print("[STARTING] server is starting...")
start()
client.send(bytes("Heloo", FORMAT))