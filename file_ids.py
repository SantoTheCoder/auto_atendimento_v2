#file_ids.py
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, Document
from config import API_ID, API_HASH

client = TelegramClient('session_name', API_ID, API_HASH)

async def get_file_details(channel_id, access_hash, message_ids):
    entity = InputPeerChannel(channel_id, access_hash)
    async with client:
        messages = await client.get_messages(entity, ids=message_ids)
        file_details = []
        for message in messages:
            if isinstance(message.media.document, Document):
                file_details.append({
                    "file_id": message.media.document.id,
                    "access_hash": message.media.document.access_hash,
                    "file_reference": message.media.document.file_reference
                })
        return file_details

channel_id = 2157663299  # ID do seu canal
access_hash = -6508081536901933377  # Substitua pelo access_hash correto

# Adicionando os novos message_ids
message_ids = [8, 9, 10, 12, 13, 14, 15]
file_details = client.loop.run_until_complete(get_file_details(channel_id, access_hash, message_ids))

print(f"Como Funciona File Details: {file_details[0]}")
print(f"Comprar File Details: {file_details[1]}")
print(f"Revender File Details: {file_details[2]}")
print(f"VIVO - Não Conecta: {file_details[3]}")
print(f"VIVO - Conecta mas não funciona: {file_details[4]}")
print(f"TIM - Não Conecta: {file_details[5]}")
print(f"TIM - Conecta mas não funciona: {file_details[6]}")
