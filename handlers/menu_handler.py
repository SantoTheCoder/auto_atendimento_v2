#menu_handler.py
import logging
from handlers.como_funciona import como_funciona
from handlers.comprar import comprar
from handlers.revender import revender
from handlers.ios import ios
from handlers.falar_com_atendente import falar_com_atendente

logger = logging.getLogger(__name__)

async def handle_option(event, text):
    user_id = event.sender_id
    logger.info(f"Opção selecionada pelo usuário {user_id}: {text}")

    if text == '1' or text == 'como funciona':
        await como_funciona(event)
    elif text == '2' or text == 'comprar':
        await comprar(event)
    elif text == '3' or text == 'revender':
        await revender(event)
    elif text == '4' or text == 'ios':
        await ios(event)
    elif text == '6' or text == 'falar com atendente':
        await falar_com_atendente(event)
    else:
        await event.reply(
            "⚠️ **Opção inválida**. Por favor, digite uma das opções abaixo:\n\n"
            "1️⃣ **Como Funciona**\n"
            "2️⃣ **Comprar**\n"
            "3️⃣ **Revender**\n"
            "4️⃣ **iOS**\n"
            "5️⃣ **Auto Atendimento**\n"
            "6️⃣ **Falar com Atendente**\n",
            parse_mode='md'
        )
