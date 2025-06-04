import socket
import threading
import json
import requests
import time

def ask_ai(prompt, model="qwen3:4b"):
    """Send a prompt to Ollama and get the response"""
    try:
        print(f"🤖 Enviando prompt para Ollama: {prompt[:50]}...")
        
        # Test if Ollama is running
        health_response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if health_response.status_code != 200:
            return "❌ Ollama não está rodando. Execute 'ollama serve' primeiro."
        
        # Send the actual prompt
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': model,
                                   'prompt': prompt,
                                   'stream': False
                               },
                               timeout=30)  # 30 second timeout
        
        print(f"📡 Status da resposta Ollama: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', 'Resposta vazia do modelo')
            print(f"✅ Resposta recebida: {ai_response[:100]}...")
            return ai_response
        elif response.status_code == 404:
            return f"❌ Modelo '{model}' não encontrado. Verifique se está instalado com 'ollama list'"
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            return f"❌ Erro HTTP {response.status_code} ao comunicar com Ollama"
            
    except requests.exceptions.ConnectionError:
        return "❌ Não foi possível conectar ao Ollama. Verifique se está rodando na porta 11434"
    except requests.exceptions.Timeout:
        return "❌ Timeout ao aguardar resposta do Ollama (>30s)"
    except requests.exceptions.RequestException as e:
        return f"❌ Erro de requisição Ollama: {e}"
    except Exception as e:
        print(f"❌ Erro inesperado na função ask_ai: {e}")
        return f"❌ Erro inesperado na API Ollama: {e}"

def test_ollama_connection():
    """Test if Ollama is accessible and list available models"""
    try:
        print("🔍 Testando conexão com Ollama...")
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama conectado! Modelos disponíveis:")
            for model in models:
                print(f"  - {model['name']}")
            return True
        else:
            print(f"❌ Ollama respondeu com status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar Ollama: {e}")
        return False

def discover_server(timeout=5):
    """Automatically discover the chat server on the local network"""
    print("🔍 Procurando servidor na rede local...")
    
    discover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discover_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discover_socket.settimeout(timeout)
    
    try:
        discover_socket.sendto(b"CHAT_DISCOVER", ('<broadcast>', 5051))
        data, addr = discover_socket.recvfrom(1024)
        if data == b"CHAT_SERVER":
            server_ip = addr[0]
            print(f"✅ Servidor encontrado: {server_ip}")
            return server_ip
    except Exception as e:
        print(f"❌ Erro na descoberta: {e}")
    finally:
        discover_socket.close()
    return None

class AIClient:
    def __init__(self, server_ip=None, port=5050):
        # Test Ollama connection first
        if not test_ollama_connection():
            print("⚠️  Continuando sem Ollama funcional...")
        
        self.SERVER_IP = server_ip or discover_server()
        if not self.SERVER_IP:
            raise ConnectionError("Não foi possível encontrar o servidor")
        
        self.PORT = port
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.FORMAT = 'utf-8'
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        
        # Send AI client identifier
        self.send_name("ChatBot")
        print("✅ AI Client conectado ao servidor")

    def send(self, message):
        try:
            self.client.send(json.dumps(message).encode(self.FORMAT))
        except Exception as e:
            print(f"Erro ao enviar: {e}")

    def send_name(self, name):
        message = {"type": "name", "control": "dontcare", "message": name}
        self.send(message)

    def send_response(self, to_user, response):
        message = {
            "type": "msg",
            "control": to_user,  # Send as private message to the user
            "message": f"🤖 {response}"
        }
        self.send(message)

    def handle_messages(self):
        while True:
            try:
                msg = self.client.recv(2048).decode(self.FORMAT)
                print(f"DEBUG: Mensagem recebida: {msg}")
                if msg:
                    key, value = msg.split("=", 1)
                    if key == "msg":
                        # Detecta mensagens privadas no formato [remetente -> destinatario]: mensagem
                        if "[" in value and " -> " in value and "]:" in value:
                            # Extrai o remetente
                            sender = value[value.find("[")+1:value.find(" ->")]
                            
                            # Extrai o destinatário
                            start_dest = value.find(" -> ") + 4  # +4 para pular " -> "
                            end_dest = value.find("]:", start_dest)
                            destinatario = value[start_dest:end_dest].strip()
                            
                            print(f"DEBUG: destinatario extraído: '{destinatario}'")
                            
                            # Extrai a mensagem
                            message = value[value.find("]:")+2:].strip()
                            
                            # Exibe toda mensagem privada recebida
                            print(f"\n💬 Mensagem privada de {sender} para {destinatario}: {message}")

                            # Só responde se o destinatário for o próprio ChatBot
                            if destinatario == "ChatBot":
                                print(f"🎯 Processando mensagem para ChatBot...")
                                response = ask_ai(message)
                                time.sleep(1)
                                self.send_response(sender, response)
                                
            except Exception as e:
                print(f"❌ Erro ao receber mensagem: {e}")
                import traceback
                traceback.print_exc()
                break

    def start(self):
        """Start the AI client"""
        print("🤖 Iniciando AI Client...")
        
        # Start message handler in background
        thread = threading.Thread(target=self.handle_messages, daemon=True)
        thread.start()
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 AI Client desconectado.")
        finally:
            self.client.close()

if __name__ == "__main__":
    try:
        ai_client = AIClient()
        ai_client.start()
    except Exception as e:
        print(f"❌ Erro no AI Client: {e}")
        import traceback
        traceback.print_exc()