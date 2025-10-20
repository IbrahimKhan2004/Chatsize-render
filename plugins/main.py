# https://huzunluartemis.github.io/ChatSizeBot/

import math
import re
import time
from pyrogram.types.messages_and_media.message import Message
from pyrogram.types import Chat
from bot import LOGGER, botStartTime
from config import Config
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from helper_funcs.humanfuncs import TimeFormatter, get_progressbar, humanbytes
from pyrogram.errors.exceptions.bad_request_400 import \
    ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

quee = []
tg_link_regex = "(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)_?(.\d+)?_?(\d+)?"
f_msg_id = 0
t_chatid = 0
a=""
b=""
def run_task(gelen: Message, duzenlenecek: Message):
    try:
        if gelen.text:
            regex = re.compile(tg_link_regex)
            match = regex.match(gelen.text)
            if not match:
                duzenlenecek.edit_text(
                    '🇹🇷 Kanaldaki son mesajı iletin ya da son mesaj linkini gönderin.' \
                    '\n🇬🇧 Forward the last message on the channel or send the last message link.' \
                    '\nÖrnek / Example: `https://t.me/c/6262626/24234234`'
                    , disable_web_page_preview=True
                )
                return on_task_complete()
            chat_id = match[4]
            last_msg_id = int(match[5])
            a = match[6]
            b = match[7]
            if a==b:
                f_msg_id = int(match[7]) if a is not None else 1
            else:
                f_msg_id = 1 if b is None else int(match[7])
                t_chatid = int(match[6])
            if chat_id.isnumeric():
                chat_id = int(f"-100{chat_id}")
        elif gelen.forward_from_chat.type in [ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP]:
            last_msg_id = gelen.forward_from_message_id
            chat_id = gelen.forward_from_chat.username or gelen.forward_from_chat.id
        else:
            duzenlenecek.edit_text(
                    '🇹🇷 Bir kanal ya da grup olmalı.' \
                    '\n🇬🇧 Must be a channel or group.'
                    , disable_web_page_preview=True
                )
            return on_task_complete()
        # get access to chat
        try:
            gotchat:Chat = duzenlenecek._client.get_chat(chat_id)
        except (ChannelInvalid, ChannelPrivate, ChatAdminRequired):
            duzenlenecek.edit_text(
                '🇹🇷 Beni kanalınıza/grubunuza yönetici olarak eklemelisiniz.' \
                    '\n🇬🇧 You must add me to your channel/group as admin.'
                    , disable_web_page_preview=True
            )
            return on_task_complete()
        except (UsernameInvalid, UsernameNotModified):
            duzenlenecek.edit_text('Geçersiz kullanıcı adı.', disable_web_page_preview=True)
            return on_task_complete()
        except Exception as e:
            LOGGER.exception(e)
            duzenlenecek.edit_text(f'Errors - {e}', disable_web_page_preview=True)

        if a != b:
            try:
                duzenlenecek._client.get_chat(t_chatid)
            except Exception as e:
                duzenlenecek.edit_text(f'Error getting target chat: {e}\n\nPlease make sure I am a member of the target channel and have permission to send messages.')
                LOGGER.exception(e)
                return on_task_complete()

        if not gotchat:
            duzenlenecek.edit_text(
                '🇹🇷 Beni kanalınıza/grubunuza yönetici olarak eklemelisiniz.' \
                    '\n🇬🇧 You must add me to your channel/group as admin.'
                    , disable_web_page_preview=True
            )
            return on_task_complete()

        #
        txt = ""
        total = last_msg_id + 1
        current = f_msg_id - 1
        empty = nomessage = nomedia = mediawosize = total_calculated_size = m = 0
        start_time = time.time()
        while current < total:
            current = current + 1
            # hız
            try: hiz = (current / ((time.time() - start_time).__round__())).__round__()
            except: hiz = 0
            # guncelle
            if current % 30 == 0:
                try:

                    infochat = f"**💚 Chat Info**\n" \
                               f"**Name:** `{gotchat.title}`\n" \
                               f"**Username:** @{gotchat.username}\n" \
                               f"**Chat ID:** `{gotchat.id}`\n" \
                               f"**Chat DC:** `{gotchat.dc_id}`\n" \
                               f"**First Message ID:** `{f_msg_id}`\n" \
                               f"**Last Message ID:** `{last_msg_id}`"


                    process_info = f"**💜 Process**\n" \
                                   f"**Total Size:** `{humanbytes(total_calculated_size)}`\n" \
                                   f"**Processed:** `{current - f_msg_id}`\n" \
                                   f"**Remaining:** `{total - current}`\n" \
                                   f"**Deleted:** `{empty}`\n" \
                                   f"**Damaged:** `{nomessage}`\n" \
                                   f"**Non-Media:** `{nomedia}`\n" \
                                   f"**Media:** `{m}`\n" \
                                   f"**No Filesize:** `{mediawosize}`"


                    time_info = f"**⏱️ Time**\n" \
                                f"**Passed:** `{TimeFormatter(time.time() - start_time)}`\n" \
                                f"**Elapsed:** `{TimeFormatter((total - current) / hiz if hiz > 0 else 0)}`\n" \
                                f"**Speed:** `{hiz} msg/s`\n" \
                                f"**Uptime:** `{TimeFormatter(time.time() - botStartTime)}`"


                    progress = f"**📊 Progress**\n" \
                               f"`{get_progressbar(current, total)}`\n" \
                               f"**Percent:** `%{'{:.7f}'.format((current * 100 / total))}`"


                    txt = f"{progress}\n\n{infochat}\n\n{process_info}\n\n{time_info}"
                    duzenlenecek.edit_text(text=txt, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                except: pass
            # kaydet
            message:Message = None
            try:
                message = duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                if a != b:
                    message.copy(t_chatid)
            except FloodWait as e:
                time.sleep(e.value)
                message = duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                if a != b:
                    message.copy(t_chatid)
            except Exception as e:
                LOGGER.exception(e)
                continue
            if not message:
                nomessage  += 1
                continue
            elif message.empty:
                empty = empty + 1
                continue
            #◙ find media
            media = None
            media_array = [message.document, message.video, message.audio, message.photo, message.animation, message.voice, message.video_note]
            for i in media_array:
                if i is not None:
                    media = i
                    m += 1
                    break
            if not media:
                nomedia += 1
                continue
            # find size
            if media.file_size:
                total_calculated_size += int(media.file_size)
            else:
                mediawosize  += 1
            continue
        #
        if last_msg_id <= 30:

            infochat = f"**💚 Chat Info**\n" \
                       f"**Name:** `{gotchat.title}`\n" \
                       f"**Username:** @{gotchat.username}\n" \
                       f"**Chat ID:** `{gotchat.id}`\n" \
                       f"**Chat DC:** `{gotchat.dc_id}`\n" \
                       f"**First Message ID:** `{f_msg_id}`\n" \
                       f"**Last Message ID:** `{last_msg_id}`"


            process_info = f"**💜 Process**\n" \
                           f"**Total Size:** `{humanbytes(total_calculated_size)}`\n" \
                           f"**Processed:** `{current - f_msg_id}`\n" \
                           f"**Deleted:** `{empty}`\n" \
                           f"**Damaged:** `{nomessage}`\n" \
                           f"**Non-Media:** `{nomedia}`\n" \
                           f"**Media:** `{m}`\n" \
                           f"**No Filesize:** `{mediawosize}`"


            time_info = f"**⏱️ Time**\n" \
                        f"**Passed:** `{TimeFormatter(time.time() - start_time)}`\n" \
                        f"**Uptime:** `{TimeFormatter(time.time() - botStartTime)}`"


            progress = f"**📊 Progress**\n" \
                       f"`{get_progressbar(current, total)}`\n" \
                       f"**Percent:** `%{'{:.3f}'.format(current * 100 / total)}`"


            txt = f"{progress}\n\n{infochat}\n\n{process_info}\n\n{time_info}\n\n[✅](https://t.me/{Config.CHANNEL_OR_CONTACT}) **Finished**"
            duzenlenecek.edit_text(
                     txt,
                    parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
                )
    except Exception as e:
        duzenlenecek.edit_text("Cannot completed. Try again later.")
        LOGGER.exception(e)
    on_task_complete()

def on_task_complete():
    if len(quee) > 0:
        del quee[0]
    if len(quee) > 0:
        time.sleep(10)
        run_task(quee[0][0], quee[0][1])

@Client.on_message((filters.forwarded | ((filters.regex(tg_link_regex)) & filters.text)) & filters.private & filters.incoming)
def handler(_, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    # add to quee
    duz:Message = message.reply_text(f"✅ Your Turn: {len(quee)+1}\nWait. Dont spam with same ID.", quote=True, disable_web_page_preview=True)
    quee.append([message, duz])
    if len(quee) == 1: run_task(message, duz)

@Client.on_message(filters.command(["help", "yardım", "yardim", "start", "h", "y"]))
def welcome(_, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    te = "🇹🇷 Esenlikler. Bir kanal/grup kimliği gönder, tüm dosyaların toplam boyutunu hesaplaycağım." \
        "\nKanaldaki / gruptaki son mesaja tıkla, mesaj bağlantısını kopyala, bana yapıştır." \
        "\n\n🇬🇧 Hi. Send a channel/group id and I will calculate the full size of all files." \
        "\nClick the last message in the channel / group, copy the message link, paste it to me.." \
        f"\n\n**@{Config.CHANNEL_OR_CONTACT}**"
    message.reply_text(te, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
