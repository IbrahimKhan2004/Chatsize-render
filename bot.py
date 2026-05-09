# https://huzunluartemis.github.io/ChatSizeBot/

import logging
import time
from config import Config
from pyrogram import idle
import pyrogram
import asyncio
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
botStartTime = time.time()

async def main():
    plugins = dict(root = 'plugins')
    app = pyrogram.Client("ChatSizeBot", bot_token = Config.BOT_TOKEN,
        api_id = Config.APP_ID, api_hash = Config.API_HASH, plugins = plugins)
    await app.start()
    LOGGER.info(await app.get_me())
    LOGGER.info(msg="Bot Started.")
    try: await app.send_message(Config.OWNER_ID, "Bot Started.")
    except: pass
    await idle()
    LOGGER.info(msg="Bot Stopped.")
    try: await app.send_message(Config.OWNER_ID, "Bot Stopped.")
    except: pass

if __name__ == '__main__':
    asyncio.run(main())
