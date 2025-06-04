import socket
import threading
import json
import requests
import time

def ask_ai(prompt, model="qwen3:4b"):
    """
    Envia prompt para o Ollama e retorna a resposta da IA
    
    Args:
        prompt (str): Texto/pergunta para enviar ao modelo de IA
        model (str): Nome do modelo Ollama a ser usado (padrao: qwen3:4b)
    
    Returns:
        str: Resposta da IA ou mensagem de erro
    
    Processo:
        1. Testa se Ollama esta rodando
        2. Envia requisicao POST com o prompt
        3. Retorna resposta ou mensagem de erro apropriada
    """
    try:
        print(f"🤖 Enviando prompt para Ollama: {prompt[:50]}...")
        
        # Testar se Ollama esta rodando verificando endpoint de saude
        health_response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if health_response.status_code != 200:
            return "❌ Ollama não está rodando. Execute 'ollama serve' primeiro."
        
        # Enviar o prompt para geracao
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': model, # Modelo a ser usado
                                   'prompt': prompt, # Texto de entrada
                                   'stream': False # Resposta completa (nao streaming)
                               },
                               timeout=30)  # 30 second timeout
        
        print(f"📡 Status da resposta Ollama: {response.status_code}")
        
        # Processar resposta baseada no status HTTP
        if response.status_code == 200:
            # Sucesso - extrair resposta do JSON
            result = response.json()
            ai_response = result.get('response', 'Resposta vazia do modelo')
            print(f"✅ Resposta recebida: {ai_response[:100]}...")
            return ai_response
        elif response.status_code == 404:
            # Modelo nao encontrado
            return f"❌ Modelo '{model}' não encontrado. Verifique se está instalado com 'ollama list'"
        else:
            # Outros erros HTTP
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            return f"❌ Erro HTTP {response.status_code} ao comunicar com Ollama"
            
    except requests.exceptions.ConnectionError:
        # Ollama nao esta rodando ou inacessivel
        return "❌ Não foi possível conectar ao Ollama. Verifique se está rodando na porta 11434"
    except requests.exceptions.Timeout:
        # Timeout na requisicao
        return "❌ Timeout ao aguardar resposta do Ollama (>30s)"
    except requests.exceptions.RequestException as e:
        # Outros erros de requisicao
        return f"❌ Erro de requisição Ollama: {e}"
    except Exception as e:
        # Erros inesperados
        print(f"❌ Erro inesperado na função ask_ai: {e}")
        return f"❌ Erro inesperado na API Ollama: {e}"

def test_ollama_connection():
    """
    Testa conexao com Ollama e lista modelos disponiveis
    
    Returns:
        bool: True se conexao bem-sucedida, False caso contrario
    
    Funcionalidades:
        - Verifica se Ollama esta acessivel
        - Lista todos os modelos instalados
        - Fornece feedback detalhado sobre o status
    """
    try:
        print("🔍 Testando conexão com Ollama...")
        # Fazer requisicao para listar modelos
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            # Sucesso - extrair lista de modelos
            models = response.json().get('models', [])
            print(f"✅ Ollama conectado! Modelos disponíveis:")
            
            # Listar cada modelo disponivel
            for model in models:
                print(f"  - {model['name']}")
            return True
        else:
            # Erro na resposta
            print(f"❌ Ollama respondeu com status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar Ollama: {e}")
        return False

def discover_server(timeout=5):
    """
    Descobre automaticamente o servidor de chat na rede local
    
    Args:
        timeout (int): Tempo limite para aguardar resposta (segundos)
    
    Returns:
        str or None: IP do servidor encontrado ou None se nao encontrado
    
    Processo:
        1. Cria socket UDP para broadcast
        2. Envia mensagem "CHAT_DISCOVER" na porta 5051
        3. Aguarda resposta "CHAT_SERVER"
        4. Retorna IP do servidor que respondeu
    """
    print("🔍 Procurando servidor na rede local...")
    
    # Criar socket UDP para descoberta por broadcast
    discover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discover_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discover_socket.settimeout(timeout)
    
    try:
        # Enviar mensagem de descoberta via broadcast
        discover_socket.sendto(b"CHAT_DISCOVER", ('<broadcast>', 5051))
        
        # Aguardar resposta do servidor
        data, addr = discover_socket.recvfrom(1024)
        if data == b"CHAT_SERVER":
            server_ip = addr[0]
            print(f"✅ Servidor encontrado: {server_ip}")
            return server_ip
    except Exception as e:
        print(f"❌ Erro na descoberta: {e}")
    finally:
        # Garantir fechamento do socket
        discover_socket.close()
    return None

