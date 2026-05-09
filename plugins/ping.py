# https://huzunluartemis.github.io/ChatSizeBot/

import time
from pyrogram import Client, filters
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
from pyrogram.types.messages_and_media.message import Message

@Client.on_message(filters.command("ping"))
async def ping(_, message:Message):
    if not AuthUserCheck(message): return
    if await ForceSub(message) == 400: return
    start_time = int(round(time.time() * 1000))
    reply = await message.reply_text("Ping")
    end_time = int(round(time.time() * 1000))
    await reply.edit_text(f"Pong\n{end_time - start_time} ms")
