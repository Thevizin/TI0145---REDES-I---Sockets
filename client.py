#client.py

import socket
import threading
import base64
import os
import json
import sys
import platform
import time
from diffie_Hellman_utils import generate_keys, compute_shared_secret


SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

<<<<<<< Updated upstream
# State control to avoid input conflicts
input_lock = threading.Lock()
waiting_for_file_decision = False
pending_file_data = None
name_registered = False  # CORREÇÃO: Controle para saber se o nome foi aceito
waiting_for_name = False  # CORREÇÃO: Controle para reenvio de nome

private_key, public_key = generate_keys()
shared_secret = None
=======
# Controles de estado para evitar conflitos de entrada
input_lock = threading.Lock() # Mutex para input thread-safe
name_registered = False  # Controle para saber se o nome foi aceito
waiting_for_name = False  # Controle para reenvio de nome
>>>>>>> Stashed changes

# Sistema de Caixa Postal
mailbox = []  # Lista de arquivos recebidos
mailbox_lock = threading.Lock()  # Mutex para acesso thread-safe à caixa postal

def safe_input(prompt):
    """Thread-safe input that respects the lock"""
    with input_lock:
        return input(prompt)

def display_online_users(users_data):
    """Exibe a lista de usuários online de forma formatada"""
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

def add_to_mailbox(sender, filename, b64data, file_size):
    """
    Adiciona um arquivo à caixa postal
    """
    with mailbox_lock:
        file_entry = {
            'sender': sender,
            'filename': filename,
            'b64data': b64data,
            'file_size': file_size,
            'timestamp': time.time()
        }
        mailbox.append(file_entry)
        print(f"\n📧 Novo arquivo na caixa postal de {sender}: {filename}")

def display_mailbox():
    """
    Exibe o conteúdo da caixa postal
    """
    with mailbox_lock:
        if not mailbox:
            print("\n📪 Caixa postal vazia.")
            return
        
        print("\n" + "="*60)
        print("📫 CAIXA POSTAL - ARQUIVOS RECEBIDOS")
        print("="*60)
        
        for i, file_entry in enumerate(mailbox, 1):
            sender = file_entry['sender']
            filename = file_entry['filename']
            file_size = file_entry['file_size']
            timestamp = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(file_entry['timestamp']))
            
            print(f"{i:2d}. 📎 {filename}")
            print(f"    👤 De: {sender}")
            print(f"    📊 Tamanho: {file_size/1024:.1f}KB")
            print(f"    🕒 Recebido: {timestamp}")
            print("-" * 60)

def manage_mailbox():
    """
    Gerencia a caixa postal - permite ver, baixar e deletar arquivos
    """
    while True:
        display_mailbox()
        
        with mailbox_lock:
            if not mailbox:
                safe_input("\nPressione Enter para voltar ao menu...")
                return
        
        print("\nOpções:")
        print("1. 💾 Baixar arquivo")
        print("2. 🗑️  Deletar arquivo")
        print("3. 🔄 Atualizar lista")
        print("4. ⬅️  Voltar ao menu")
        
        choice = safe_input("Escolha (1-4): ").strip()
        
        if choice == "1":
            download_file_from_mailbox()
        elif choice == "2":
            delete_file_from_mailbox()
        elif choice == "3":
            continue  # Apenas atualiza a exibição
        elif choice == "4":
            break
        else:
            print("❌ Opção inválida! Digite apenas 1, 2, 3 ou 4.")

def download_file_from_mailbox():
    """
    Baixa um arquivo específico da caixa postal
    """
    with mailbox_lock:
        if not mailbox:
            print("❌ Caixa postal vazia.")
            return
        
        while True:
            try:
                file_num = int(safe_input(f"Digite o número do arquivo (1-{len(mailbox)}): "))
                if 1 <= file_num <= len(mailbox):
                    break
                print(f"❌ Digite apenas números entre 1 e {len(mailbox)}")
            except ValueError:
                print("❌ Digite apenas números!")
            except KeyboardInterrupt:
                return
        
        file_entry = mailbox[file_num - 1]
    
    try:
        # Criar diretório downloads se não existir
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
            print("📁 Diretório 'downloads' criado")
        
        # Evitar sobrescrever arquivos
        base_name = os.path.splitext(file_entry['filename'])[0]
        extension = os.path.splitext(file_entry['filename'])[1]
        counter = 1
        new_filename = file_entry['filename']
        
        while os.path.exists(os.path.join("downloads", new_filename)):
            new_filename = f"{base_name}_{counter}{extension}"
            counter += 1
        
        filepath = os.path.join("downloads", new_filename)
        
        print("⏳ Baixando arquivo...")
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(file_entry['b64data']))
        
        actual_size = os.path.getsize(filepath)
        print(f"✅ Arquivo baixado com sucesso!")
        print(f"📁 Local: {filepath}")
        print(f"📊 Tamanho: {actual_size/1024:.1f}KB")
        
        # Perguntar se quer deletar da caixa postal
        delete_choice = safe_input("Deletar arquivo da caixa postal? (s/n): ").lower()
        if delete_choice in ['s', 'sim', 'y', 'yes']:
            with mailbox_lock:
                mailbox.pop(file_num - 1)
            print("🗑️ Arquivo removido da caixa postal.")
        
    except Exception as e:
        print(f"❌ Erro ao baixar arquivo: {e}")