class AIClient:
    """
    Cliente AI que se conecta ao servidor de chat e responde automaticamente
    
    Funcionalidades:
        - Conecta ao servidor de chat como usuario "ChatBot"
        - Monitora mensagens privadas direcionadas ao bot
        - Processa mensagens usando Ollama AI
        - Responde automaticamente ao remetente
    
    Attributes:
        SERVER_IP (str): IP do servidor de chat
        PORT (int): Porta do servidor (padrao: 5050)
        ADDR (tuple): Endereco completo (IP, porta)
        FORMAT (str): Codificacao de caracteres (utf-8)
        client (socket): Socket de conexao com o servidor
    """
    def __init__(self, server_ip=None, port=5050):
        """
        Inicializa o cliente AI
        
        Args:
            server_ip (str, optional): IP do servidor. Se None, tenta descobrir automaticamente
            port (int): Porta do servidor (padrao: 5050)
        
        Raises:
            ConnectionError: Se nao conseguir encontrar ou conectar ao servidor
        """
        # Testar conexao com Ollama antes de conectar ao chat
        if not test_ollama_connection():
            print("⚠️  Continuando sem Ollama funcional...")
        
        # Descobrir servidor automaticamente se IP nao fornecido
        self.SERVER_IP = server_ip or discover_server()
        if not self.SERVER_IP:
            raise ConnectionError("Não foi possível encontrar o servidor")
        
        # Configurar parametros de conexao
        self.PORT = port
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.FORMAT = 'utf-8'
        
        # Criar e conectar socket TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        
        # Registrar como "ChatBot" no servidor
        self.send_name("ChatBot")
        print("✅ AI Client conectado ao servidor")

    def send(self, message):
        """
        Envia mensagem JSON para o servidor
        
        Args:
            message (dict): Dicionario com dados da mensagem
        
        Processo:
            - Converte dicionario para JSON
            - Codifica em UTF-8
            - Envia via socket
        """
        try:
            self.client.send(json.dumps(message).encode(self.FORMAT))
        except Exception as e:
            print(f"Erro ao enviar: {e}")

    def send_name(self, name):
        """
        Envia nome do cliente para registro no servidor
        
        Args:
            name (str): Nome do cliente (ex: "ChatBot")
        """
        message = {"type": "name", "control": "dontcare", "message": name}
        self.send(message)

    def send_response(self, to_user, response):
        """
        Envia resposta privada para um usuario especifico
        
        Args:
            to_user (str): Nome do usuario destinatario
            response (str): Texto da resposta da IA
        
        Formato da mensagem:
            - type: "msg" (mensagem de texto)
            - control: nome do destinatario (mensagem privada)
            - message: resposta com prefixo de bot
        """
        message = {
            "type": "msg",
            "control": to_user,  # Enviar como mensagem privada para o usuario
            "message": f"🤖 {response}"
        }
        self.send(message)

    def handle_messages(self):
        """
        Thread principal para processar mensagens recebidas do servidor
        
        Funcionalidades:
            - Monitora mensagens em loop infinito
            - Detecta mensagens privadas no formato: [remetente -> destinatario]: mensagem
            - Responde apenas quando destinatario for "ChatBot"
            - Processa mensagem com IA e envia resposta
        
        Formato esperado das mensagens privadas:
            "[NomeUsuario -> ChatBot]: Qual e a capital do Brasil?"
        """
        while True:
            try:
                # Receber mensagem do servidor
                msg = self.client.recv(2048).decode(self.FORMAT)
                print(f"DEBUG: Mensagem recebida: {msg}")
                if msg:
                    # Separar tipo da mensagem do conteudo
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
        """
        Inicia o cliente AI
        
        Funcionalidades:
            - Cria thread daemon para processar mensagens
            - Mantem thread principal ativo
            - Trata interrupcao por teclado (Ctrl+C)
            - Garante fechamento adequado da conexao
        """
        print("🤖 Iniciando AI Client...")
        
        # Criar thread daemon para processar mensagens em backgroundd
        thread = threading.Thread(target=self.handle_messages, daemon=True)
        thread.start()
        
        try:
            # Manter thread principal ativo
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 AI Client desconectado.")
        finally:
            # Garantir fechamento da conexao
            self.client.close()

# Ponto de entrada do programa
if __name__ == "__main__":
    try:
        ai_client = AIClient()
        ai_client.start()
    except Exception as e:
        print(f"❌ Erro no AI Client: {e}")
        import traceback
        traceback.print_exc()