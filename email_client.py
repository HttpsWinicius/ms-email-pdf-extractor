"""
Módulo para conexão e operações com e-mail via IMAP.
"""
import imaplib
import email.message
import logging
from typing import List, Tuple, Optional
from email.header import decode_header
import ssl

from config import EMAIL_CONFIG, EMAIL_CREDENTIALS

logger = logging.getLogger(__name__)


class EmailClient:
    """Cliente para operações com e-mail via IMAP."""
    
    def __init__(self):
        self.imap_client: Optional[imaplib.IMAP4_SSL] = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Estabelece conexão com o servidor de e-mail.
        
        Returns:
            bool: True se a conexão foi bem-sucedida, False caso contrário
        """
        try:
            logger.info(f"Conectando ao servidor IMAP: {EMAIL_CONFIG['imap_server']}")
            
            # Criar contexto SSL seguro
            context = ssl.create_default_context()
            
            # Conectar ao servidor IMAP
            self.imap_client = imaplib.IMAP4_SSL(
                EMAIL_CONFIG['imap_server'],
                EMAIL_CONFIG['imap_port'],
                ssl_context=context
            )
            
            # Fazer login
            self.imap_client.login(
                EMAIL_CREDENTIALS['email'],
                EMAIL_CREDENTIALS['password']
            )
            
            # Selecionar caixa de entrada
            self.imap_client.select('INBOX')
            
            self.connected = True
            logger.info("Conexão com e-mail estabelecida com sucesso")
            return True
            
        except imaplib.IMAP4.error as e:
            logger.error(f"Erro de autenticação IMAP: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro ao conectar com o e-mail: {e}")
            return False
    
    def disconnect(self) -> None:
        """Fecha a conexão com o servidor de e-mail."""
        if self.imap_client and self.connected:
            try:
                self.imap_client.close()
                self.imap_client.logout()
                self.connected = False
                logger.info("Conexão com e-mail encerrada")
            except Exception as e:
                logger.error(f"Erro ao desconectar: {e}")
    
    def get_unread_emails(self) -> List[str]:
        """
        Busca e-mails não lidos na caixa de entrada.
        
        Returns:
            List[str]: Lista de IDs dos e-mails não lidos
        """
        if not self.connected or not self.imap_client:
            logger.error("Cliente não conectado")
            return []
        
        try:
            # Buscar e-mails não lidos
            status, messages = self.imap_client.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.error("Erro ao buscar e-mails não lidos")
                return []
            
            email_ids = messages[0].split()
            logger.info(f"Encontrados {len(email_ids)} e-mails não lidos")
            
            # Limitar quantidade de e-mails por verificação
            max_emails = EMAIL_CONFIG['max_emails_per_check']
            if len(email_ids) > max_emails:
                email_ids = email_ids[-max_emails:]  # Pegar os mais recentes
                logger.info(f"Limitando a {max_emails} e-mails mais recentes")
            
            return [email_id.decode() for email_id in email_ids]
            
        except Exception as e:
            logger.error(f"Erro ao buscar e-mails não lidos: {e}")
            return []
    
    def get_email_content(self, email_id: str) -> Optional[email.message.Message]:
        """
        Obtém o conteúdo de um e-mail específico.
        
        Args:
            email_id: ID do e-mail
            
        Returns:
            email.message.Message: Objeto do e-mail ou None se houver erro
        """
        if not self.connected or not self.imap_client:
            logger.error("Cliente não conectado")
            return None
        
        try:
            status, msg_data = self.imap_client.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                logger.error(f"Erro ao buscar e-mail {email_id}")
                return None
            
            # Decodificar o e-mail
            raw_email = msg_data[0][1]
            email_message = email.message.message_from_bytes(raw_email)
            
            return email_message
            
        except Exception as e:
            logger.error(f"Erro ao obter conteúdo do e-mail {email_id}: {e}")
            return None
    
    def mark_as_read(self, email_id: str) -> bool:
        """
        Marca um e-mail como lido.
        
        Args:
            email_id: ID do e-mail
            
        Returns:
            bool: True se marcado com sucesso, False caso contrário
        """
        if not self.connected or not self.imap_client:
            logger.error("Cliente não conectado")
            return False
        
        try:
            # Marcar como lido (remover flag UNSEEN)
            self.imap_client.store(email_id, '-FLAGS', '\\Seen')
            logger.info(f"E-mail {email_id} marcado como lido")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao marcar e-mail {email_id} como lido: {e}")
            return False
    
    def get_email_subject(self, email_message: email.message.Message) -> str:
        """
        Extrai o assunto do e-mail, decodificando se necessário.
        
        Args:
            email_message: Objeto do e-mail
            
        Returns:
            str: Assunto do e-mail
        """
        try:
            subject = email_message['Subject']
            if subject:
                # Decodificar header se necessário
                decoded_subject = decode_header(subject)[0]
                if isinstance(decoded_subject[0], bytes):
                    return decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
                return decoded_subject[0]
            return "Sem assunto"
        except Exception as e:
            logger.error(f"Erro ao extrair assunto: {e}")
            return "Erro ao extrair assunto"
    
    def get_email_sender(self, email_message: email.message.Message) -> str:
        """
        Extrai o remetente do e-mail.
        
        Args:
            email_message: Objeto do e-mail
            
        Returns:
            str: Remetente do e-mail
        """
        try:
            sender = email_message['From']
            return sender if sender else "Remetente desconhecido"
        except Exception as e:
            logger.error(f"Erro ao extrair remetente: {e}")
            return "Erro ao extrair remetente"
