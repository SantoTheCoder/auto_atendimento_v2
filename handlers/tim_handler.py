#tim_handler.py
import logging
from telethon.tl.types import Document, PeerChannel

logger = logging.getLogger(__name__)

async def get_channel_details(client, channel_url):
    try:
        entity = await client.get_entity(channel_url)
        if hasattr(entity, 'id') and hasattr(entity, 'access_hash'):
            return entity.id, entity.access_hash
        else:
            logger.error(f"A entidade não é um canal ou não possui 'id' e 'access_hash': {entity}")
            return None, None
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do canal: {str(e)}")
        return None, None

async def get_new_file_reference(client, channel_url, message_id):
    try:
        logger.info(f"Obtendo nova referência de arquivo para channel_url={channel_url}, message_id={message_id}")
        channel_id, access_hash = await get_channel_details(client, channel_url)
        if not channel_id or not access_hash:
            logger.error("Não foi possível obter channel_id ou access_hash")
            return None

        entity = await client.get_entity(PeerChannel(channel_id))
        logger.info(f"Entidade obtida: {entity}")

        messages = await client.get_messages(entity, ids=[message_id])
        logger.info(f"Mensagens obtidas: {messages}")

        if messages:
            message = messages[0]
            logger.info(f"Primeira mensagem: {message}")
            if isinstance(message.media.document, Document):
                logger.info(f"Documento encontrado na mensagem: {message.media.document}")
                return message.media.document
            else:
                logger.error(f"Nenhum documento encontrado na mensagem com ID {message_id}")
        else:
            logger.error(f"Nenhuma mensagem encontrada para o ID da mensagem {message_id}")
    except Exception as e:
        logger.error(f"Erro ao obter referência do arquivo: {str(e)}")
    return None

async def tim_auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento TIM** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Conecta, mas não Gera Dados**\n"
        "🔙 Escreva `Voltar` para retornar ao menu anterior",
        parse_mode='md'
    )

async def handle_tim_auto_atendimento(event, text, user_state):
    user_id = event.sender_id
    if text == '1':
        await problema_conexao_tim(event)
    elif text == '2':
        await conecta_nao_gera_dados_tim(event)
    elif text == 'voltar' or text == 'menu':
        user_state[user_id] = 'auto_atendimento'
        await tim_auto_atendimento(event)
    else:
        await event.reply(
            "⚠️ Opção inválida. Por favor, selecione uma das opções do menu de autoatendimento TIM.\n"
            "🔙 Escreva `Voltar` para retornar ao menu anterior",
            parse_mode='md'
        )

async def problema_conexao_tim(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 14  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            await event.client.send_file(
                event.chat_id,
                document,
                caption=(
                    "🌐 **Problema de Conexão TIM** 🌐\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Cada região possui uma configuração diferente. Verifique se você tem saldo válido ou saldo expirado (ligue para *222#).\n\n"
                    "1. **Testar todas as opções da operadora TIM:**\n"
                    "   - Cada configuração funciona em determinadas regiões.\n\n"
                    "2. **Conferir Saldo:**\n"
                    "   - Se tiver saldo expirado e não funcionar, é necessário fazer uma recarga para ter saldo válido e poder usar as configurações.\n\n"
                    "3. **Alterar do 4G para 3G:**\n"
                    "   - Isso muda o IP da sua operadora, o que pode funcionar em muitas ocasiões. Nosso aplicativo força o modo avião se não conectar de primeira.\n\n"
                    "4. **Auto Modo Avião:**\n"
                    "   - Tente conectar em algumas configurações e deixe o aplicativo forçar o modo avião para encontrar uma faixa de IP que funcione na sua região.\n\n"
                    "🔙 **Escreva `Voltar` para retornar ao menu anterior**\n"
                ),
                parse_mode='md'
            )
        else:
            await event.reply("Erro ao obter a nova referência do arquivo. Por favor, tente novamente mais tarde.")
    except Exception as e:
        await event.reply(f"Erro ao enviar o vídeo: {str(e)}")

async def conecta_nao_gera_dados_tim(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 15  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            await event.client.send_file(
                event.chat_id,
                document,
                caption=(
                    "🌐 **Conecta, mas não Gera Dados TIM** 🌐\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "1. **IPV4:**\n"
                    "   - Na TIM, normalmente, basta mudar para IPV4.\n\n"
                    "2. **Usar 3G:**\n"
                    "   - Teste se conectar e gerar dados usando o 3G.\n\n"
                    "🔙 **Escreva `Voltar` para retornar ao menu anterior**\n"
                ),
                parse_mode='md'
            )
        else:
            await event.reply("Erro ao obter a nova referência do arquivo. Por favor, tente novamente mais tarde.")
    except Exception as e:
        await event.reply(f"Erro ao enviar o vídeo: {str(e)}")
