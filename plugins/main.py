# https://huzunluartemis.github.io/ChatSizeBot/

import math
import re
import time
from pyrogram.types.messages_and_media.message import Message
from pyrogram.types import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from bot import LOGGER, botStartTime
from config import Config
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.enums import ChatType, ChatAction
from pyrogram.errors import FloodWait
from helper_funcs.humanfuncs import TimeFormatter, get_progressbar, humanbytes
from pyrogram.errors.exceptions.bad_request_400 import \
    ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

quee = []
cancelled_tasks = set()
tg_link_regex = "(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)_?(.\d+)?_?(\d+)?"
f_msg_id = 0
t_chatid = 0
a=""
b=""

@Client.on_callback_query(filters.regex("^cancel_task"))
def cancel_handler(_, query):
    user_id = query.from_user.id
    cancelled_tasks.add(user_id)
    query.answer("Cancelling task...", show_alert=True)

def run_task(gelen: Message, duzenlenecek: Message):
    user_id = gelen.from_user.id
    if user_id in cancelled_tasks:
        cancelled_tasks.remove(user_id)

    try:
        if gelen.text:
            filters_list = []
            link_to_parse = gelen.text
            if ' --filter ' in gelen.text:
                parts = gelen.text.split(' --filter ')
                link_to_parse = parts[0].strip()
                filter_part = parts[1].strip()
                if filter_part:
                    filters_list = [f.strip().lower() for f in filter_part.split(',')]

            regex = re.compile(tg_link_regex)
            match = regex.match(link_to_parse)
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

        if not gotchat:
            duzenlenecek.edit_text(
                '🇹🇷 Beni kanalınıza/grubunuza yönetici olarak eklemelisiniz.' \
                    '\n🇬🇧 You must add me to your channel/group as admin.'
                    , disable_web_page_preview=True
            )
            return on_task_complete()

        if a != b:
            try:
                duzenlenecek._client.send_chat_action(t_chatid, ChatAction.TYPING)
            except Exception as e:
                duzenlenecek.edit_text(f'Error getting target chat: {e}\n\nPlease make sure I am a member of the target channel and have permission to send messages.')
                LOGGER.exception(e)
                return on_task_complete()

        #
        txt = ""
        total_loop = last_msg_id + 1
        current = f_msg_id - 1
        
        total_messages_in_range = last_msg_id - f_msg_id + 1

        empty = nomessage = nomedia = mediawosize = total_calculated_size = m = 0
        start_time = time.time()
        while current < total_loop:
            if user_id in cancelled_tasks:
                cancelled_tasks.remove(user_id)
                duzenlenecek.edit_text("❌ **Task Cancelled by user.**")
                return on_task_complete()

            current = current + 1
            # hız
            try: hiz = ((current - f_msg_id + 1) / ((time.time() - start_time).__round__())).__round__()
            except: hiz = 0
            # guncelle
            if current % 30 == 0:
                try:
                    processed_count = current - f_msg_id + 1
                    infochat = f"**💚 Chat Info**\n" \
                               f"**Name:** `{gotchat.title}`\n" \
                               f"**Username:** @{gotchat.username}\n" \
                               f"**Chat ID:** `{gotchat.id}`\n" \
                               f"**Chat DC:** `{gotchat.dc_id}`\n" \
                               f"**First Message ID:** `{f_msg_id}`\n" \
                               f"**Last Message ID:** `{last_msg_id}`"


                    process_info = f"**💜 Process**\n" \
                                   f"**Total Size:** `{humanbytes(total_calculated_size)}`\n" \
                                   f"**Processed:** `{processed_count}`\n" \
                                   f"**Remaining:** `{total_messages_in_range - processed_count}`\n" \
                                   f"**Deleted:** `{empty}`\n" \
                                   f"**Damaged:** `{nomessage}`\n" \
                                   f"**Non-Media:** `{nomedia}`\n" \
                                   f"**Media:** `{m}`\n" \
                                   f"**No Filesize:** `{mediawosize}`"


                    time_info = f"**⏱️ Time**\n" \
                                f"**Passed:** `{TimeFormatter(time.time() - start_time)}`\n" \
                                f"**Elapsed:** `{TimeFormatter((total_messages_in_range - processed_count) / hiz if hiz > 0 else 0)}`\n" \
                                f"**Speed:** `{hiz} msg/s`\n" \
                                f"**Uptime:** `{TimeFormatter(time.time() - botStartTime)}`"


                    progress = f"**📊 Progress**\n" \
                               f"`{get_progressbar(processed_count, total_messages_in_range)}`\n" \
                               f"**Percent:** `%{'{:.2f}'.format((processed_count * 100 / total_messages_in_range))}`"


                    txt = f"{progress}\n\n{infochat}\n\n{process_info}\n\n{time_info}"
                    cancel_button = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel Task ❌", callback_data="cancel_task")]])
                    duzenlenecek.edit_text(text=txt, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, reply_markup=cancel_button)
                except: pass
            # kaydet
            message:Message = None
            try:
                message = duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                if a != b:
                    forward_this = True
                    if filters_list:
                        has_allowed_media = False
                        for media_type in filters_list:
                            if getattr(message, media_type, None):
                                has_allowed_media = True
                                break
                        if not has_allowed_media:
                            forward_this = False
                    
                    if forward_this:
                        time.sleep(3)
                        message.copy(t_chatid)
            except FloodWait as e:
                time.sleep(e.value)
                message = duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                if a != b:
                    forward_this = True
                    if filters_list:
                        has_allowed_media = False
                        for media_type in filters_list:
                            if getattr(message, media_type, None):
                                has_allowed_media = True
                                break
                        if not has_allowed_media:
                            forward_this = False
                    
                    if forward_this:
                        time.sleep(3)
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
            
            if a != b and filters_list:
                has_allowed_media = False
                for media_type in filters_list:
                    if getattr(message, media_type, None):
                        has_allowed_media = True
                        break
                if not has_allowed_media:
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
        processed_count = current - f_msg_id + 1
        if last_msg_id <= 30 or True:
            infochat = f"**💚 Chat Info**\n" \
                       f"**Name:** `{gotchat.title}`\n" \
                       f"**Username:** @{gotchat.username}\n" \
                       f"**Chat ID:** `{gotchat.id}`\n" \
                       f"**Chat DC:** `{gotchat.dc_id}`\n" \
                       f"**First Message ID:** `{f_msg_id}`\n" \
                       f"**Last Message ID:** `{last_msg_id}`"


            process_info = f"**💜 Process**\n" \
                           f"**Total Size:** `{humanbytes(total_calculated_size)}`\n" \
                           f"**Processed:** `{processed_count}`\n" \
                           f"**Deleted:** `{empty}`\n" \
                           f"**Damaged:** `{nomessage}`\n" \
                           f"**Non-Media:** `{nomedia}`\n" \
                           f"**Media:** `{m}`\n" \
                           f"**No Filesize:** `{mediawosize}`"


            time_info = f"**⏱️ Time**\n" \
                        f"**Passed:** `{TimeFormatter(time.time() - start_time)}`\n" \
                        f"**Uptime:** `{TimeFormatter(time.time() - botStartTime)}`"


            progress = f"**📊 Progress**\n" \
                       f"`{get_progressbar(processed_count, total_messages_in_range)}`\n" \
                       f"**Percent:** `%{'{:.2f}'.format((processed_count * 100 / total_messages_in_range))}`"


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
