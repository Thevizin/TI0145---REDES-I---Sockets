import socket
import threading
import time

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connections = []
messagesGlobal = []
messagesPriv = []

def search_name_connections(name):
    global connections
    for conn in connections:
        if conn["name"] == name:
            return conn
    return None

def view_global_historic(connection_client):
    global messagesGlobal
    conn = connection_client["conn"]
    for i in range(len(messagesGlobal)):
        try:
            conn.send(f"msg={messagesGlobal[i]}".encode(FORMAT))
            time.sleep(0.2)
        except:
            print("Erro ao enviar histórico de mensagens globais.")

def send_message_to_user(conn_sending, connection_client, priv):
    global messagesGlobal
    global messagesPriv
    conn = connection_client["conn"]
    name_dest = connection_client["name"]
    if(conn_sending != 0):
        name_from = conn_sending["name"]
    print(f"[Servidor] Enviando mensagens para {connection_client['addr']}")

    if priv:
        messages_for_client = [msg for msg in messagesPriv if f"{name_from} -> {name_dest}:" in msg]
        if messages_for_client:
            ultima_msg = messages_for_client[-1]
            try:
                conn.send(f"msg={ultima_msg}".encode(FORMAT))
                time.sleep(0.2)
            except:
                print("Erro ao enviar mensagem privada.")
    else:
        if messagesGlobal:
            try:
                conn.send(f"msg={messagesGlobal[-1]}".encode(FORMAT))
                time.sleep(0.2)
            except:
                print("Erro ao enviar mensagem global.")

def send_message_4all(conn_usr):
    global connections
    for conn in connections:
        if conn["conn"] != conn_usr["conn"]: 
            send_message_to_user(0, conn, priv=False)


# Vamos definir o seguinte padrão para a conexão:
# Caso o cliente se conecte pela primeira vez, ele informará:
# name=nomedocliente
# Em seguida, informará, com outra mensagem, a sua mensagem:
# msg-4all=mensagemdocliente   ou... msg-nomedodestinatario=mensagemdoclient
# Dessa forma, o formato será: name=nomedocliente
# Ou, poderá ser: msg=mensagemdocliente


def handle_clients(conn, addr):
    print(f"[Conexão] Novo usuário conectado: {addr}")
    global connections
    global messagesPriv
    global messagesGlobal

    nome = False
    conn_usr = None

    while True:
        try:
            message = conn.recv(2048).decode(FORMAT)
            if message:
                if message.startswith("name="):
                    name = message.split("=")[1]
                    conn_usr = {"conn": conn, "addr": addr, "name": name, "last": 0}
                    connections.append(conn_usr)
                    view_global_historic(conn_usr)

                elif message.startswith("msg-"):
                    msg_part = message.split("-", 1)[1]
                    if msg_part.startswith("4all="):
                        message_text = msg_part.split("=", 1)[1]
                        messagesGlobal.append(f"{conn_usr['name']}: {message_text}")
                        send_message_4all(conn_usr)
                    else:
                        destination_name, message_text = msg_part.split("=", 1)
                        messagesPriv.append(f"{conn_usr['name']} -> {destination_name}: {message_text}")
                        conn_dest = search_name_connections(destination_name)
                        if conn_dest:
                            send_message_to_user(conn_usr, conn_dest, priv=True)
                        else:
                            print(f"[Aviso] Usuário '{destination_name}' não encontrado.")
        except:
            print(f"[Desconexão] {addr} desconectou.")
            break

def start():
    print("[Servidor] Iniciando socket...")
    server.listen()
    print(f"[Servidor] Ouvindo em {SERVER_IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
        print(f"[Conexões ativas] {threading.active_count() - 1}")

start()
