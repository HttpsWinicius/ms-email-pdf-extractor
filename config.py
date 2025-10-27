"""
Configurações do serviço de extração de PDFs de e-mail.
"""
import os
from typing import Dict, Any

# Configurações de e-mail
EMAIL_CONFIG: Dict[str, Any] = {
    # Gmail IMAP settings
    'imap_server': 'imap.gmail.com',
    'imap_port': 993,
    'use_ssl': True,
    
    # Configurações de monitoramento
    'check_interval': 60,  # segundos
    'max_emails_per_check': 10,  # limite de e-mails por verificação
    
    # Configurações de arquivo
    'download_folder': './downloads',
    'allowed_extensions': ['.pdf'],
    'max_file_size_mb': 50,  # tamanho máximo do arquivo em MB
}

# Configurações de logging
LOGGING_CONFIG: Dict[str, Any] = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# Configurações de e-mail (para ser preenchido pelo usuário)
EMAIL_CREDENTIALS: Dict[str, str] = {
    'email': '',  # Seu e-mail Gmail
    'password': '',  # Senha do app Gmail ou senha da conta
}

def validate_config() -> bool:
    """
    Valida se as configurações necessárias estão preenchidas.
    
    Returns:
        bool: True se as configurações estão válidas, False caso contrário
    """
    if not EMAIL_CREDENTIALS['email'] or not EMAIL_CREDENTIALS['password']:
        return False
    return True

def create_download_folder() -> None:
    """Cria a pasta de download se ela não existir."""
    os.makedirs(EMAIL_CONFIG['download_folder'], exist_ok=True)
