#!/usr/bin/env python3
"""
Serviço de monitoramento de e-mail para extração de PDFs.
Monitora uma conta Gmail e baixa anexos PDF automaticamente.
"""
import time
import signal
import sys
from typing import Optional

from config import EMAIL_CONFIG, validate_config, create_download_folder
from email_client import EmailClient
from pdf_extractor import PDFExtractor
from logger_config import setup_colored_logging

# Configurar logging
logger = setup_colored_logging()


class EmailPDFMonitor:
    """Monitor principal para extração de PDFs de e-mails."""
    
    def __init__(self):
        self.email_client = EmailClient()
        self.pdf_extractor = PDFExtractor()
        self.running = False
        self.processed_emails = set()  # Para evitar processar o mesmo e-mail
        
    def start_monitoring(self) -> None:
        """Inicia o monitoramento contínuo de e-mails."""
        logger.info("🚀 Iniciando serviço de monitoramento de e-mail")
        
        # Validar configurações
        if not validate_config():
            logger.error("❌ Configurações inválidas. Verifique email e senha em config.py")
            return
        
        # Criar pasta de download
        create_download_folder()
        logger.info(f"📁 Pasta de download: {EMAIL_CONFIG['download_folder']}")
        
        # Conectar ao e-mail
        if not self.email_client.connect():
            logger.error("❌ Falha ao conectar com o e-mail")
            return
        
        self.running = True
        logger.info("✅ Serviço iniciado com sucesso!")
        logger.info(f"⏰ Verificando e-mails a cada {EMAIL_CONFIG['check_interval']} segundos")
        logger.info("🛑 Pressione Ctrl+C para parar o serviço")
        
        try:
            while self.running:
                self._check_for_new_emails()
                time.sleep(EMAIL_CONFIG['check_interval'])
                
        except KeyboardInterrupt:
            logger.info("🛑 Interrupção detectada pelo usuário")
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
        finally:
            self._cleanup()
    
    def _check_for_new_emails(self) -> None:
        """Verifica e processa novos e-mails com anexos PDF."""
        try:
            # Buscar e-mails não lidos
            unread_email_ids = self.email_client.get_unread_emails()
            
            if not unread_email_ids:
                logger.debug("📭 Nenhum e-mail não lido encontrado")
                return
            
            logger.info(f"📧 Encontrados {len(unread_email_ids)} e-mails não lidos")
            
            # Processar cada e-mail
            for email_id in unread_email_ids:
                if email_id in self.processed_emails:
                    continue
                
                self._process_email(email_id)
                self.processed_emails.add(email_id)
                
        except Exception as e:
            logger.error(f"❌ Erro ao verificar e-mails: {e}")
    
    def _process_email(self, email_id: str) -> None:
        """
        Processa um e-mail específico.
        
        Args:
            email_id: ID do e-mail
        """
        try:
            email_message = self.email_client.get_email_content(email_id)
            print(email_message)
            if not email_message:
                logger.warning(f"⚠️ Não foi possível obter conteúdo do e-mail {email_id}")
                return
            
            # Obter informações do e-mail
            subject = self.email_client.get_email_subject(email_message)
            sender = self.email_client.get_email_sender(email_message)
            
            logger.info(f"📨 Processando e-mail: {subject[:50]}...")
            logger.info(f"👤 De: {sender}")
            
            # Verificar se tem anexos PDF
            if not self.pdf_extractor.has_pdf_attachments(email_message):
                logger.info("📄 E-mail não possui anexos PDF, marcando como lido")
                self.email_client.mark_as_read(email_id)
                return
            
            # Obter informações dos anexos
            attachments_info = self.pdf_extractor.get_attachment_info(email_message)
            pdf_attachments = [att for att in attachments_info if att['is_pdf']]
            
            logger.info(f"📎 Encontrados {len(pdf_attachments)} anexos PDF:")
            for att in pdf_attachments:
                logger.info(f"   📄 {att['filename']} ({att['size_mb']} MB)")
            
            # Extrair PDFs
            saved_files = self.pdf_extractor.extract_pdf_attachments(email_message, email_id)
            
            if saved_files:
                logger.info(f"✅ {len(saved_files)} PDF(s) extraído(s) com sucesso:")
                for original_name, saved_path in saved_files:
                    logger.info(f"   💾 Salvo em: {saved_path}")
            else:
                logger.warning("⚠️ Nenhum PDF foi extraído")
            
            # Marcar e-mail como lido
            if self.email_client.mark_as_read(email_id):
                logger.info("✅ E-mail marcado como lido")
            else:
                logger.warning("⚠️ Falha ao marcar e-mail como lido")
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar e-mail {email_id}: {e}")
    
    def _cleanup(self) -> None:
        """Limpa recursos antes de encerrar."""
        logger.info("🧹 Encerrando serviço...")
        self.email_client.disconnect()
        self.running = False
        logger.info("👋 Serviço encerrado")
    
    def stop(self) -> None:
        """Para o monitoramento."""
        self.running = False


def signal_handler(signum, frame):
    """Handler para sinais do sistema (Ctrl+C)."""
    logger.info("🛑 Sinal de interrupção recebido")
    sys.exit(0)



def main():
    """Função principal."""
    # Configurar handler para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Criar e iniciar monitor
    monitor = EmailPDFMonitor()
    
    try:
        monitor.start_monitoring()
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
