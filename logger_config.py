"""
Configuração do sistema de logging para o serviço de extração de PDFs.
"""
import logging
import sys
from typing import Optional

from config import LOGGING_CONFIG


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Configura o sistema de logging da aplicação.
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Usar nível fornecido ou o padrão da configuração
    level = log_level or LOGGING_CONFIG['level']
    
    # Configurar formato do log
    formatter = logging.Formatter(
        LOGGING_CONFIG['format'],
        datefmt=LOGGING_CONFIG['date_format']
    )
    
    # Configurar handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Configurar logger principal
    logger = logging.getLogger('email_pdf_extractor')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remover handlers existentes para evitar duplicação
    if logger.handlers:
        logger.handlers.clear()
    
    # Adicionar handler
    logger.addHandler(console_handler)
    
    # Evitar propagação para loggers pai
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger específico para um módulo.
    
    Args:
        name: Nome do módulo
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(f'email_pdf_extractor.{name}')


class ColoredFormatter(logging.Formatter):
    """Formatter com cores para diferentes níveis de log."""
    
    # Códigos de cores ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Ciano
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Amarelo
        'ERROR': '\033[31m',      # Vermelho
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Adicionar cor baseada no nível
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Aplicar cor ao nível
        record.levelname = f"{color}{record.levelname}{reset}"
        
        return super().format(record)


def setup_colored_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Configura logging com cores para melhor visualização no console.
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Logger configurado com cores
    """
    level = log_level or LOGGING_CONFIG['level']
    
    # Configurar formato do log
    formatter = ColoredFormatter(
        LOGGING_CONFIG['format'],
        datefmt=LOGGING_CONFIG['date_format']
    )
    
    # Configurar handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Configurar logger principal
    logger = logging.getLogger('email_pdf_extractor')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remover handlers existentes
    if logger.handlers:
        logger.handlers.clear()
    
    # Adicionar handler
    logger.addHandler(console_handler)
    
    # Evitar propagação
    logger.propagate = False
    
    return logger
