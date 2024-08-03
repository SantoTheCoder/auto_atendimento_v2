#auto_atendimento_handler.py
import logging
from handlers.vivo_handler import vivo_auto_atendimento, handle_vivo_auto_atendimento
from handlers.tim_handler import tim_auto_atendimento, handle_tim_auto_atendimento
from handlers.claro_handler import claro_auto_atendimento, handle_claro_auto_atendimento

logger = logging.getLogger(__name__)

async def auto_atendimento_menu(event):
    await event.reply(
        "💬 **Auto Atendimento** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Aqui estão as opções mais comuns de suporte, resolvendo 90% das dúvidas! Selecione sua operadora:\n\n"
        "1️⃣ **VIVO**\n"
        "2️⃣ **TIM**\n"
        "3️⃣ **CLARO**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 **Digite `Menu` para solicitar o menu de alternativas novamente**",
        parse_mode='md'
    )

async def handle_auto_atendimento_event(event, text, user_state):
    user_id = event.sender_id
    current_state = user_state.get(user_id, 'menu_principal')

    if current_state == 'auto_atendimento':
        if text == '1' or text == 'vivo':
            user_state[user_id] = 'auto_atendimento_vivo'
            await vivo_auto_atendimento(event)
        elif text == '2' or text == 'tim':
            user_state[user_id] = 'auto_atendimento_tim'
            await tim_auto_atendimento(event)
        elif text == '3' or text == 'claro':
            user_state[user_id] = 'auto_atendimento_claro'
            await claro_auto_atendimento(event)
        elif text == 'voltar' or text == 'menu':
            await auto_atendimento_menu(event)
        else:
            await event.reply(
                "⚠️ **Opção inválida. Por favor, selecione uma das opções do menu de autoatendimento.**\n\n"
                "🔙 **Escreva `Voltar` para retornar ao menu anterior**",
                parse_mode='md'
            )
    elif current_state == 'auto_atendimento_vivo':
        if text == 'voltar' or text == 'menu':
            user_state[user_id] = 'auto_atendimento'
            await auto_atendimento_menu(event)
        else:
            await handle_vivo_auto_atendimento(event, text, user_state)
    elif current_state == 'auto_atendimento_tim':
        if text == 'voltar' or text == 'menu':
            user_state[user_id] = 'auto_atendimento'
            await auto_atendimento_menu(event)
        else:
            await handle_tim_auto_atendimento(event, text, user_state)
    elif current_state == 'auto_atendimento_claro':
        if text == 'voltar' or text == 'menu':
            user_state[user_id] = 'auto_atendimento'
            await auto_atendimento_menu(event)
        else:
            await handle_claro_auto_atendimento(event, text, user_state)

async def vivo_auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento Vivo** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Conecta, mas não Funciona**\n\n"
        "🔙 **Escreva `Voltar` para retornar ao menu anterior**",
        parse_mode='md'
    )

async def tim_auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento TIM** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Conecta, mas não Gera Dados**\n\n"
        "🔙 **Escreva `Voltar` para retornar ao menu anterior**",
        parse_mode='md'
    )

async def claro_auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento Claro** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Não Gera Dados**\n\n"
        "🔙 **Escreva `Voltar` para retornar ao menu anterior**",
        parse_mode='md'
    )
