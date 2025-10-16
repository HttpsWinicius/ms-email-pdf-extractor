# 📧 Email PDF Extractor

O **Email PDF Extractor** é um microsserviço projetado para monitorar caixas de e-mail (Gmail, Outlook, Yahoo, etc.) em tempo real.  
Sempre que um novo e-mail chega com anexos em PDF, o serviço baixa o arquivo e o armazena automaticamente em um bucket cloud.

---

## 🚀 Funcionalidades

- Monitora múltiplas contas de e-mail simultaneamente.  
- Suporte para provedores como Gmail, Outlook e Yahoo.  
- Extração automática de anexos PDF.  
- Upload seguro dos arquivos para **S3** ou **Azure Blob**.  
- Configuração dinâmica via banco de dados (cada cliente tem sua conta monitorada).  
- Logs e monitoramento para observabilidade (via Grafana.

---

## 🧩 Arquitetura

1. Lê as configurações do cliente (provedor, credenciais, pastas a monitorar);
2. Mantém uma conexão ativa com o provedor via IMAP/POP3 API;
3. Ao detectar um novo e-mail, verifica se há anexos PDF;
4. Faz o upload automático para o diretório configurado no S3 ou Blob.

## ⚙️ Tecnologias

- **Linguagem:** Python
- **Cloud:** AWS S3 / Azure Blob Storage  
- **Banco de Dados:** PostgreSQL
- **Monitoramento:** Grafana

## 🐍 Por que Python?

Python é ideal para este tipo de serviço por:
- Possuir bibliotecas maduras para IMAP/SMTP (como `imaplib`, `imapclient`, `mail-parser`);
- Ter SDKs oficiais para AWS e Azure;
- Ser leve para rodar 24/7 com baixo consumo de memória;
- Facilitar integração assíncrona (usando `asyncio` ou `aioimaplib`);
- Rápido desenvolvimento e manutenção simples.

## 📦 Instalação

```bash
git clone https://github.com/seuusuario/email-pdf-extractor.git
cd email-pdf-extractor
pip install -r requirements.txt
```
