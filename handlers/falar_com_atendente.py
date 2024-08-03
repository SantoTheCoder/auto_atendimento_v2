#falar_com_atendente.py
import logging
import asyncio
from telethon.tl.types import PeerChannel
from datetime import datetime

logger = logging.getLogger(__name__)

atendimento_ativo = {}
atendimentos_ativos_contagem = 0
atendimento_confirmacao = {}
atendimento_cliente_mensagem = {}
atendimento_auto_off = set()  # Usando um conjunto para rastrear chats com atendimento automático desligado
CANAL_LOG_ID = -1002203568072  # Substitua pelo ID do seu canal
user_state = {}  # Adicionando user_state aqui

async def enviar_mensagem_canal(client, mensagem):
    if CANAL_LOG_ID:
        await client.send_message(PeerChannel(CANAL_LOG_ID), mensagem)

async def falar_com_atendente(event):
    chat_id = event.chat_id

    if chat_id not in atendimento_ativo:
        atendimento_confirmacao[chat_id] = True
        await event.reply(
            "📞 **Falar com Atendente** 📞\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔹 **Nosso autoatendimento resolve 90% das dúvidas!**\n\n"
            "📝 **Para conferir nosso autoatendimento, escreva** **`Menu`** **e selecione a opção** **`5`**.\n\n"
            "👥 **Para falar com um atendente, escreva** **`SIM`**.",
            parse_mode='md'
        )

async def handle_atendimento_confirmacao(event):
    global atendimentos_ativos_contagem
    chat_id = event.chat_id
    user = await event.get_sender()
    text = event.raw_text.lower()

    if text == 'menu':
        await encerrar_atendimento(event)
        await event.reply(
            "📋 **Menu Principal** 📋\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Digite uma das opções abaixo para saber mais:\n\n"
            "1️⃣ **Como Funciona**\n"
            "2️⃣ **Comprar**\n"
            "3️⃣ **Revender**\n"
            "4️⃣ **iOS**\n"
            "5️⃣ **Auto Atendimento**\n"
            "6️⃣ **Falar com Atendente**",
            parse_mode='md'
        )
        return

    if chat_id in atendimento_confirmacao and text == 'sim':
        atendimento_confirmacao.pop(chat_id)
        atendimento_ativo[chat_id] = True
        atendimento_cliente_mensagem[chat_id] = True
        atendimentos_ativos_contagem += 1
        logger.info(f"Chat {chat_id} entrou em atendimento. Total de atendimentos ativos: {atendimentos_ativos_contagem}")
        await event.reply(
            "📸 **Por favor, descreva seu problema e, se possível, envie fotos ou vídeos para ajudar no suporte.** Seja o mais completo possível, assim facilitará nosso suporte. 😊📷📹",
            parse_mode='md'
        )
        mensagem_canal = (
            f"👤 **Atendimento Iniciado**\n"
            f"Chat ID: {chat_id}\n"
            f"Usuário: {user.first_name} (@{user.username})\n"
            f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Posição na fila: {atendimentos_ativos_contagem}"
        )
        await enviar_mensagem_canal(event.client, mensagem_canal)
        await aguardar_mensagens_cliente(event, chat_id)
    elif text == 'menu':
        atendimento_confirmacao.pop(chat_id, None)  # Remove o estado de confirmação
        await event.reply(
            "📋 **Menu Principal** 📋\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Digite uma das opções abaixo para saber mais:\n\n"
            "1️⃣ **Como Funciona**\n"
            "2️⃣ **Comprar**\n"
            "3️⃣ **Revender**\n"
            "4️⃣ **iOS**\n"
            "5️⃣ **Auto Atendimento**\n"
            "6️⃣ **Falar com Atendente**",
            parse_mode='md'
        )

async def aguardar_mensagens_cliente(event, chat_id):
    while chat_id in atendimento_cliente_mensagem:
        atendimento_cliente_mensagem[chat_id] = False  # Reseta a flag para aguardar nova mensagem
        await asyncio.sleep(60)  # Aguarda 1 minuto

        # Verifica se uma nova mensagem foi recebida
        if not atendimento_cliente_mensagem[chat_id]:
            posicao = list(atendimento_ativo.keys()).index(chat_id) + 1
            await event.reply(
                f"**SUPORTE A CAMINHO 🚒🚒🚒**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "📨 **Informações recebidas.**\n\n"
                f"Você está na posição **{posicao}** na fila de atendimento. O suporte retornará em breve.",
                parse_mode='md'
            )
            break  # Encerra o loop após enviar a mensagem de confirmação

async def encerrar_atendimento(event):
    global atendimentos_ativos_contagem
    chat_id = event.chat_id
    user = await event.get_sender()

    logger.info(f"Iniciando o encerramento do atendimento para o chat {chat_id}")

    # Reseta todos os estados de atendimento, independentemente de serem ativos ou não.
    if chat_id in atendimento_ativo:
        atendimento_ativo.pop(chat_id)
        atendimentos_ativos_contagem -= 1
        logger.info(f"Atendimento ativo encerrado para o chat {chat_id}. Total de atendimentos ativos: {atendimentos_ativos_contagem}")

    if chat_id in atendimento_confirmacao:
        atendimento_confirmacao.pop(chat_id)
        logger.info(f"Atendimento em confirmação encerrado para o chat {chat_id}.")

    if chat_id in atendimento_auto_off:
        atendimento_auto_off.remove(chat_id)
        logger.info(f"Auto atendimento desativado removido para o chat {chat_id}.")

    user_state.pop(chat_id, None)  # Resetar o estado do usuário
    logger.info(f"Estado do usuário resetado para o chat {chat_id}")

    # Enviar mensagem de confirmação
    await event.reply(
        "🔚 **Atendimento encerrado pelo suporte.** 🔚\n"
        "Obrigado por utilizar nosso serviço. Se precisar de mais ajuda, não hesite em nos contatar novamente.",
        parse_mode='md'
    )

    # Enviar log ao canal
    mensagem_canal = (
        f"👤 **Atendimento Encerrado**\n"
        f"Chat ID: {chat_id}\n"
        f"Usuário: {user.first_name} (@{user.username})\n"
        f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Total de atendimentos ativos: {atendimentos_ativos_contagem}"
    )
    await enviar_mensagem_canal(event.client, mensagem_canal)

async def handle_message(event):
    chat_id = event.chat_id
    text = event.raw_text.lower()

    if chat_id in atendimento_confirmacao:
        await handle_atendimento_confirmacao(event)
    elif chat_id in atendimento_ativo:
        # Permitir que o usuário envie mensagens livremente enquanto está em atendimento
        logger.info(f"Mensagem de {chat_id} em atendimento: {text}")
        atendimento_cliente_mensagem[chat_id] = True  # Reset the timer
    elif text == 'falar com atendente' or text == '6':
        await falar_com_atendente(event)
    elif text == '/encerrar':
        logger.info(f"Comando /encerrar recebido de {chat_id}")
        await encerrar_atendimento(event)
    elif text == 'menu':
        if chat_id in atendimento_auto_off:
            atendimento_auto_off.remove(chat_id)
        await event.reply(
            "📋 **Menu Principal** 📋\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Digite uma das opções abaixo para saber mais:\n\n"
            "1️⃣ **Como Funciona**\n"
            "2️⃣ **Comprar**\n"
            "3️⃣ **Revender**\n"
            "4️⃣ **iOS**\n"
            "5️⃣ **Auto Atendimento**\n"
            "6️⃣ **Falar com Atendente**",
            parse_mode='md'
        )
