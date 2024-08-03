#keyboards.py utils
from telethon import Button
import logging

logger = logging.getLogger(__name__)

def main_menu_keyboard():
    logger.info("Criando teclado do menu principal")
    return [
        [Button.inline("1. Como Funciona", b'como_funciona')],
        [Button.inline("2. Comprar", b'comprar')],
        [Button.inline("3. Revender", b'revender')],
        [Button.inline("4. iOS", b'ios')],
        [Button.inline("5. Auto Atendimento", b'auto_atendimento')],
        [Button.inline("6. Falar com Atendente", b'falar_com_atendente')]
    ]

def back_to_menu_keyboard():
    logger.info("Criando botão para voltar ao menu principal")
    return [Button.inline("Voltar ao Menu Principal", b'menu_principal')]