def delete_file_from_mailbox():
    """
    Deleta um arquivo específico da caixa postal
    """
    with mailbox_lock:
        if not mailbox:
            print("❌ Caixa postal vazia.")
            return
        
        while True:
            try:
                file_num = int(safe_input(f"Digite o número do arquivo (1-{len(mailbox)}): "))
                if 1 <= file_num <= len(mailbox):
                    break
                print(f"❌ Digite apenas números entre 1 e {len(mailbox)}")
            except ValueError:
                print("❌ Digite apenas números!")
            except KeyboardInterrupt:
                return
        
        file_entry = mailbox[file_num - 1]
        filename = file_entry['filename']
        sender = file_entry['sender']
        
        confirm = safe_input(f"Confirma a exclusão de '{filename}' de {sender}? (s/n): ").lower()
        if confirm in ['s', 'sim', 'y', 'yes']:
            mailbox.pop(file_num - 1)
            print(f"🗑️ Arquivo '{filename}' removido da caixa postal.")
        else:
            print("❌ Exclusão cancelada.")

def get_mailbox_count():
    """
    Retorna o número de arquivos na caixa postal
    """
    with mailbox_lock:
        return len(mailbox)

def handle_messages():
<<<<<<< Updated upstream
    global waiting_for_file_decision, pending_file_data, name_registered, waiting_for_name
=======
    """
    Thread dedicada para receber e processar mensagens do servidor
    Roda continuamente em background processando:
    - msg: mensagens de texto
    - online_users: lista de usuarios online
    - file: arquivos recebidos (agora vai para caixa postal)
    """
    global name_registered, waiting_for_name
>>>>>>> Stashed changes
    
    while True:
        try:
            msg = client.recv(2048 * 10).decode(FORMAT)
            if msg:
                key, value = msg.split("=", 1)
                
                if key == "msg":
<<<<<<< Updated upstream
                    # CORREÇÃO: Verificar se é mensagem do servidor sobre nome duplicado
=======
                    # Verificar se é mensagem do servidor sobre nome duplicado
>>>>>>> Stashed changes
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
                        # Não fazer nada aqui, deixar o loop principal tratar
                    else:
                        print(f"\n💬 {value}")
                        
                elif key == "online_users":
                    # Trata a resposta da lista de usuários online
                    display_online_users(value)
                    
                elif key == "file":
                    # Format: sender||filename||b64data
                    parts = value.split("||", 2)
                    if len(parts) == 3:
                        sender, filename, b64data = parts
                        file_size = (len(b64data) * 3) // 4  # Approximate size in bytes
                        
<<<<<<< Updated upstream
                        # Store pending file data
                        pending_file_data = {
                            'sender': sender,
                            'filename': filename,
                            'b64data': b64data,
                            'file_size': file_size
                        }
                        
                        # Mark that we're waiting for file decision
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
                        
                        # Don't capture input here - will be handled in main menu
=======
                        # Adicionar à caixa postal
                        add_to_mailbox(sender, filename, b64data, file_size)
>>>>>>> Stashed changes
                        
                    else:
                        # Compatibility with old format
                        try:
                            filename, b64data = value.split("||", 1)
                            file_size = (len(b64data) * 3) // 4
                            add_to_mailbox("Desconhecido", filename, b64data, file_size)
                        except:
                            print("❌ Erro ao processar arquivo (formato incompatível)")
                            
        except Exception as e:
            print(f"❌ Erro ao receber mensagem: {e}")
            break

<<<<<<< Updated upstream
def process_pending_file():
    """Process pending file when called from main menu"""
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
            # Create downloads directory if it doesn't exist
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
                print("📁 Diretório 'downloads' criado")
            
            # Avoid overwriting files
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
    
    # Clear state
    waiting_for_file_decision = False
    pending_file_data = None

=======
>>>>>>> Stashed changes
def send(message):
    try:
        client.send(json.dumps(message).encode(FORMAT))
    except Exception as e:
        print(f"Erro ao enviar: {e}")

def send_global_message():
    message, is_text, filename = capture_message()
    if message is None:
        return
    if is_text:
        message_formatted = {"type": "msg", "control": "4all", "message": message}
    else:
        message_formatted = {"type": "file", "control": "4all", "message": message, "filename": filename}
    send(message_formatted)

