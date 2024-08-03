#como_funciona.py
import logging
from telethon.tl.types import InputDocument, Document, PeerChannel

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

async def como_funciona(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 8  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            logger.info(f"Referência de arquivo obtida: {document.file_reference}")
            await event.client.send_file(
                event.chat_id,
                document,
                caption=(
                    "📘 **Como Funciona** 📘\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🚀 **Descubra as Vantagens da Internet Ilimitada NetDez!** 🚀\n\n"
                    "🔹 **Mantenha-se sempre conectado!**\n"
                    "Mesmo após atingir o limite da sua franquia, continue navegando livremente com nosso aplicativo.\n\n"
                    "🔹 **Aplicativo intuitivo e fácil de usar**\n"
                    "Disponível para todos os sistemas operacionais, incluindo Android e iOS.\n\n"
                    "Transforme sua comunicação hoje mesmo: aproveite a liberdade total para navegar sem limites.\n\n"
                    "ℹ️ **E TEM MAIS...** Você sabia que é possível compartilhar sua internet? Nós ensinamos como fazer isso!\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "📌 **Digite** `Menu` **para solicitar o menu de alternativas novamente**"
                ),
                parse_mode='md'
            )
        else:
            logger.error("Falha ao obter a referência do arquivo")
            await event.reply("Erro ao obter a nova referência do arquivo. Por favor, tente novamente mais tarde.")
    except Exception as e:
        logger.error(f"Erro ao enviar o vídeo: {str(e)}")
        await event.reply(f"Erro ao enviar o vídeo: {str(e)}")
