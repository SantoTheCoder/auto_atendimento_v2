#revender.py
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

async def revender(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 10  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            logger.info(f"Referência de arquivo obtida: {document.file_reference}")
            await event.client.send_file(
                event.chat_id,
                document,
                caption=(
                    "🚀 **Torne-se um Revendedor** 🚀\n\n"
                    "Está interessado em revender nossos inovadores serviços de internet? Confira os detalhes e comece sua jornada de sucesso:\n\n"
                    "💵 **Investimento Acessível:** Torne-se um revendedor por apenas R$4,00 por cliente, com total liberdade para definir o preço de revenda. A recarga mínima é de R$40,00.\n\n"
                    "🔄 **Sub Revenda:** Tenha sua própria rede de revendedores.\n\n"
                    "🔁 **Testes Ilimitados:** Ofereça testes ilimitados aos seus clientes.\n\n"
                    "🖼 **Material de Apoio:** Banners exclusivos em: [@BANNERS_NET_ILIMITADA](https://t.me/BANNERS_NET_ILIMITADA).\n\n"
                    "📝 **Passos para se Tornar um Revendedor:**\n\n"
                    "1. Adquira créditos automaticamente em nosso bot [@netdez_bot](https://t.me/netdez_bot) e administre diretamente pelo bot.\n"
                    "2. Utilize nosso painel de revenda para quem preferir administrar por um painel.\n"
                    "3. Realize o login e gerencie seus usuários com facilidade.\n\n"
                    "**Inicie Agora:**\n\n"
                    "**BOT:**\n"
                    "- [@Netdez_bot](https://t.me/netdez_bot)\n\n"
                    "**PAINEL:**\n"
                    "- **Cadastro:** [Clique aqui](https://netdez.sshshop.com.br/manage/register.php)\n"
                    "- **Login:** [Clique aqui](https://netdez.sshshop.com.br/manage/index.php)\n\n"
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
