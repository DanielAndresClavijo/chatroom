from email import message
import socket
import threading

clients = {}  # {conn (a socket object) : "name of user"}


def handle_client(conn, addr, user):
    message = f'{user} has joined the chat server.'
    for client in clients:
        if clients[client] != user:
            client.send(message.encode())

    disconnect = None
    connected = True
    while connected:
        try:
            message = conn.recv(1024)
            data = message.decode('utf-8').split()
            # print("this data")
            # print(data)
            name = data[0]

            typo = data[2]  # message : name : --- => data[2] = ------

            if typo == "left-the-meeting.":
                disconnect = conn
                connected = False

            for client in clients:
                if clients[client] != name:
                    client.send(message)
        except Exception as e:
            print(e)
            connected = False
            conn.close()

    try:
        clients.pop(disconnect)
    except:
        pass

    conn.close()


def start(server):
    server.listen(2)

    print('[SERVER STARTED]')

    while True:
        conn, addr = server.accept()

        user = conn.recv(1024).decode('utf-8')
        clients[conn] = user

        thread = threading.Thread(
            target=handle_client, args=(conn, addr, user))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount()-1}')


if __name__ == '__main__':
    PORT = 9999
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print('[SERVER INITIALIZED]')

    start(server)
