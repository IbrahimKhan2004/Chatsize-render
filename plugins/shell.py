# https://huzunluartemis.github.io/ChatSizeBot/

# https://huzunluartemis.github.io/ChatSizeBot/

import os
from pyrogram import Client, filters
from bot import LOGGER
from config import Config
from subprocess import Popen, PIPE
from pyrogram.types.messages_and_media.message import Message

@Client.on_message(filters.command("shell"))
async def shell(_, message:Message):
    if Config.OWNER_ID == 0 or message.from_user.id != Config.OWNER_ID: return
    try:
        cmd = message.text.split(' ', 1)
        if len(cmd) == 1:
            return await message.reply_text('🇬🇧 No command to execute was given.\n\n🇹🇷 Boşluk bırakıp komut gir zırcahil seni.',
                reply_to_message_id = message.id)
        cmd = cmd[1].strip()
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()
        reply = ''
        stderr = stderr.decode()
        stdout = stdout.decode()
        if len(stdout) != 0:
            reply += f"**Stdout:**\n`{stdout}`\n"
            LOGGER.info(f"Shell - {cmd} - {stdout}")
        if len(stderr) != 0:
            reply += f"**Stderr:**\n`{stderr}`\n"
            LOGGER.error(f"Shell - {cmd} - {stderr}")
        if len(reply) > 3000:
            with open('shell.txt', 'w') as file:
                file.write(reply)
            with open('shell.txt', 'rb') as doc:
                await message.reply_document(document=doc)
            if os.path.isfile('shell.txt'): os.remove('shell.txt')
        else:
            await message.reply_text(reply)
    except:
        await message.reply_text(f"🇬🇧 Maybe your shell message was empty.\n🇹🇷 Boş bir şeyler döndü valla.\n\n{reply}")
