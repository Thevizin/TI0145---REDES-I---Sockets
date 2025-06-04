# 💬 Chat Multi-Cliente em Python com AI Bot

Um sistema de chat completo desenvolvido em Python com socket programming, suportando mensagens de texto, envio de arquivos, comunicação privada/global e integração com AI via Ollama.

## ✨ Funcionalidades

### Chat Básico
- 🌐 **Mensagens Globais**: Envie mensagens para todos os usuários conectados
- 🔒 **Mensagens Privadas**: Converse diretamente com usuários específicos
- 📎 **Envio de Arquivos**: Compartilhe arquivos de qualquer tipo (com interface gráfica)
- 👥 **Lista de Usuários Online**: Veja quem está conectado em tempo real
- 📜 **Histórico de Mensagens**: Mensagens globais são mantidas para novos usuários
- 💾 **Download de Arquivos**: Receba e salve arquivos automaticamente
- 🛡️ **Interface Thread-Safe**: Evita conflitos de entrada simultânea
- 🔍 **Descoberta Automática**: Encontra o servidor na rede local automaticamente

### AI Bot (Novo!)
- 🤖 **ChatBot Inteligente**: Bot AI que responde automaticamente mensagens privadas
- 🧠 **Integração Ollama**: Utiliza modelos locais de IA (Qwen, Llama, etc.)
- 🎯 **Respostas Contextuais**: Processa e responde perguntas em linguagem natural
- 🔄 **Funcionamento Automático**: Conecta e responde sem intervenção manual
- 📊 **Monitoramento**: Logs detalhados de atividade e status de conexão

## 🚀 Como Executar

### Pré-requisitos

