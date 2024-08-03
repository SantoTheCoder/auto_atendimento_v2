import logging
import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH
from handlers.menu_handler import handle_option
from handlers.auto_atendimento_handler import auto_atendimento_menu, handle_auto_atendimento_event
from handlers.falar_com_atendente import falar_com_atendente, encerrar_atendimento, handle_message, handle_atendimento_confirmacao, atendimento_ativo, atendimento_confirmacao, atendimento_auto_off, CANAL_LOG_ID, user_state
from datetime import datetime, timedelta
import requests
from collections import deque
from keywords import keywords

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome do arquivo de sessão
SESSION_NAME = 'netdez_session'

last_menu_time = {}
last_message_time = {}
atendimentos_ativos_contagem = 0  # Contagem de atendimentos ativos
CANAL_LOG_ID = -1002203568072  # Substitua pelo ID do seu canal

# Filtro Anti-Spam: Limite de 10 mensagens em 10 segundos
MESSAGE_LIMIT = 10
TIME_WINDOW = 10  # segundos
user_messages = {}

# Função para verificar se o IP é brasileiro
def is_brazilian_ip():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        country = data.get('country')
        return country == 'BR'
    except Exception as e:
        logger.error(f"Erro ao verificar o IP: {e}")
        return False

if is_brazilian_ip():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    @client.on(events.NewMessage)
    async def handle_message_event(event):
        # Ignorar mensagens de grupos, canais e bots
        sender = await event.get_sender()
        if event.is_group or event.is_channel or (sender and sender.bot):
            logger.info(f"Ignorando mensagem de grupo/canal/bot: {event.chat_id}")
            return

        chat_id = event.chat_id
        text = event.raw_text.lower()

        # Filtro Anti-Spam
        current_time = datetime.now()
        if chat_id not in user_messages:
            user_messages[chat_id] = deque(maxlen=MESSAGE_LIMIT)

        user_messages[chat_id].append(current_time)

        # Remover mensagens que estão fora do intervalo de tempo
        while user_messages[chat_id] and (current_time - user_messages[chat_id][0]).total_seconds() > TIME_WINDOW:
            user_messages[chat_id].popleft()

        # Verificar se o usuário excedeu o limite de mensagens
        if len(user_messages[chat_id]) == MESSAGE_LIMIT:
            logger.warning(f"Usuário {chat_id} excedeu o limite de mensagens. Ignorando mensagens por um tempo.")
            await event.reply("🚫 **Você está enviando mensagens muito rapidamente. Por favor, aguarde um pouco antes de enviar mais mensagens.**")
            return

        logger.info(f"Mensagem recebida de {chat_id}: {text}")

        last_time = last_message_time.get(chat_id, current_time)
        last_message_time[chat_id] = current_time

        # Verificar se é a primeira mensagem do usuário
        if chat_id not in user_state:
            user_state[chat_id] = 'menu_principal'
            user = await event.get_sender()
            logger.info(f"Enviando mensagem de boas-vindas para {chat_id} na primeira interação")
            await event.reply(
                f"👋 **Bem-vindo(a), {user.first_name}!**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Abaixo, apresentamos as perguntas mais comuns que recebemos, para que possamos informar você no momento.\n\n"
                "ℹ️ **Nota:** Nosso auto-suporte resolve 90% dos problemas. Basta acessar a opção de suporte.\n\n"
                "**Digite uma das opções abaixo para saber mais:**\n\n"
                "1️⃣ **Como Funciona**\n"
                "2️⃣ **Comprar**\n"
                "3️⃣ **Revender**\n"
                "4️⃣ **iOS**\n"
                "5️⃣ **Auto Atendimento**\n"
                "6️⃣ **Falar com Atendente**",
                parse_mode='md'
            )
            return

        # Enviar menu principal se a última mensagem foi enviada há mais de 48 horas
        if current_time - last_time > timedelta(hours=48):
            user_state[chat_id] = 'menu_principal'
            user = await event.get_sender()
            logger.info(f"Enviando mensagem de boas-vindas para {chat_id} após período de inatividade")
            await event.reply(
                f"👋 **Bem-vindo(a) novamente, {user.first_name}!**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Abaixo, apresentamos as perguntas mais comuns que recebemos, para que possamos informar você no momento.\n\n"
                "ℹ️ **Nota:** Nosso auto-suporte resolve 90% dos problemas. Basta acessar a opção de suporte.\n\n"
                "**Digite uma das opções abaixo para saber mais:**\n\n"
                "1️⃣ **Como Funciona**\n"
                "2️⃣ **Comprar**\n"
                "3️⃣ **Revender**\n"
                "4️⃣ **iOS**\n"
                "5️⃣ **Auto Atendimento**\n"
                "6️⃣ **Falar com Atendente**",
                parse_mode='md'
            )
            return

        # Verificar palavras-chave específicas para saudações, se o auto_atendimento não estiver desativado
        if any(keyword in text for keyword in keywords) and chat_id not in atendimento_auto_off and chat_id not in atendimento_ativo:
            user_state[chat_id] = 'menu_principal'
            user = await event.get_sender()
            logger.info(f"Enviando mensagem de boas-vindas para {chat_id} em resposta a saudação")
            await event.reply(
                f"👋 **Olá, {user.first_name}!**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Aqui está o menu principal para você:\n\n"
                "ℹ️ **Nota:** Nosso auto-suporte resolve 90% dos problemas. Basta acessar a opção de suporte.\n\n"
                "**Digite uma das opções abaixo para saber mais:**\n\n"
                "1️⃣ **Como Funciona**\n"
                "2️⃣ **Comprar**\n"
                "3️⃣ **Revender**\n"
                "4️⃣ **iOS**\n"
                "5️⃣ **Auto Atendimento**\n"
                "6️⃣ **Falar com Atendente**",
                parse_mode='md'
            )
            return

        if text == 'menu':
            if chat_id in atendimento_ativo or chat_id in atendimento_confirmacao:
                await encerrar_atendimento(event)
            if chat_id in atendimento_auto_off:
                atendimento_auto_off.remove(chat_id)
            user_state[chat_id] = 'menu_principal'
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
        elif text == '/encerrar':
            logger.info(f"Comando /encerrar recebido de {chat_id}")
            # Reseta o estado e remove o atendimento de qualquer lista de atendimento ativo
            user_state.pop(chat_id, None)
            if chat_id in atendimento_auto_off:
                atendimento_auto_off.remove(chat_id)
            if chat_id in atendimento_ativo:
                atendimento_ativo.pop(chat_id, None)
            if chat_id in atendimento_confirmacao:
                atendimento_confirmacao.pop(chat_id, None)
            await event.reply(
                "🔚 **Atendimento encerrado pelo suporte.** 🔚\n",
                parse_mode='md'
            )
            await event.reply(
                "👍 **Obrigado por utilizar nosso serviço. Se precisar de mais ajuda, não hesite em nos contatar novamente.**",
                parse_mode='md'
            )
        elif chat_id in atendimento_auto_off:
            # Auto atendimento desativado para este chat
            return
        elif chat_id in atendimento_ativo:
            # Permitir que o usuário envie mensagens livremente enquanto está em atendimento
            await handle_message(event)
        elif chat_id in atendimento_confirmacao:
            await handle_atendimento_confirmacao(event)
        elif text == '/start':
            user_state[chat_id] = 'menu_principal'
            user = await event.get_sender()
            logger.info(f"Enviando mensagem de boas-vindas para {chat_id}")
            await event.reply(
                f"👋 **Bem-vindo(a), {user.first_name}!**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Abaixo, apresentamos as perguntas mais comuns que recebemos, para que possamos informar você no momento.\n\n"
                "ℹ️ **Nota:** Nosso auto-suporte resolve 90% dos problemas. Basta acessar a opção de suporte.\n\n"
                "**Digite uma das opções abaixo para saber mais:**\n\n"
                "1️⃣ **Como Funciona**\n"
                "2️⃣ **Comprar**\n"
                "3️⃣ **Revender**\n"
                "4️⃣ **iOS**\n"
                "5️⃣ **Auto Atendimento**\n"
                "6️⃣ **Falar com Atendente**",
                parse_mode='md'
            )
        elif chat_id in user_state and user_state[chat_id] != 'menu_principal':
            await handle_auto_atendimento_event(event, text, user_state)
        else:
            if text == '5' or text == 'auto atendimento':
                user_state[chat_id] = 'auto_atendimento'
                await auto_atendimento_menu(event)
            elif text == '6' or text == 'falar com atendente':
                await falar_com_atendente(event)
            elif text == '/auto_off':
                atendimento_auto_off.add(chat_id)
                await event.reply("🚫 **Auto Atendimento Desativado.** Para reativar, digite `Menu`.")
            else:
                await handle_option(event, text)

    def main():
        logger.info("IP brasileiro verificado. Iniciando o bot")
        client.start()
        client.run_until_disconnected()

    if __name__ == '__main__':
        main()
else:
    logger.error("IP não é brasileiro. Bot não iniciado.")
