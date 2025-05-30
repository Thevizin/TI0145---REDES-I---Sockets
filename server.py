#server.py

import socket
import threading
import time
import json


SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connections = []
global_messages = []
private_messages = []

def search_name_in_connections(name):
    for conn in connections:
        if conn["name"] == name:
            return conn
    return None

def view_global_history(client_connection):
    conn = client_connection["conn"]
    for msg in global_messages:
        try:
            if msg["type"] == "msg":
                message = f"[{msg['sender']} -> todos]: {msg['content']}"
                conn.send(f"msg={message}".encode(FORMAT))
            elif msg["type"] == "file":
                filename = msg.get("filename", "arquivo_recebido")
                data = msg["content"]
                sender = msg["sender"]
                # New format: sender||filename||data
                conn.send(f"file={sender}||{filename}||{data}".encode(FORMAT))
            time.sleep(0.2)
        except Exception as e:
            print(f"Erro ao enviar histórico para {client_connection['name']}: {e}")

def send_online_users_list(client_connection):
    """Envia a lista de usuários online para o cliente solicitante"""
    conn = client_connection["conn"]
    try:
        online_users = []
        for connection in connections:
            user_info = {
                "name": connection["name"],
                "addr": f"{connection['addr'][0]}:{connection['addr'][1]}"
            }
            online_users.append(user_info)
        
        # Envia a lista como JSON
        users_data = json.dumps(online_users)
        conn.send(f"online_users={users_data}".encode(FORMAT))
        print(f"[Lista de Usuários] Enviada para {client_connection['name']} - {len(online_users)} usuários online")
        
    except Exception as e:
        print(f"Erro ao enviar lista de usuários para {client_connection['name']}: {e}")

def send_message_to_user(sending_conn, client_connection, is_private):
    conn = client_connection["conn"]
    dest_name = client_connection["name"]
    from_name = sending_conn["name"] if sending_conn != 0 else "Servidor"

    messages_source = private_messages if is_private else global_messages
    
    if is_private:
        # For private messages, filter only messages for this user
        messages_for_client = [
            msg for msg in messages_source
            if (msg["sender"] == from_name and msg["destination"] == dest_name)
        ]
    else:
        # For global messages, get all
        messages_for_client = messages_source

    if messages_for_client:
        last_msg = messages_for_client[-1]
        try:
            if last_msg["type"] == "msg":
                if is_private:
                    message = f"[{last_msg['sender']} -> {last_msg['destination']}]: {last_msg['content']}"
                else:
                    message = f"[{last_msg['sender']} -> todos]: {last_msg['content']}"
                conn.send(f"msg={message}".encode(FORMAT))
            elif last_msg["type"] == "file":
                filename = last_msg.get("filename", "arquivo_recebido")
                data = last_msg["content"]
                sender = last_msg["sender"]
                # New format: sender||filename||data
                conn.send(f"file={sender}||{filename}||{data}".encode(FORMAT))
        except Exception as e:
            print(f"Erro ao enviar mensagem para {dest_name}: {e}")

def send_message_to_all(user_conn):
    for conn in connections:
        if conn["conn"] != user_conn["conn"]:
            send_message_to_user(user_conn, conn, is_private=False)

def handle_clients(conn, addr):
    print(f"[Conexão] Novo usuário conectado: {addr}")
    global connections

    user_conn = None

    while True:
        try:
            data = conn.recv(2048 * 10)
            if not data:
                break

            message = json.loads(data.decode(FORMAT))

            if message["type"] == "name":
                name = message["message"]
                user_conn = {"conn": conn, "addr": addr, "name": name}
                connections.append(user_conn)
                print(f"[Nome definido] {name} conectado de {addr}")
                view_global_history(user_conn)

            elif message["type"] == "online_usr":
                # Envia a lista de usuários online
                send_online_users_list(user_conn)

            elif message["type"] == "msg":
                if message["control"] == "4all":
                    new_message = {
                        "sender": user_conn["name"],
                        "destination": "all",
                        "type": "msg",
                        "content": message["message"]
                    }
                    global_messages.append(new_message)
                    print(f"[Mensagem Global] {user_conn['name']}: {message['message'][:50]}...")
                    send_message_to_all(user_conn)
                else:
                    destination = message["control"]
                    new_message = {
                        "sender": user_conn["name"],
                        "destination": destination,
                        "type": "msg",
                        "content": message["message"]
                    }
                    private_messages.append(new_message)
                    print(f"[Mensagem Privada] {user_conn['name']} -> {destination}: {message['message'][:50]}...")
                    dest_conn = search_name_in_connections(destination)
                    if dest_conn:
                        send_message_to_user(user_conn, dest_conn, is_private=True)
                    else:
                        # Send error message to sender
                        error_msg = f"❌ Usuário '{destination}' não encontrado ou offline."
                        conn.send(f"msg=[Servidor]: {error_msg}".encode(FORMAT))

            elif message["type"] == "file":
                destination = message["control"]
                filename = message.get("filename", "arquivo_recebido")
                file_data = message["message"]
                
                # Check file size (in Base64)
                file_size_b64 = len(file_data)
                file_size_bytes = (file_size_b64 * 3) // 4  # Approximation of real size
                
                print(f"[Arquivo] {user_conn['name']} enviando '{filename}' ({file_size_bytes/1024:.1f}KB)")
                
                new_message = {
                    "sender": user_conn["name"],
                    "destination": destination,
                    "type": "file",
                    "content": file_data,
                    "filename": filename
                }
                
                if destination == "4all":
                    global_messages.append(new_message)
                    print(f"[Arquivo Global] {user_conn['name']}: {filename}")
                    send_message_to_all(user_conn)
                else:
                    private_messages.append(new_message)
                    print(f"[Arquivo Privado] {user_conn['name']} -> {destination}: {filename}")
                    dest_conn = search_name_in_connections(destination)
                    if dest_conn:
                        send_message_to_user(user_conn, dest_conn, is_private=True)
                    else:
                        # Send error message to sender
                        error_msg = f"❌ Usuário '{destination}' não encontrado. Arquivo '{filename}' não foi entregue."
                        conn.send(f"msg=[Servidor]: {error_msg}".encode(FORMAT))

        except json.JSONDecodeError as e:
            print(f"[Erro JSON] Conexão {addr}: {e}")
            break
        except Exception as e:
            print(f"[Erro] Conexão com {addr} encerrada. Motivo: {e}")
            break

    # Clean up connection
    if user_conn:
        connections.remove(user_conn)
        print(f"[Desconexão] {user_conn['name']} ({addr}) desconectado")
        print(f"[Conexões ativas]: {len(connections)}")
    conn.close()

def start():
    print("[Servidor] Iniciando...")
    server.listen()
    print(f"[Servidor] Ouvindo em {SERVER_IP}:{PORT}")
    print(f"[Servidor] Pronto para receber conexões!")
    
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_clients, args=(conn, addr))
            thread.start()
            print(f"[Conexões ativas]: {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("\n[Servidor] Encerrando servidor...")
            break
        except Exception as e:
            print(f"[Erro do Servidor]: {e}")

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\n[Servidor] Servidor encerrado pelo usuário.")
    finally:
        try:
            server.close()
        except:
            pass