def send_private_message():
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
    """CORREÇÃO: Função melhorada para lidar com nomes duplicados"""
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
    """Solicita a lista de usuários online do servidor"""
    if not name_registered:
        print("❌ Você precisa definir um nome primeiro!")
        return
        
    print("⏳ Buscando usuários online...")
    message_formatted = {"type": "online_usr", "control": "dontcare", "message": "dontcare"}
    send(message_formatted)
    # A resposta será tratada automaticamente pela função handle_messages()
    time.sleep(0.5)  # Pequena pausa para dar tempo da resposta chegar

def select_file():
    """File selection using Tkinter graphical interface"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create invisible main window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        root.wm_attributes('-topmost', 1)  # Put in front
        
        # Force focus
        if platform.system() == "Windows":
            root.wm_attributes('-alpha', 0.0)  # Transparent on Windows
        
        # Open dialog
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo para enviar",
            filetypes=[
                ("Todos os arquivos", "*.*"),
                ("Documentos de texto", "*.txt *.doc *.docx *.pdf"),
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Arquivos de código", "*.py *.js *.html *.css *.json")
            ]
        )
        
        # Destroy window
        root.destroy()
        
        return filepath if filepath else None
        
    except Exception as e:
        print(f"❌ Erro ao abrir seletor de arquivos: {e}")
        return None

def capture_message():
    print("\nTipo de mensagem:")
    print("1. 💬 Texto")
    print("2. 📎 Arquivo")
    
    while True:
        control = safe_input("Escolha (1-2): ").strip()
        if control in ['1', '2']:
            break
        print("❌ Digite apenas 1 ou 2")
    
    if control == "1":
        message = safe_input("\n✏️  Digite sua mensagem: ")
        return message, True, None
        
    elif control == "2":
        print("\n📎 ENVIO DE ARQUIVO")
        path = select_file()
        if not path or not os.path.isfile(path):
            print("❌ Arquivo não encontrado ou seleção cancelada.")
            return None, False, None
            
        # Check file size
        size = os.path.getsize(path)
        if size > 10 * 1024 * 1024:  # 10MB
            print(f"⚠️  Arquivo muito grande ({size/1024/1024:.1f}MB). Máximo recomendado: 10MB")
            if safe_input("Continuar mesmo assim? (s/n): ").lower() != 's':
                return None, False, None
        
        filename = os.path.basename(path)
        print(f"\n📤 Preparando envio...")
        print(f"📄 Arquivo: {filename}")
        print(f"📊 Tamanho: {size/1024:.1f}KB")
        
        try:
            print("⏳ Codificando arquivo...")
            with open(path, "rb") as file:
                data = base64.b64encode(file.read()).decode(FORMAT)
            print("✅ Arquivo pronto para envio!")
            return data, False, filename
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
            return None, False, None

def start_sending():
<<<<<<< Updated upstream
    global waiting_for_file_decision, name_registered
=======
    """
    Funcao principal do cliente - gerencia todo o fluxo de interacao
    1. Solicita nome do usuario
    2. Aguarda confirmacao do servidor
    3. Apresenta menu principal com opcoes (incluindo caixa postal)
    """
    global name_registered
>>>>>>> Stashed changes
    
    print("\n🎉 Bem-vindo ao Chat!")
    if (private_key and public_key):
        print(f"🔐 Chaves Diffie-Hellman geradas com sucesso: {private_key}, {public_key}")
    send_name()
    
    # Aguardar confirmação do nome
    while not name_registered:
        time.sleep(0.1)
    
    print("\n" + "="*50)
    print("📋 MENU PRINCIPAL")
    print("="*50)
    
    while True:
<<<<<<< Updated upstream
        # Check if there's a pending file to process
        if waiting_for_file_decision:
            print("\n⚠️  Você tem um arquivo pendente para processar!")
            process_pending_file()
            continue
=======
        # Mostrar contador de arquivos na caixa postal
        mailbox_count = get_mailbox_count()
        mailbox_indicator = f" ({mailbox_count} arquivos)" if mailbox_count > 0 else ""
>>>>>>> Stashed changes
        
        print("\nEscolha uma opção:")
        print("1. 🌐 Mensagem global (todos)")
        print("2. 🔒 Mensagem privada")
        print("3. 👥 Listar usuários online")
        print(f"4. 📫 Caixa postal{mailbox_indicator}")
        print("5. ❌ Sair")
        print("-"*30)
        
        option = safe_input("Escolha (1-5): ").strip()
        
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
            print("\n📫 CAIXA POSTAL")
            manage_mailbox()
        elif option == "5":
            print("\n👋 Saindo do chat...")
            break
        else:
            print("❌ Opção inválida! Digite apenas 1, 2, 3, 4 ou 5.")

def start():
    thread1 = threading.Thread(target=handle_messages, daemon=True)
    thread1.start()
    start_sending()

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\n👋 Cliente desconectado.")
    except Exception as e:
        print(f"❌ Erro no cliente: {e}")
    finally:
        try:
            client.close()
        except:
            pass