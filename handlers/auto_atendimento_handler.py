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

    logger.info(f"Usuário {user_id} no estado {current_state} selecionou a opção: {text}")

    if current_state == 'auto_atendimento':
        if text == '1' or text == 'vivo':
            logger.info(f"Atualizando estado do usuário {user_id} para 'auto_atendimento_vivo'")
            user_state[user_id] = 'auto_atendimento_vivo'
            logger.info(f"Chamando a função vivo_auto_atendimento para o usuário {user_id}")
            await vivo_auto_atendimento(event)
        elif text == '2' or text == 'tim':
            logger.info(f"Atualizando estado do usuário {user_id} para 'auto_atendimento_tim'")
            user_state[user_id] = 'auto_atendimento_tim'
            logger.info(f"Chamando a função tim_auto_atendimento para o usuário {user_id}")
            await tim_auto_atendimento(event)
        elif text == '3' or text == 'claro':
            logger.info(f"Atualizando estado do usuário {user_id} para 'auto_atendimento_claro'")
            user_state[user_id] = 'auto_atendimento_claro'
            logger.info(f"Chamando a função claro_auto_atendimento para o usuário {user_id}")
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
        logger.info(f"Usuário {user_id} está no estado 'auto_atendimento_vivo' e enviou: {text}")
        if text == 'voltar' or text == 'menu':
            user_state[user_id] = 'auto_atendimento'
            logger.info(f"Estado do usuário {user_id} atualizado para 'auto_atendimento'")
            await auto_atendimento_menu(event)
        else:
            await handle_vivo_auto_atendimento(event, text, user_state)
    elif current_state == 'auto_atendimento_tim':
        logger.info(f"Usuário {user_id} está no estado 'auto_atendimento_tim' e enviou: {text}")
        if text == 'voltar' or text == 'menu':
            user_state[user_id] = 'auto_atendimento'
            logger.info(f"Estado do usuário {user_id} atualizado para 'auto_atendimento'")
            await auto_atendimento_menu(event)
        else:
            await handle_tim_auto_atendimento(event, text, user_state)
    elif current_state == 'auto_atendimento_claro':
        logger.info(f"Usuário {user_id} está no estado 'auto_atendimento_claro' e enviou: {text}")
        if text == 'voltar' or text == 'menu':
            user_state[user_id] = 'auto_atendimento'
            logger.info(f"Estado do usuário {user_id} atualizado para 'auto_atendimento'")
            await auto_atendimento_menu(event)
        else:
            await handle_claro_auto_atendimento(event, text, user_state)

async def vivo_auto_atendimento(event):
    logger.info("Vivo Auto Atendimento ativado")
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
    logger.info("TIM Auto Atendimento ativado")
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
    logger.info("Claro Auto Atendimento ativado")
    await event.reply(
        "💬 **Auto Atendimento Claro** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Não Gera Dados**\n\n"
        "🔙 **Escreva `Voltar` para retornar ao menu anterior**",
        parse_mode='md'
    )