- Python 3.6 ou superior
- Biblioteca `tkinter` (geralmente incluída no Python)
- **Para o AI Bot**: [Ollama](https://ollama.ai) instalado localmente

### Configuração do AI Bot (Opcional)

1. **Instale o Ollama:**
   ```bash
   # Linux/macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows: Baixe de https://ollama.ai/download
   ```

2. **Baixe um modelo de IA:**
   ```bash
   ollama pull qwen2.5:4b  # Modelo recomendado (leve)
   # ou
   ollama pull llama3.2     # Modelo alternativo
   ```

3. **Inicie o servidor Ollama:**
   ```bash
   ollama serve
   ```

### Executando no Terminal

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd chat-python
   ```

2. **Execute o servidor:**
   ```bash
   python server.py
   ```

3. **Execute o(s) cliente(s) em terminais separados:**
   ```bash
   python client.py
   ```

4. **Execute o AI Bot (opcional):**
   ```bash
   python ai_client.py
   ```

### 💡 Executando no VS Code com Terminais Divididos

#### Método 1: Usando o Terminal Integrado

1. **Abra o VS Code** na pasta do projeto
2. **Abra o terminal integrado**: `Ctrl + ` ` (backtick) ou `View > Terminal`
3. **Divida o terminal**:
   - Clique no ícone **"+"** no canto superior direito do terminal
   - Ou use `Ctrl + Shift + 5` para dividir o terminal
   - Ou clique no ícone **"Split Terminal"** (ícone de divisão)

4. **Execute os programas**:
   - **Terminal 1**: `python server.py`
   - **Terminal 2**: `python client.py`
   - **Terminal 3**: `python ai_client.py` (opcional - AI Bot)
   - **Terminal 4** (opcional): `python client.py` (mais clientes)

#### Método 2: Usando Múltiplas Abas de Terminal

1. **Terminal 1**: `Ctrl + Shift + ` ` (novo terminal)
2. **Terminal 2**: Clique no **"+"** para criar nova aba
3. **Terminal 3**: Repita conforme necessário

#### Método 3: Usando a Paleta de Comandos

1. Pressione `Ctrl + Shift + P`
2. Digite "Terminal: Create New Terminal"
3. Repita para criar múltiplos terminais

## 🎮 Como Usar

### Primeiro Uso

1. **Inicie o servidor** primeiro
2. **(Opcional) Inicie o AI Bot** se quiser ter assistente IA
3. **Execute um ou mais clientes**
4. **Digite seu nome** quando solicitado
5. **Navegue pelo menu** com as opções numeradas

### Menu Principal

```
📋 MENU PRINCIPAL
==========================================

Escolha uma opção:
1. 🌐 Mensagem global (todos)
2. 🔒 Mensagem privada
3. 👥 Listar usuários online
4. ❌ Sair
```

### Enviando Mensagens

- **Mensagem de Texto**: Digite sua mensagem normalmente
- **Envio de Arquivo**: Selecione um arquivo através da interface gráfica
- **Mensagem Privada**: Digite o nome exato do destinatário

### Interagindo com o AI Bot

1. **Certifique-se que o ChatBot está online** (use opção 3 para verificar)
2. **Envie uma mensagem privada** (opção 2)
3. **Digite "ChatBot"** como destinatário
4. **Faça sua pergunta** em linguagem natural
5. **Aguarde a resposta** do bot

**Exemplos de perguntas para o ChatBot:**
- "Qual é a capital do Brasil?"
- "Explique como funciona a internet"
- "Conte uma piada"
- "Resuma a história da Segunda Guerra Mundial"
- "Como fazer um bolo de chocolate?"

### Recebendo Arquivos

Quando receber um arquivo, você verá:

```
==================================================
📎 ARQUIVO RECEBIDO
👤 De: João
📄 Arquivo: documento.pdf
📊 Tamanho: 245.3KB
==================================================
O que deseja fazer?
1. 💾 Baixar arquivo
2. ❌ Ignorar
```

Os arquivos baixados são salvos na pasta `downloads/`.

## 📁 Estrutura do Projeto

```
chat-python/
├── server.py          # Servidor principal do chat
├── client.py          # Cliente humano do chat
├── ai_client.py       # Cliente AI Bot (novo!)
├── downloads/         # (criada automaticamente) Arquivos recebidos
└── README.md          # Este arquivo
```

## 🔧 Configuração

### Alterando IP/Porta

**No servidor** (`server.py`):
```python
SERVER_IP = "0.0.0.0"  # Aceita de qualquer IP
PORT = 5050           # Porta principal
```

**Nos clientes** (`client.py` e `ai_client.py`):
```python
PORT = 5050  # Deve coincidir com o servidor
# IP é descoberto automaticamente via broadcast
```

### Configuração do AI Bot

**No arquivo `ai_client.py`**, você pode alterar:

```python
def ask_ai(prompt, model="qwen2.5:4b"):  # Modelo padrão
```

**Modelos disponíveis no Ollama:**
- `qwen2.5:4b` - Leve e rápido (recomendado)
- `llama3.2` - Modelo padrão da Meta
- `gemma2` - Modelo do Google
- `mistral` - Modelo francês especializado
- `codellama` - Especializado em código

**Para listar modelos instalados:**
```bash
ollama list
```

**Para baixar novos modelos:**
```bash
ollama pull nome-do-modelo
```

### Limites e Configurações

**Limite de Arquivo:**
```python
if size > 10 * 1024 * 1024:  # 10MB padrão
```

**Timeout do AI Bot:**
```python
timeout=30  # 30 segundos para resposta da IA
```

**Porta de Descoberta:**
```python
5051  # Porta UDP para auto-descoberta
```

## 🛠️ Tecnologias Utilizadas

### Core do Chat
- **Socket Programming**: Comunicação cliente-servidor TCP/UDP
- **Threading**: Manipulação simultânea de múltiplos clientes
- **JSON**: Protocolo de comunicação estruturada
- **Base64**: Codificação de arquivos para transmissão
- **Tkinter**: Interface gráfica para seleção de arquivos

### AI Bot
- **Ollama**: Framework para executar LLMs localmente
- **Requests**: HTTP client para comunicação com Ollama API
- **Auto-discovery**: Protocolo UDP para encontrar servidor automaticamente

## 📊 Recursos Técnicos

### Arquitetura do Chat
- **Multi-threading**: Cada cliente é tratado em thread separada
- **Sincronização**: Uso de locks para evitar conflitos de entrada
- **Protocolo Personalizado**: Comunicação estruturada em JSON
- **Gestão de Estado**: Controle de arquivos pendentes e usuários online
- **Tratamento de Erros**: Recuperação graceful de falhas de conexão
- **Descoberta Automática**: Localização do servidor via broadcast UDP

### Arquitetura do AI Bot
- **Processamento Assíncrono**: Thread separada para monitorar mensagens
- **Cache de Conexão**: Reutilização de conexões HTTP com Ollama
- **Fallback Graceful**: Continua funcionando mesmo sem Ollama
- **Logs Detalhados**: Monitoramento completo de atividades
- **Detecção de Mensagens**: Parseamento inteligente de mensagens privadas

## 🐛 Solução de Problemas

### Problemas Gerais

**"ConnectionRefusedError"**
- Certifique-se de que o servidor está rodando antes dos clientes
- Verifique se a porta 5050 não está sendo usada por outro programa

**"ModuleNotFoundError: tkinter"**
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: Tkinter vem incluído com Python do python.org
- **Windows**: Geralmente incluído por padrão

**Arquivos não são recebidos**
- Verifique as permissões da pasta
- Certifique-se de que há espaço em disco suficiente

**"Usuário não encontrado"**
- Digite o nome exato do usuário (case-sensitive)
- Use a opção "Listar usuários online" para ver nomes disponíveis

### Problemas do AI Bot

**"❌ Ollama não está rodando"**
- Execute `ollama serve` em um terminal separado
- Verifique se a porta 11434 não está bloqueada

**"❌ Modelo não encontrado"**
- Liste modelos: `ollama list`
- Baixe o modelo: `ollama pull qwen2.5:4b`

**"❌ Timeout ao aguardar resposta"**
- Modelo pode estar sendo carregado pela primeira vez (aguarde)
- Tente um modelo menor como `qwen2.5:4b`
- Verifique recursos do sistema (RAM, CPU)

**Bot não responde**
- Verifique se o bot está online: liste usuários (opção 3)
- Certifique-se de enviar mensagem privada para "ChatBot" (exato)
- Verifique logs do AI Bot no terminal

**"❌ Não foi possível conectar ao Ollama"**
- Verifique se Ollama está instalado: `ollama --version`
- Reinicie o serviço: `ollama serve`
- Teste manualmente: `curl http://localhost:11434/api/tags`

## 🎯 Fluxo de Funcionamento

### Descoberta Automática
1. Cliente envia broadcast UDP "CHAT_DISCOVER" na porta 5051
2. Servidor responde "CHAT_SERVER" com seu IP
3. Cliente conecta no IP descoberto na porta 5050

### Comunicação Chat
1. Cliente envia nome em JSON: `{"type": "name", "message": "João"}`
2. Servidor valida e confirma registro
3. Cliente pode enviar mensagens, arquivos ou listar usuários
4. Servidor roteia mensagens baseado no campo "control"

### AI Bot
1. AI Bot conecta como cliente normal com nome "ChatBot"
2. Monitora mensagens privadas direcionadas a ele
3. Extrai pergunta e envia para Ollama API local
4. Retorna resposta formatada para o remetente

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎯 Próximas Funcionalidades

### Chat
- [ ] Salas de chat separadas
- [ ] Criptografia de mensagens
- [ ] Interface gráfica completa (GUI)
- [ ] Histórico persistente em banco de dados
- [ ] Notificações desktop
- [ ] Emojis e formatação de texto
- [ ] Status de usuário (online/ausente/ocupado)
- [ ] Mensagens com timestamps
- [ ] Sistema de moderação

### AI Bot
- [ ] Múltiplos bots especializados
- [ ] Comandos especiais (!help, !weather, etc.)
- [ ] Integração com outras APIs (tradução, clima, etc.)
- [ ] Memória de conversas
- [ ] Personalidades diferentes por bot
- [ ] Geração de imagens
- [ ] Análise de sentimentos
- [ ] Resumo de conversas

## 💡 Dicas de Uso

### Chat Geral
- Use nomes de usuário únicos para evitar conflitos
- Arquivos grandes podem demorar para ser transmitidos
- Mensagens privadas não são salvas no histórico global
- O servidor mantém log de todas as atividades no terminal

### AI Bot
- Seja específico nas perguntas para melhores respostas
- O bot funciona melhor com perguntas em português ou inglês
- Evite perguntas muito complexas se usar modelos pequenos
- O primeiro uso pode ser mais lento (carregamento do modelo)
- Use modelos maiores para respostas mais elaboradas

### Performance
- Modelos menores (4B parâmetros) são mais rápidos
- Modelos maiores (7B+) dão respostas mais detalhadas
- Feche outros programas pesados quando usar o AI Bot
- SSD acelera significativamente o carregamento de modelos

## 🔗 Links Úteis

- [Ollama - Site Oficial](https://ollama.ai)
- [Ollama - Modelos Disponíveis](https://ollama.ai/library)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Threading em Python](https://docs.python.org/3/library/threading.html)

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no repositório!**

🤖 **Experimente conversar com o ChatBot - pergunte qualquer coisa!**