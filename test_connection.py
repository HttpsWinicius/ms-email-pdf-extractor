#!/usr/bin/env python3
"""
Script de teste para verificar a conexão com Gmail.
Use este script para testar suas credenciais antes de executar o serviço principal.
"""
import sys
from config import EMAIL_CREDENTIALS, validate_config
from email_client import EmailClient
from logger_config import setup_colored_logging

# Configurar logging
logger = setup_colored_logging()


def test_email_connection():
    """Testa a conexão com Gmail."""
    logger.info("🧪 Iniciando teste de conexão com Gmail")
    
    # Validar configurações
    if not validate_config():
        logger.error("❌ Configurações inválidas!")
        logger.error("   Verifique se você preencheu email e password em config.py")
        return False
    
    logger.info(f"📧 Testando conexão com: {EMAIL_CREDENTIALS['email']}")
    
    # Criar cliente de e-mail
    email_client = EmailClient()
    
    try:
        # Tentar conectar
        if email_client.connect():
            logger.info("✅ Conexão estabelecida com sucesso!")
            
            # Testar busca de e-mails
            unread_emails = email_client.get_unread_emails()
            logger.info(f"📬 E-mails não lidos encontrados: {len(unread_emails)}")
            
            # Desconectar
            email_client.disconnect()
            logger.info("✅ Teste concluído com sucesso!")
            return True
        else:
            logger.error("❌ Falha na conexão!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro durante o teste: {e}")
        return False


def main():
    """Função principal do teste."""
    logger.info("=" * 50)
    logger.info("🔧 TESTE DE CONEXÃO GMAIL")
    logger.info("=" * 50)
    
    success = test_email_connection()
    
    logger.info("=" * 50)
    if success:
        logger.info("🎉 TESTE PASSOU! Você pode executar o serviço principal.")
        logger.info("   Execute: python main.py")
    else:
        logger.error("💥 TESTE FALHOU! Verifique suas configurações.")
        logger.error("   Dicas:")
        logger.error("   1. Verifique se o e-mail está correto")
        logger.error("   2. Use uma senha de app do Gmail (não a senha normal)")
        logger.error("   3. Ative a verificação em 2 etapas")
        logger.error("   4. Gere uma senha de app em: https://myaccount.google.com/apppasswords")
    logger.info("=" * 50)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
