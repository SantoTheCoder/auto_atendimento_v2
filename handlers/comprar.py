#comprar.py
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

async def comprar(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 9  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            logger.info(f"Referência de arquivo obtida: {document.file_reference}")
            await event.client.send_file(
                event.chat_id,
                document,
                caption=(
                    "🛒 **Comprar** 🛒\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🌟 **Opções para uma Conexão Ilimitada com a NetDez!** 🌟\n\n"
                    "🔹 **Disponível em Android e iOS**: Temos a solução perfeita para você. Buscando uma experiência de internet sem fronteiras? Veja como é fácil adquirir nossos serviços:\n\n"
                    "**Servidor NET10**:\n"
                    "- **Pagamento pelo Bot**: Realize pagamentos rápidos e seguros com o [@Netdez_bot](https://t.me/Netdez_bot) ou [@Nettdez_bot](https://t.me/Nettdez_bot).\n"
                    "- **Website**: Visite [www.netdez.sshshop.com.br](http://www.netdez.sshshop.com.br/) para escolher o plano ideal para você.\n\n"
                    "**Suporte Técnico**:\n"
                    "- Orgulhosamente, oferecemos autoatendimento que responde a 90% das dúvidas e possíveis problemas. Basta selecionar a opção de autoatendimento em nosso menu.\n\n"
                    "✨ Estamos comprometidos em garantir que sua experiência conosco seja excepcional. **Pronto para navegar sem limites? Escolha a NetDez!** ✨\n\n"
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
