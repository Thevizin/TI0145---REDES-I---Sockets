#client.py

import socket
import threading
import base64
import os
import json
import sys
import platform
import time

def discover_server(timeout=5):
    """
    Descobre automaticamente o servidor de chat na rede local
    - Envia broadcast UDP na porta 5051 com mensagem "CHAT_DISCOVER"
    - Aguarda resposta "CHAT_SERVER" do servidor
    - Retorna o IP do servidor encontrado ou None
    """
    print("🔍 Procurando servidor na rede local...")
    
    # Criar socket UDP para broadcast
    discover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discover_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discover_socket.settimeout(timeout)
    
    try:
        # Enviar mensagem de descoberta
        discover_socket.sendto(b"CHAT_DISCOVER", ('<broadcast>', 5051))
        
        # Aguardar resposta do servidor
        data, addr = discover_socket.recvfrom(1024)
        if data == b"CHAT_SERVER":
            server_ip = addr[0]
            print(f"✅ Servidor encontrado: {server_ip}")
            return server_ip
    except socket.timeout:
        print("❌ Nenhum servidor encontrado automaticamente.")
    except Exception as e:
        print(f"❌ Erro na descoberta: {e}")
    finally:
        discover_socket.close()
    
    return None

SERVER_IP = discover_server() # Descobre servidor automaticamente
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Controles de estado para evitar conflitos de entrada
input_lock = threading.Lock() # Mutex para input thread-safe
waiting_for_file_decision = False # Flag para processar arquivo pendente
pending_file_data = None # Dados do arquivo aguardando decisao
name_registered = False  # Controle para saber se o nome foi aceito
waiting_for_name = False  # Controle para reenvio de nome

def safe_input(prompt):
    """
    Input thread-safe que respeita o mutex
    Evita conflitos quando multiplas threads tentam capturar entrada
    """
    with input_lock:
        return input(prompt)

def display_online_users(users_data):
    """
    Exibe a lista de usuarios online de forma formatada
    Recebe dados JSON do servidor e apresenta em tabela organizada
    """
    try:
        users = json.loads(users_data)
        print("\n" + "="*50)
        print("👥 USUÁRIOS ONLINE (OUTROS USUÁRIOS)")
        print("="*50)
        
        if not users:
            print("❌ Nenhum outro usuário online no momento.")
        else:
            print(f"📊 Total de outros usuários online: {len(users)}")
            print("-"*50)
            
            for i, user in enumerate(users, 1):
                name = user.get('name', 'Desconhecido')
                addr = user.get('addr', 'N/A')
                print(f"{i:2d}. 👤 {name:<20} | 🌐 {addr}")
        
        print("="*50)
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao processar lista de usuários: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao exibir usuários: {e}")

def handle_messages():
    """
    Thread dedicada para receber e processar mensagens do servidor
    Roda continuamente em background processando:
    - msg: mensagens de texto
    - online_users: lista de usuarios online
    - file: arquivos recebidos
    """
    global waiting_for_file_decision, pending_file_data, name_registered, waiting_for_name
    
    while True:
        try:
            msg = client.recv(2048 * 10).decode(FORMAT) # Buffer grande para arquivos
            if msg:
                key, value = msg.split("=", 1) # Separar tipo da mensagem do conteudo
                
                if key == "msg":
                    # Verificar se e mensagem do servidor sobre nome duplicado
                    if "[Servidor]:" in value and "já está sendo usado" in value:
                        waiting_for_name = True
                        name_registered = False
                        print(f"\n💬 {value}")
                    elif "[Servidor]:" in value and "Bem-vindo ao chat" in value:
                        name_registered = True
                        waiting_for_name = False
                        print(f"\n💬 {value}")
                    elif "[Servidor]:" in value and "Digite um novo nome:" in value:
                        print(f"\n💬 {value}")
                        # Nao fazer nada aqui, deixar o loop principal tratar
                    else:
                        print(f"\n💬 {value}")
                    
                elif key == "online_users":
                    # Trata a resposta da lista de usuários online
                    display_online_users(value)
                    
                elif key == "file":
                    # Formato: remetente||nome_arquivo||dados_base64
                    parts = value.split("||", 2)
                    if len(parts) == 3:
                        sender, filename, b64data = parts
                        file_size = (len(b64data) * 3) // 4  # Tamanho aproximado em bytes
                        
                        # Armazenar dados do arquivo pendente
                        pending_file_data = {
                            'sender': sender,
                            'filename': filename,
                            'b64data': b64data,
                            'file_size': file_size
                        }
                        
                        # Marcar que estamos aguardando decisao sobre arquivo
                        waiting_for_file_decision = True
                        
                        print(f"\n" + "="*50)
                        print(f"📎 ARQUIVO RECEBIDO")
                        print(f"👤 De: {sender}")
                        print(f"📄 Arquivo: {filename}")
                        print(f"📊 Tamanho: {file_size/1024:.1f}KB")
                        print("="*50)
                        print("O que deseja fazer?")
                        print("1. 💾 Baixar arquivo")
                        print("2. ❌ Ignorar")
                        print("-"*30)
                        
                        # Nao capturar input aqui - sera tratado no menu principal
                        
                    else:
                        # Compatibilidade com formato antigo
                        try:
                            filename, b64data = value.split("||", 1)
                            print(f"\n📎 [Arquivo recebido - formato antigo]: {filename}")
                            with open("recebido_" + filename, "wb") as f:
                                f.write(base64.b64decode(b64data))
                            print(f"✅ Salvo como: recebido_{filename}")
                        except:
                            print("❌ Erro ao processar arquivo (formato incompatível)")
                            
        except Exception as e:
            print(f"❌ Erro ao receber mensagem: {e}")
            break

