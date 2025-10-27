# 📧 MS Email PDF Extractor

Serviço em Python para monitoramento automático de e-mails e extração de anexos PDF.

## 🚀 Funcionalidades

- ✅ Monitoramento contínuo de conta Gmail via IMAP
- ✅ Detecção automática de e-mails não lidos com anexos PDF
- ✅ Download e salvamento local de PDFs
- ✅ Marcação automática de e-mails como lidos
- ✅ Sistema de logging completo com cores
- ✅ Tratamento robusto de erros
- ✅ Validação de arquivos e segurança

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Conta Gmail com App Password habilitado

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd ms-email-pdf-extractor
```

2. **Configure suas credenciais:**
   - Abra o arquivo `config.py`
   - Preencha suas credenciais de e-mail:
```python
EMAIL_CREDENTIALS = {
    'email': 'seu-email@gmail.com',
    'password': 'sua-senha-do-app',  # Use App Password do Gmail
}
```

3. **Configure o Gmail (IMPORTANTE):**
   - Ative a verificação em 2 etapas na sua conta Google
   - Gere uma "Senha de app" específica para este serviço
   - Use essa senha de app no campo `password` do config.py

## 🚀 Como usar

### Execução básica:
```bash
python main.py
```

### O que acontece:
1. O serviço conecta com sua conta Gmail
2. Verifica e-mails não lidos a cada 60 segundos
3. Identifica e-mails com anexos PDF
4. Baixa os PDFs para a pasta `./downloads/`
5. Marca os e-mails como lidos
6. Exibe logs detalhados no console

### Parar o serviço:
- Pressione `Ctrl+C` para parar o monitoramento

## 📁 Estrutura do Projeto

```
ms-email-pdf-extractor/
├── main.py              # Script principal
├── config.py            # Configurações
├── email_client.py      # Cliente IMAP
├── pdf_extractor.py     # Extrator de PDFs
├── logger_config.py     # Configuração de logs
├── utils.py             # Utilitários
├── requirements.txt     # Dependências
├── README.md           # Documentação
└── downloads/          # Pasta para PDFs baixados
```

## ⚙️ Configurações

### config.py
```python
EMAIL_CONFIG = {
    'imap_server': 'imap.gmail.com',
    'imap_port': 993,
    'check_interval': 60,           # Segundos entre verificações
    'max_emails_per_check': 10,     # Máximo de e-mails por verificação
    'download_folder': './downloads',
    'max_file_size_mb': 50,         # Tamanho máximo do arquivo
}
```

## 🔧 Configuração do Gmail

### 1. Ativar verificação em 2 etapas:
- Acesse: https://myaccount.google.com/security
- Ative "Verificação em duas etapas"

### 2. Gerar senha de app:
- Acesse: https://myaccount.google.com/apppasswords
- Selecione "E-mail" e "Outro (nome personalizado)"
- Digite "MS Email PDF Extractor"
- Copie a senha gerada (16 caracteres)
- Use essa senha no `config.py`

## 📊 Logs

O sistema exibe logs coloridos no console:
- 🟢 **INFO**: Operações normais
- 🟡 **WARNING**: Avisos importantes
- 🔴 **ERROR**: Erros que precisam atenção
- 🔵 **DEBUG**: Informações detalhadas (quando habilitado)

## 🛡️ Segurança

- ✅ Validação de tipos de arquivo
- ✅ Verificação de tamanho máximo
- ✅ Sanitização de nomes de arquivo
- ✅ Conexão SSL segura
- ✅ Tratamento de erros robusto

## 🔮 Funcionalidades Futuras

- [ ] Suporte a múltiplos provedores (Outlook, Yahoo)
- [ ] Autenticação via banco de dados
- [ ] Upload automático para AWS S3/Azure Blob
- [ ] Interface web para monitoramento
- [ ] Filtros avançados de e-mail
- [ ] Notificações por e-mail/Slack

## 🐛 Solução de Problemas

### Erro de autenticação:
- Verifique se a senha de app está correta
- Confirme se a verificação em 2 etapas está ativa
- Teste a conexão manualmente

### E-mails não detectados:
- Verifique se os e-mails estão realmente não lidos
- Confirme se possuem anexos PDF
- Verifique os logs para erros específicos

### Problemas de permissão:
- Verifique se a pasta `downloads/` pode ser criada
- Confirme permissões de escrita no diretório

## 📝 Exemplo de Uso

```python
# Executar o serviço
python main.py

# Saída esperada:
# 2024-01-15 10:30:00 - INFO - 🚀 Iniciando serviço de monitoramento de e-mail
# 2024-01-15 10:30:01 - INFO - 📁 Pasta de download: ./downloads
# 2024-01-15 10:30:02 - INFO - ✅ Serviço iniciado com sucesso!
# 2024-01-15 10:30:02 - INFO - ⏰ Verificando e-mails a cada 60 segundos
# 2024-01-15 10:31:02 - INFO - 📧 Encontrados 2 e-mails não lidos
# 2024-01-15 10:31:02 - INFO - 📨 Processando e-mail: Relatório Mensal...
# 2024-01-15 10:31:02 - INFO - 📎 Encontrados 1 anexos PDF:
# 2024-01-15 10:31:02 - INFO -    📄 relatorio_janeiro.pdf (2.5 MB)
# 2024-01-15 10:31:03 - INFO - ✅ 1 PDF(s) extraído(s) com sucesso:
# 2024-01-15 10:31:03 - INFO -    💾 Salvo em: ./downloads/relatorio_janeiro_12345_20240115_103103.pdf
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção de solução de problemas
2. Consulte os logs do sistema
3. Abra uma issue no repositório