"""
Módulo para extração e processamento de anexos PDF de e-mails.
"""
import os
import email.message
import logging
from typing import List, Tuple, Optional
from pathlib import Path
import mimetypes

from config import EMAIL_CONFIG

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Classe para extrair e processar anexos PDF de e-mails."""
    
    def __init__(self):
        self.download_folder = Path(EMAIL_CONFIG['download_folder'])
        self.allowed_extensions = EMAIL_CONFIG['allowed_extensions']
        self.max_file_size = EMAIL_CONFIG['max_file_size_mb'] * 1024 * 1024  # Converter para bytes
    
    def has_pdf_attachments(self, email_message: email.message.Message) -> bool:
        """
        Verifica se o e-mail possui anexos PDF.
        
        Args:
            email_message: Objeto do e-mail
            
        Returns:
            bool: True se possui anexos PDF, False caso contrário
        """
        try:
            for part in email_message.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        # Decodificar nome do arquivo se necessário
                        decoded_filename = self._decode_filename(filename)
                        if self._is_pdf_file(decoded_filename):
                            return True
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar anexos PDF: {e}")
            return False
    
    def extract_pdf_attachments(self, email_message: email.message.Message, 
                               email_id: str) -> List[Tuple[str, str]]:
        """
        Extrai anexos PDF do e-mail e salva localmente.
        
        Args:
            email_message: Objeto do e-mail
            email_id: ID do e-mail para identificação
            
        Returns:
            List[Tuple[str, str]]: Lista de tuplas (nome_arquivo, caminho_salvo)
        """
        saved_files = []
        
        try:
            for part in email_message.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        # Decodificar nome do arquivo
                        decoded_filename = self._decode_filename(filename)
                        
                        if self._is_pdf_file(decoded_filename):
                            # Verificar tamanho do arquivo
                            file_size = len(part.get_payload(decode=True))
                            if file_size > self.max_file_size:
                                logger.warning(f"Arquivo {decoded_filename} muito grande ({file_size} bytes), ignorando")
                                continue
                            
                            # Gerar nome único para o arquivo
                            unique_filename = self._generate_unique_filename(decoded_filename, email_id)
                            file_path = self.download_folder / unique_filename
                            
                            # Salvar arquivo
                            with open(file_path, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            
                            saved_files.append((decoded_filename, str(file_path)))
                            logger.info(f"PDF salvo: {file_path}")
            
            return saved_files
            
        except Exception as e:
            logger.error(f"Erro ao extrair anexos PDF: {e}")
            return saved_files
    
    def _decode_filename(self, filename: str) -> str:
        """
        Decodifica o nome do arquivo se necessário.
        
        Args:
            filename: Nome do arquivo codificado
            
        Returns:
            str: Nome do arquivo decodificado
        """
        try:
            from email.header import decode_header
            decoded_parts = decode_header(filename)
            decoded_filename = ""
            
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        decoded_filename += part.decode(encoding)
                    else:
                        decoded_filename += part.decode('utf-8', errors='ignore')
                else:
                    decoded_filename += part
            
            return decoded_filename
        except Exception as e:
            logger.error(f"Erro ao decodificar nome do arquivo {filename}: {e}")
            return filename
    
    def _is_pdf_file(self, filename: str) -> bool:
        """
        Verifica se o arquivo é um PDF baseado na extensão.
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            bool: True se é PDF, False caso contrário
        """
        if not filename:
            return False
        
        # Verificar extensão
        file_extension = Path(filename).suffix.lower()
        if file_extension in self.allowed_extensions:
            return True
        
        # Verificar tipo MIME se disponível
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type == 'application/pdf':
            return True
        
        return False
    
    def _generate_unique_filename(self, original_filename: str, email_id: str) -> str:
        """
        Gera um nome único para o arquivo para evitar conflitos.
        
        Args:
            original_filename: Nome original do arquivo
            email_id: ID do e-mail
            
        Returns:
            str: Nome único do arquivo
        """
        try:
            # Extrair nome e extensão
            file_path = Path(original_filename)
            name = file_path.stem
            extension = file_path.suffix
            
            # Adicionar timestamp e ID do e-mail para unicidade
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_name = f"{name}_{email_id}_{timestamp}{extension}"
            
            # Limitar tamanho do nome do arquivo
            if len(unique_name) > 200:
                unique_name = f"{name[:50]}_{email_id}_{timestamp}{extension}"
            
            return unique_name
            
        except Exception as e:
            logger.error(f"Erro ao gerar nome único para {original_filename}: {e}")
            # Fallback: usar timestamp e ID do e-mail
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"pdf_{email_id}_{timestamp}.pdf"
    
    def get_attachment_info(self, email_message: email.message.Message) -> List[dict]:
        """
        Obtém informações sobre todos os anexos do e-mail.
        
        Args:
            email_message: Objeto do e-mail
            
        Returns:
            List[dict]: Lista de informações dos anexos
        """
        attachments_info = []
        
        try:
            for part in email_message.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        decoded_filename = self._decode_filename(filename)
                        file_size = len(part.get_payload(decode=True))
                        
                        attachment_info = {
                            'filename': decoded_filename,
                            'size_bytes': file_size,
                            'size_mb': round(file_size / (1024 * 1024), 2),
                            'is_pdf': self._is_pdf_file(decoded_filename)
                        }
                        attachments_info.append(attachment_info)
            
            return attachments_info
            
        except Exception as e:
            logger.error(f"Erro ao obter informações dos anexos: {e}")
            return attachments_info
