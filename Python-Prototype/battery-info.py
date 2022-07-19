
import socket


HOST = "127.0.0.1"
PORT = 8423

command = input("WHAT DO YOU WANT DA COMMAND TO SAY?")
command = bytes(command, 'utf-8')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(command)
    data = s.recv(1024)

data = data.decode('utf-8')
print(data)
