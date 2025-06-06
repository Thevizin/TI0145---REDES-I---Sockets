# 💬 Chat Multi-Cliente em Python

Um sistema de chat completo desenvolvido em Python com socket programming, suportando mensagens de texto, envio de arquivos e comunicação privada/global.

## ✨ Funcionalidades

- 🌐 **Mensagens Globais**: Envie mensagens para todos os usuários conectados
- 🔒 **Mensagens Privadas**: Converse diretamente com usuários específicos
- 📎 **Envio de Arquivos**: Compartilhe arquivos de qualquer tipo (com interface gráfica)
- 👥 **Lista de Usuários Online**: Veja quem está conectado em tempo real
- 📜 **Histórico de Mensagens**: Mensagens globais são mantidas para novos usuários
- 💾 **Download de Arquivos**: Receba e salve arquivos automaticamente
- 🛡️ **Interface Thread-Safe**: Evita conflitos de entrada simultânea

## 🚀 Como Executar

### Pré-requisitos

- Python 3.6 ou superior
- Biblioteca `tkinter` (geralmente incluída no Python)

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
   - **Terminal 3** (opcional): `python client.py` (para mais clientes)

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
2. **Execute um ou mais clientes**
3. **Digite seu nome** quando solicitado
4. **Navegue pelo menu** com as opções numeradas

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
├── server.py          # Servidor principal
├── client.py          # Cliente do chat
├── downloads/         # (criada automaticamente) Arquivos recebidos
└── README.md          # Este arquivo
```

## 🔧 Configuração

### Alterando IP/Porta

No início dos arquivos `server.py` e `client.py`, modifique:

```python
SERVER_IP = socket.gethostbyname(socket.gethostname())  # IP automático
PORT = 5050  # Porta do servidor
```

### Limite de Arquivo

Por padrão, o sistema alerta para arquivos maiores que 10MB:

```python
if size > 10 * 1024 * 1024:  # 10MB
```

## 🛠️ Tecnologias Utilizadas

- **Socket Programming**: Comunicação cliente-servidor
- **Threading**: Manipulação simultânea de múltiplos clientes
- **JSON**: Protocolo de comunicação estruturada
- **Base64**: Codificação de arquivos para transmissão
- **Tkinter**: Interface gráfica para seleção de arquivos

## 📊 Recursos Técnicos

- **Multi-threading**: Cada cliente é tratado em thread separada
- **Sincronização**: Uso de locks para evitar conflitos de entrada
- **Protocolo Personalizado**: Comunicação estruturada em JSON
- **Gestão de Estado**: Controle de arquivos pendentes e usuários online
- **Tratamento de Erros**: Recuperação graceful de falhas de conexão

## 🐛 Solução de Problemas

### "ConnectionRefusedError"
- Certifique-se de que o servidor está rodando antes dos clientes
- Verifique se a porta 5050 não está sendo usada por outro programa

### "ModuleNotFoundError: tkinter"
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: Tkinter vem incluído com Python do python.org
- **Windows**: Geralmente incluído por padrão

### Arquivos não são recebidos
- Verifique as permissões da pasta
- Certifique-se de que há espaço em disco suficiente

### "Usuário não encontrado"
- Digite o nome exato do usuário (case-sensitive)
- Use a opção "Listar usuários online" para ver nomes disponíveis

<<<<<<< Updated upstream
## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request
=======
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
>>>>>>> Stashed changes

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎯 Próximas Funcionalidades

- [ ] Salas de chat separadas
- [ ] Criptografia de mensagens
- [ ] Interface gráfica completa
- [ ] Histórico persistente
- [ ] Notificações desktop
- [ ] Emojis e formatação de texto
- [ ] Status de usuário (online/ausente/ocupado)

## 💡 Dicas de Uso

- Use nomes de usuário únicos para evitar conflitos
- Arquivos grandes podem demorar para ser transmitidos
- Mensagens privadas não são salvas no histórico global
- O servidor mantém log de todas as atividades no terminal

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no repositório!**