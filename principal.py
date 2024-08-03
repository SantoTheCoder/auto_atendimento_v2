import logging
from telethon import TelegramClient, events
from config import API_ID, API_HASH
from handlers.como_funciona import como_funciona

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('session_name', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/comofunciona'))
async def handle_como_funciona(event):
    await como_funciona(event)

def main():
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
