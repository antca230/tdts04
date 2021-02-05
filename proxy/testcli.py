import socket

HEADER = 64
PORT = 12345
SERVER = (socket.gethostbyname(socket.gethostname()))   
ADDR = (SERVER, PORT)                                   # ANVÄNDS I SERVER.BIND
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER -len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("HEllo world!")
send("testt")
send(DISCONNECT_MESSAGE)