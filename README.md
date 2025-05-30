# 💬 Chat TCP em Python (Servidor e Cliente)

Este projeto implementa um sistema de **chat via socket TCP** usando **Python**, com suporte a:

- Envio de mensagens **globais** (para todos os usuários)
- Envio de mensagens **privadas** (para um usuário específico)
- Histórico de mensagens globais enviado ao cliente ao se conectar
- Múltiplas conexões simultâneas usando **threads**

---

## ⚙️ Tecnologias utilizadas

- Python 3.x
- `socket`
- `threading`
- `time`

---

## 📁 Estrutura do Projeto

```
chat-socket/
├── server.py   # Código do servidor TCP
├── client.py   # Código do cliente TCP
└── README.md   # Este arquivo
```

---

## 🚀 Como executar localmente (na mesma máquina)

### ✅ Pré-requisitos

- Python 3 instalado
- Terminal com suporte a múltiplas abas ou splits (como o terminal do VS Code, Windows Terminal, tmux, etc.)

### 🔧 Passos para execução

1. Abra um terminal e divida em dois ou mais splits, ou abra várias abas.

2. Em **um terminal**, execute o servidor com:

   ```
   python .\server.py
   ```

   Você verá a saída:

   ```
   [Servidor] Iniciando socket...
   [Servidor] Ouvindo em 127.0.0.1:5050
   ```

3. Em **outros terminais**, execute os clientes:

   ```
   python .\client.py
   ```

   Agora você terá um servidor rodando e dois ou mais clientes conectados para conversar entre si.

---

## 💬 Comandos disponíveis no cliente

### Definir nome do cliente

```
name=SeuNome
```

### Enviar mensagem global para todos

```
msg-4all=Olá pessoal!
```

### Enviar mensagem privada para um usuário específico

```
msg-NomeDoDestinatario=Mensagem privada aqui
```

### Exemplo

```
name=Joao
msg-4all=Oi galera!
msg-Maria=Oi Maria, tudo bem?
```

---

## 🧠 Funcionamento Interno

- O servidor mantém:
  - `messagesGlobal`: histórico de mensagens públicas
  - `messagesPriv`: histórico de mensagens privadas
  - `connections`: lista de conexões ativas e nomes

- Quando um cliente se conecta:
  - Ele recebe todo o histórico de mensagens globais

- Quando uma mensagem é enviada:
  - Se for `msg-4all`, ela é enviada para todos os clientes (menos o remetente)
  - Se for `msg-Nome=...`, ela é enviada apenas ao cliente com aquele nome

---

## 📝 Observações

- As mensagens são codificadas como `utf-8` e enviadas via sockets
- A letra `b` que aparece no terminal vem da representação `bytes` do Python (`b"mensagem"`). Isso é normal ao imprimir objetos do tipo `bytes`.
