#vivo_handler.py
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

async def vivo_auto_atendimento(event):
    await event.reply(
        "💬 **Auto Atendimento Vivo** 💬\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Selecione uma das opções abaixo para obter ajuda:\n\n"
        "1️⃣ **Não Conecta**\n"
        "2️⃣ **Conecta, mas não Funciona**\n"
        "🔙 Escreva `Voltar` para retornar ao menu anterior",
        parse_mode='md'
    )

async def handle_vivo_auto_atendimento(event, text, user_state):
    user_id = event.sender_id
    if text == '1':
        await problema_conexao_vivo(event)
    elif text == '2':
        await conecta_nao_funciona_vivo(event)
    elif text == 'voltar' or text == 'menu':
        user_state[user_id] = 'auto_atendimento'
        await vivo_auto_atendimento(event)
    else:
        await event.reply(
            "⚠️ Opção inválida. Por favor, selecione uma das opções do menu de autoatendimento Vivo.\n"
            "🔙 Escreva `Voltar` para retornar ao menu anterior",
            parse_mode='md'
        )

async def problema_conexao_vivo(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 12  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            video_message = await event.client.send_file(
                event.chat_id,
                document,
                caption="🌐 **Problema de Conexão Vivo** 🌐"
            )
        else:
            await event.reply("Erro ao obter a nova referência do arquivo. Por favor, tente novamente mais tarde.")
            return
    except Exception as e:
        await event.reply(f"Erro ao enviar o vídeo: {str(e)}")
        return

    await event.client.send_message(
        event.chat_id,
        (
            "1. **Resumo do vídeo:**\n"
            "   Certifique-se de que \"fazer login na rede\" está ativo, conforme a imagem no vídeo.\n\n"
            "2. **Soluções:**\n\n"
            "   **a)** Atualize seu aplicativo conectando ao WiFi. Em seguida, force o portal alternando para o modo avião e voltando.\n\n"
            "   **b)** Alterne o sinal do 4G para 3G ou 2G e volte ao 4G após alguns segundos.\n\n"
            "   **c)** Solicite megas grátis através do site: [internetgratis.vivo.com.br](https://internetgratis.vivo.com.br) - O portal da Vivo retornará após os megas terminarem.\n\n"
            "   **d)** Saia do 4G e mantenha no 3G, depois tente conectar.\n\n"
            "   **e)** Após 3 tentativas de conexão, nosso aplicativo ativará o modo avião automaticamente para encontrar uma faixa de IP que funcione na sua região. Teste diferentes configurações.\n\n"
            "3. **Opções adicionais se o portal da Vivo não retornar:**\n\n"
            "   **f)** Se a Vivo parou de funcionar, faça uma recarga de qualquer valor para reativar a linha.\n\n"
            "   **g)** Considere mudar seu plano ou promoção: Vivo Pré Turbo 30 dias por R$ 20,00 mensal (funciona em todos os DDDs).\n\n"
            "   **Tutorial de Como se Cadastrar na Promoção Vivo Turbo 30 Dias:**\n"
            "   1. Envie \"VTMENSAL\" para o número 9003.\n"
            "   2. Confirme com \"SIM\".\n"
            "   3. Realize uma recarga de R$ 20,00 em até 24 horas.\n\n"
            "🔙 **Escreva `Voltar` para retornar ao menu anterior**\n"            
        ),
        reply_to=video_message.id,
        parse_mode='md'
    )

async def conecta_nao_funciona_vivo(event):
    try:
        channel_url = 'https://t.me/t56t651'  # URL do canal fornecida
        message_id = 13  # ID da mensagem a ser obtida
        document = await get_new_file_reference(event.client, channel_url, message_id)
        if document:
            video_message = await event.client.send_file(
                event.chat_id,
                document,
                caption="🌐 **Conecta, mas não Funciona Vivo** 🌐"
            )
        else:
            await event.reply("Erro ao obter a nova referência do arquivo. Por favor, tente novamente mais tarde.")
            return
    except Exception as e:
        await event.reply(f"Erro ao enviar o vídeo: {str(e)}")
        return

    await event.client.send_message(
        event.chat_id,
        (
            "**Resumo do vídeo:\n\n"
            "**Se a VPN conecta, mas não gera dados, tente as seguintes soluções:**\n\n"
            "**a)** **Protocolo da APN:** Altere as configurações de APN do seu celular para apenas IPV4.\n\n"
            "**b)** **Editar Domínio da APN:** Alterne \"zap.vivo.com.br\" para outras opções, como:\n"
            "   - recarga-api.vivo.com.br\n"
            "   - api.vivo.com.br\n"
            "   - recarga.vivo.com.br\n"
            "   - dns.vivo.com.br\n"
            "   - 4field.vivo.com.br\n"
            "   - assine.vivo.com.br\n\n"
            "**c)** **Mudar a Banda H+/4G/5G:** Use seu 3G invés do 4G:\n"
            "   - Configurações » Redes » Redes Móveis » Seleção de Banda\n\n"
            "**Extra:**\n\n"
            "**d)** Se nenhuma opção resolver, considere mudar seu plano ou promoção:\n"
            "   - **Planos Sugeridos:**\n"
            "     - Vivo Pré Turbo 30 dias: R$ 20,00 mensal (recarregar R$ 20,00 a cada 30 dias).\n"
            "     - Vivo Controle: Manter o plano ativo é essencial.\n"
            "   - **Tutorial de Como se Cadastrar na Promoção Vivo Turbo 30 Dias:**\n"
            "     1. Envie \"VTMENSAL\" para o número 9003.\n"
            "     2. Confirme com \"SIM\".\n"
            "     3. Realize uma recarga de R$ 20,00 em até 24 horas.\n\n"
            "🔙 **Escreva `Voltar` para retornar ao menu anterior**\n"
        ),
        reply_to=video_message.id,
        parse_mode='md'
    )
