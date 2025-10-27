"""
Utilitários e funções auxiliares para o serviço de extração de PDFs.
"""
import os
import hashlib
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_email_credentials(email: str, password: str) -> bool:
    """
    Valida se as credenciais de e-mail estão no formato correto.
    
    Args:
        email: Endereço de e-mail
        password: Senha do e-mail
        
    Returns:
        bool: True se as credenciais são válidas, False caso contrário
    """
    if not email or not password:
        return False
    
    # Verificar formato básico do e-mail
    if '@' not in email or '.' not in email.split('@')[-1]:
        return False
    
    # Verificar se a senha não está vazia
    if len(password.strip()) == 0:
        return False
    
    return True


def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    Cria um diretório se ele não existir.
    
    Args:
        directory_path: Caminho do diretório
        
    Returns:
        bool: True se o diretório foi criado ou já existia, False caso contrário
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Erro ao criar diretório {directory_path}: {e}")
        return False


def get_file_size_mb(file_path: str) -> float:
    """
    Obtém o tamanho de um arquivo em MB.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        float: Tamanho em MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except Exception as e:
        logger.error(f"Erro ao obter tamanho do arquivo {file_path}: {e}")
        return 0.0


def calculate_file_hash(file_path: str) -> str:
    """
    Calcula o hash MD5 de um arquivo.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        str: Hash MD5 do arquivo
    """
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"Erro ao calcular hash do arquivo {file_path}: {e}")
        return ""


def is_valid_pdf_file(file_path: str) -> bool:
    """
    Verifica se um arquivo é um PDF válido lendo o cabeçalho.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        bool: True se é um PDF válido, False caso contrário
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except Exception as e:
        logger.error(f"Erro ao verificar arquivo PDF {file_path}: {e}")
        return False


def clean_filename(filename: str) -> str:
    """
    Limpa um nome de arquivo removendo caracteres inválidos.
    
    Args:
        filename: Nome do arquivo original
        
    Returns:
        str: Nome do arquivo limpo
    """
    # Caracteres inválidos no Windows/Linux
    invalid_chars = '<>:"/\\|?*'
    
    cleaned = filename
    for char in invalid_chars:
        cleaned = cleaned.replace(char, '_')
    
    # Remover espaços extras e caracteres de controle
    cleaned = ' '.join(cleaned.split())
    
    # Limitar tamanho do nome
    if len(cleaned) > 200:
        name, ext = os.path.splitext(cleaned)
        cleaned = name[:200-len(ext)] + ext
    
    return cleaned


def get_disk_space_mb(directory_path: str) -> float:
    """
    Obtém o espaço livre em disco em MB.
    
    Args:
        directory_path: Caminho do diretório
        
    Returns:
        float: Espaço livre em MB
    """
    try:
        statvfs = os.statvfs(directory_path)
        free_bytes = statvfs.f_frsize * statvfs.f_bavail
        return round(free_bytes / (1024 * 1024), 2)
    except Exception as e:
        logger.error(f"Erro ao obter espaço em disco para {directory_path}: {e}")
        return 0.0


def format_file_size(size_bytes: int) -> str:
    """
    Formata o tamanho de um arquivo em uma string legível.
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        str: Tamanho formatado (ex: "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{round(size_bytes / 1024, 2)} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{round(size_bytes / (1024 * 1024), 2)} MB"
    else:
        return f"{round(size_bytes / (1024 * 1024 * 1024), 2)} GB"


def get_file_extension(filename: str) -> str:
    """
    Obtém a extensão de um arquivo em minúsculas.
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        str: Extensão do arquivo (ex: ".pdf")
    """
    return Path(filename).suffix.lower()


def is_safe_filename(filename: str) -> bool:
    """
    Verifica se um nome de arquivo é seguro (não contém caminhos relativos).
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        bool: True se é seguro, False caso contrário
    """
    # Verificar se contém caminhos relativos perigosos
    dangerous_patterns = ['../', '..\\', '/', '\\']
    
    for pattern in dangerous_patterns:
        if pattern in filename:
            return False
    
    return True


def create_backup_filename(original_path: str) -> str:
    """
    Cria um nome de arquivo de backup para evitar sobrescrever arquivos existentes.
    
    Args:
        original_path: Caminho original do arquivo
        
    Returns:
        str: Caminho do arquivo de backup
    """
    path = Path(original_path)
    counter = 1
    
    while path.exists():
        new_name = f"{path.stem}_backup_{counter}{path.suffix}"
        path = path.parent / new_name
        counter += 1
    
    return str(path)
