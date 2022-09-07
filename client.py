from email import message
from os import name
import socket
from sqlite3 import connect
import threading


def send_message(client, name):
    connected = True
    while connected:
        data = input()
        if data == "DISCONNECT":
            data = "left-the-meeting."
            connected = False
        message = f'{name} : {data}'
        client.send(message.encode())

    client.close()


def receive_message(client):
    connected = True
    while connected:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            client.close()
            connected = False

    client.close()


if __name__ == '__main__':
    PORT = 9999
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    name = input("Your name: ")
    client.send(name.encode())

    print(f'{name}, Welcome to the server! and to leave type DISCONNECT and then enter.')

    t1 = threading.Thread(target=send_message, args=(client, name))
    t1.start()

    t2 = threading.Thread(target=receive_message, args=(client, ))
    t2.start()