def process_pending_file():
    """
    Processa arquivo pendente quando chamado do menu principal
    Permite ao usuario escolher entre baixar ou ignorar o arquivo
    """
    global waiting_for_file_decision, pending_file_data
    
    if not waiting_for_file_decision or not pending_file_data:
        return
    
    data = pending_file_data
    
    while True:
        try:
            choice = safe_input("Escolha (1-2): ").strip()
            if choice in ['1', '2']:
                break
            print("❌ Digite apenas 1 ou 2")
        except KeyboardInterrupt:
            choice = '2'
            break
    
    if choice == "1":
        try:
            # Criar diretorio downloads se nao existir
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
                print("📁 Diretório 'downloads' criado")
            
            # Evitar sobrescrever arquivos
            base_name = os.path.splitext(data['filename'])[0]
            extension = os.path.splitext(data['filename'])[1]
            counter = 1
            new_filename = data['filename']
            
            while os.path.exists(os.path.join("downloads", new_filename)):
                new_filename = f"{base_name}_{counter}{extension}"
                counter += 1
            
            filepath = os.path.join("downloads", new_filename)
            
            print("⏳ Baixando arquivo...")
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(data['b64data']))
            
            actual_size = os.path.getsize(filepath)
            print(f"✅ Arquivo baixado com sucesso!")
            print(f"📁 Local: {filepath}")
            print(f"📊 Tamanho: {actual_size/1024:.1f}KB")
            
        except Exception as e:
            print(f"❌ Erro ao baixar arquivo: {e}")
    else:
        print("📎 Arquivo ignorado.")
    
    print("="*50)
    
    # Limpar estado
    waiting_for_file_decision = False
    pending_file_data = None

def send(message):
    """
    Envia mensagem JSON para o servidor
    Converte dicionario Python para JSON e envia via socket
    """
    try:
        client.send(json.dumps(message).encode(FORMAT))
    except Exception as e:
        print(f"Erro ao enviar: {e}")

def send_global_message():
    """
    Captura e envia mensagem global (para todos os usuarios)
    Pode ser texto ou arquivo dependendo da escolha do usuario
    """
    message, is_text, filename = capture_message()
    if message is None:
        return
    if is_text:
        message_formatted = {"type": "msg", "control": "4all", "message": message}
    else:
        message_formatted = {"type": "file", "control": "4all", "message": message, "filename": filename}
    send(message_formatted)

def send_private_message():
    """
    Captura e envia mensagem privada para usuario especifico
    Solicita nome do destinatario e pode ser texto ou arquivo
    """
    destination = safe_input("Nome do destinatário: ")
    message, is_text, filename = capture_message()
    if message is None:
        return
    if is_text:
        message_formatted = {"type": "msg", "control": destination, "message": message}
    else:
        message_formatted = {"type": "file", "control": destination, "message": message, "filename": filename}
    send(message_formatted)

def send_name():
    """
    Funcao melhorada para lidar com nomes duplicados
    Continua solicitando novo nome ate que seja aceito pelo servidor
    """
    global name_registered, waiting_for_name
    
    while not name_registered:
        if waiting_for_name:
            name = safe_input("Digite um novo nome: ")
        else:
            name = safe_input("Digite seu nome: ")
        
        message_formatted = {"type": "name", "control": "dontcare", "message": name}
        send(message_formatted)
        
        # Aguardar resposta do servidor por um tempo
        time.sleep(1)
        
        # Se ainda não foi registrado e não está esperando novo nome, houve erro
        if not name_registered and not waiting_for_name:
            print("❌ Erro de conexão. Tentando novamente...")
            continue

def receive_online_users():
    """
    Solicita a lista de usuarios online do servidor
    Envia requisicao especial que sera processada pelo servidor
    """
    if not name_registered:
        print("❌ Você precisa definir um nome primeiro!")
        return
        
    print("⏳ Buscando usuários online...")
    message_formatted = {"type": "online_usr", "control": "dontcare", "message": "dontcare"}
    send(message_formatted)
    # A resposta será tratada automaticamente pela função handle_messages()
    time.sleep(0.5)  # Pequena pausa para dar tempo da resposta chegar

