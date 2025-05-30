import socket
import threading

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def handle_messages():
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            if msg:
                key, value = msg.split("=", 1)
                if key == "msg":
                    print(f"[Mensagem recebida]: {value}")
        except:
            print("Erro ao receber mensagem.")
            break

def send(message):
    client.send(message.encode(FORMAT))

def send_global_message():
    message = input("Mensagem para todos: ")
    send("msg-4all=" + message)

def send_private_message():
    destination = input("Nome do destinatário: ")
    message = input("Mensagem: ")
    send("msg-" + destination + "=" + message)

def send_name():
    name = input("Digite seu nome: ")
    send("name=" + name)

def start_sending():
    send_name()
    while True:
        option = input("\nDigite:\n1 para mensagem global\n2 para mensagem privada\n> ")
        if option == "1":
            send_global_message()
        elif option == "2":
            send_private_message()
        else:
            print("Opção inválida.")

def start():
    thread1 = threading.Thread(target=handle_messages)
    thread2 = threading.Thread(target=start_sending)
    thread1.start()
    thread2.start()

start()