def select_file():
    """
    Selecao de arquivo usando interface grafica Tkinter
    Abre dialog para usuario escolher arquivo do sistema
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Criar janela principal invisivel
        root = tk.Tk()
        root.withdraw()  # Esconder janela principal
        root.wm_attributes('-topmost', 1)  # Colocar na frente
        
        # Forcar foco
        if platform.system() == "Windows":
            root.wm_attributes('-alpha', 0.0)  # Transparente no Windows
        
        # Abrir dialog
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo para enviar",
            filetypes=[
                ("Todos os arquivos", "*.*"),
                ("Documentos de texto", "*.txt *.doc *.docx *.pdf"),
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Arquivos de código", "*.py *.js *.html *.css *.json")
            ]
        )
        
        # Destruir janela
        root.destroy()
        
        return filepath if filepath else None
        
    except Exception as e:
        print(f"❌ Erro ao abrir seletor de arquivos: {e}")
        return None

def capture_message():
    """
    Captura mensagem do usuario (texto ou arquivo)
    Apresenta menu para escolher tipo de mensagem
    Para texto: captura entrada do teclado
    Para arquivo: abre seletor de arquivo e codifica em base64
    
    Returns:
        tuple: (conteudo, is_text, filename)
        - conteudo: texto da mensagem ou dados base64 do arquivo
        - is_text: True para texto, False para arquivo
        - filename: nome do arquivo (None para texto)
    """
    print("\nTipo de mensagem:")
    print("1. 💬 Texto")
    print("2. 📎 Arquivo")
    
    # Loop ate escolha valida
    while True:
        control = safe_input("Escolha (1-2): ").strip()
        if control in ['1', '2']:
            break
        print("❌ Digite apenas 1 ou 2")
    
    if control == "1":
        # Capturar mensagem de texto
        message = safe_input("\n✏️  Digite sua mensagem: ")
        return message, True, None
        
    elif control == "2":
        # Capturar arquivo
        print("\n📎 ENVIO DE ARQUIVO")
        path = select_file()
        # Verificar se arquivo foi selecionado e existe
        if not path or not os.path.isfile(path):
            print("❌ Arquivo não encontrado ou seleção cancelada.")
            return None, False, None
            
        # Verificar tamanho do arquivo 
        size = os.path.getsize(path)
        if size > 10 * 1024 * 1024:  # 10MB
            print(f"⚠️  Arquivo muito grande ({size/1024/1024:.1f}MB). Máximo recomendado: 10MB")
            if safe_input("Continuar mesmo assim? (s/n): ").lower() != 's':
                return None, False, None
        
        # Extrair nome do arquivo
        filename = os.path.basename(path)
        print(f"\n📤 Preparando envio...")
        print(f"📄 Arquivo: {filename}")
        print(f"📊 Tamanho: {size/1024:.1f}KB")
        
        try:
            # Codificar arquivo em base64
            print("⏳ Codificando arquivo...")
            with open(path, "rb") as file:
                data = base64.b64encode(file.read()).decode(FORMAT)
            print("✅ Arquivo pronto para envio!")
            return data, False, filename
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
            return None, False, None

def start_sending():
    """
    Funcao principal do cliente - gerencia todo o fluxo de interacao
    1. Solicita nome do usuario
    2. Aguarda confirmacao do servidor
    3. Apresenta menu principal com opcoes
    4. Processa arquivos pendentes quando necessario
    """
    global waiting_for_file_decision, name_registered
    
    print("\n🎉 Bem-vindo ao Chat!")
    send_name()
    
    # Aguardar confirmacao do nome pelo servidor
    while not name_registered:
        time.sleep(0.1)
    
    print("\n" + "="*50)
    print("📋 MENU PRINCIPAL")
    print("="*50)
    
    # Loop principal do menu
    while True:
        # Verificar se ha arquivo pendente para processar
        if waiting_for_file_decision:
            print("\n⚠️  Você tem um arquivo pendente para processar!")
            process_pending_file()
            continue
        
        # Apresentar opcoes do menu
        print("\nEscolha uma opção:")
        print("1. 🌐 Mensagem global (todos)")
        print("2. 🔒 Mensagem privada")
        print("3. 👥 Listar usuários online")
        print("4. ❌ Sair")
        print("-"*30)
        
        option = safe_input("Escolha (1-4): ").strip()
        
        # Processar opcao selecionada
        if option == "1":
            print("\n📢 MENSAGEM GLOBAL")
            send_global_message()
        elif option == "2":
            print("\n🔒 MENSAGEM PRIVADA")
            send_private_message()
        elif option == "3":
            print("\n👥 USUÁRIOS ONLINE")
            receive_online_users()
        elif option == "4":
            print("\n👋 Saindo do chat...")
            break
        else:
            print("❌ Opção inválida! Digite apenas 1, 2, 3 ou 4.")

def start():
    """
    Inicia o cliente de chat
    Cria thread separada para receber mensagens e inicia interface de usuario
    """
    # Criar thread daemon para receber mensagens em background
    thread1 = threading.Thread(target=handle_messages, daemon=True)
    thread1.start()
    # Iniciar interface de usuario no thread principal
    start_sending()

# Ponto de entrada do programa
if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\n👋 Cliente desconectado.")
    except Exception as e:
        print(f"❌ Erro no cliente: {e}")
    finally:
        # Garantir fechamento do socket
        try:
            client.close()
        except:
            pass