# https://huzunluartemis.github.io/ChatSizeBot/

import asyncio
import math
import re
import time
from pyrogram.types.messages_and_media.message import Message
from pyrogram.types import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from bot import LOGGER, botStartTime
from config import Config
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
from pyrogram import Client, filters, StopPropagation
from pyrogram.enums import ParseMode
from pyrogram.enums import ChatType, ChatAction
from pyrogram.errors import FloodWait
from helper_funcs.humanfuncs import TimeFormatter, get_progressbar, humanbytes
from pyrogram.errors.exceptions.bad_request_400 import \
    ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

quee = []
cancelled_tasks = set()
USER_STATES = {}
AVAILABLE_FILTERS = ["photo", "document", "video", "sticker", "audio", "voice", "video_note", "animation"]
tg_link_regex = "(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)_?(.\d+)?_?(\d+)?"
f_msg_id = 0
t_chatid = 0
a=""
b=""
forward_delay = 6

@Client.on_callback_query(filters.regex("^cancel_task"))
async def cancel_handler(_, query):
    user_id = query.from_user.id
    cancelled_tasks.add(user_id)
    await query.answer("Cancelling task...", show_alert=True)

async def run_task(gelen: Message, duzenlenecek: Message):
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
                await duzenlenecek.edit_text(
                    '🇹🇷 Kanaldaki son mesajı iletin ya da son mesaj linkini gönderin.' \
                    '\n🇬🇧 Forward the last message on the channel or send the last message link.' \
                    '\nÖrnek / Example: `https://t.me/c/6262626/24234234`'
                    , disable_web_page_preview=True
                )
                return await on_task_complete()
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
            await duzenlenecek.edit_text(
                    '🇹🇷 Bir kanal ya da grup olmalı.' \
                    '\n🇬🇧 Must be a channel or group.'
                    , disable_web_page_preview=True
                )
            return await on_task_complete()
        # get access to chat
        try:
            gotchat:Chat = await duzenlenecek._client.get_chat(chat_id)
        except (ChannelInvalid, ChannelPrivate, ChatAdminRequired):
            await duzenlenecek.edit_text(
                '🇹🇷 Beni kanalınıza/grubunuza yönetici olarak eklemelisiniz.' \
                    '\n🇬🇧 You must add me to your channel/group as admin.'
                    , disable_web_page_preview=True
            )
            return await on_task_complete()
        except (UsernameInvalid, UsernameNotModified):
            await duzenlenecek.edit_text('Geçersiz kullanıcı adı.', disable_web_page_preview=True)
            return await on_task_complete()
        except Exception as e:
            LOGGER.exception(e)
            await duzenlenecek.edit_text(f'Errors - {e}', disable_web_page_preview=True)

        if not gotchat:
            await duzenlenecek.edit_text(
                '🇹🇷 Beni kanalınıza/grubunuza yönetici olarak eklemelisiniz.' \
                    '\n🇬🇧 You must add me to your channel/group as admin.'
                    , disable_web_page_preview=True
            )
            return await on_task_complete()

        if a != b:
            try:
                await duzenlenecek._client.send_chat_action(t_chatid, ChatAction.TYPING)
            except Exception as e:
                await duzenlenecek.edit_text(f'Error getting target chat: {e}\n\nPlease make sure I am a member of the target channel and have permission to send messages.')
                LOGGER.exception(e)
                return await on_task_complete()

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
                await duzenlenecek.edit_text("❌ **Task Cancelled by user.**")
                return await on_task_complete()

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
                    await duzenlenecek.edit_text(text=txt, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, reply_markup=cancel_button)
                except: pass
            # kaydet
            message:Message = None
            try:
                message = await duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                if message and not message.empty and a != b:
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
                        await asyncio.sleep(forward_delay)
                        await message.copy(t_chatid)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                message = await duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                if message and not message.empty and a != b:
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
                        await asyncio.sleep(forward_delay)
                        await message.copy(t_chatid)
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
            await duzenlenecek.edit_text(
                     txt,
                    parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
                )
    except Exception as e:
        await duzenlenecek.edit_text("Cannot completed. Try again later.")
        LOGGER.exception(e)
    await on_task_complete()

async def on_task_complete():
    if len(quee) > 0:
        del quee[0]
    if len(quee) > 0:
        await asyncio.sleep(10)
        await run_task(quee[0][0], quee[0][1])

async def finalize_index(client, message, state):
    user_id = state["original_message"].from_user.id
    start_id = state["start_id"]
    end_id = state["end_id"]
    chat_id = state["chat_id"]
    target_chat = state.get("target_chat")
    filters_list = state.get("filters")

    source_link = state["end_link"]
    regex = re.compile(tg_link_regex)
    match = regex.match(source_link)
    base_link = source_link[:match.end(5)]

    if target_chat:
        command_text = f"{base_link}_{target_chat}_{start_id}"
        if filters_list:
            command_text += f" --filter {filters_list}"
    else:
        command_text = f"{base_link}_{start_id}_{start_id}"

    if user_id in USER_STATES:
        del USER_STATES[user_id]

    await message.edit_text("✅ All data collected. Starting task...", reply_markup=None)

    original_message = state["original_message"]
    original_message.text = command_text
    await handler(client, original_message)

@Client.on_message(filters.private & filters.incoming, group=-1)
async def interactive_handler(client, message):
    user_id = message.from_user.id
    try:
        if user_id not in USER_STATES:
            return

        text = message.text or message.caption or ""

        if text.startswith("/"):
            del USER_STATES[user_id]
            return

        state = USER_STATES[user_id]

        # Timeout check (5 minutes)
        if time.time() - state.get("last_activity", time.time()) > 300:
            del USER_STATES[user_id]
            return
        state["last_activity"] = time.time()

        step = state.get("step")
        cancel_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel_index")]])

        if not text:
            await message.reply_text("❌ Please send a text message or a link.", reply_markup=cancel_markup)
            message.stop_propagation()
            return

        if step == "WAIT_START_LINK":
            regex = re.compile(tg_link_regex)
            match = regex.match(text or "")
            if not match:
                await message.reply_text("❌ Invalid link. Please send a valid Telegram message link for the **Start Message**:", reply_markup=cancel_markup)
                message.stop_propagation()
                return

            state["start_link"] = text
            state["chat_id"] = match[4]
            state["start_id"] = int(match[5])
            state["step"] = "WAIT_END_LINK"
            await message.reply_text(f"✅ Start Message saved (ID: {state['start_id']}).\n\nPlease send the **End Message Link**:", reply_markup=cancel_markup)
            message.stop_propagation()

        elif step == "WAIT_END_LINK":
            regex = re.compile(tg_link_regex)
            match = regex.match(text or "")
            if not match:
                await message.reply_text("❌ Invalid link. Please send a valid Telegram message link for the **End Message**:", reply_markup=cancel_markup)
                message.stop_propagation()
                return

            if match[4] != state["chat_id"]:
                await message.reply_text("❌ Error: Start and End messages must be from the same chat.\n\nPlease send a valid **End Message Link** from the same chat:", reply_markup=cancel_markup)
                message.stop_propagation()
                return

            state["end_link"] = text
            state["end_id"] = int(match[5])

            if state["end_id"] < state["start_id"]:
                state["start_id"], state["end_id"] = state["end_id"], state["start_id"]
                state["start_link"], state["end_link"] = state["end_link"], state["start_link"]

            state["step"] = "WAIT_TARGET_CHAT"
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ Skip (Size Only)", callback_data="skip_target")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_index")]
            ])
            await message.reply_text("✅ End Message saved.\n\nNow, send the **Target Chat ID/Link/Username** to forward messages, or click **Skip** to just calculate the size:", reply_markup=markup)
            message.stop_propagation()

        elif step == "WAIT_TARGET_CHAT":
            target_input = text.strip()

            # Check if it's a link first
            regex = re.compile(tg_link_regex)
            match = regex.match(target_input)
            if match:
                target_chat = match[4]
                if target_chat.isnumeric():
                    target_chat = int(f"-100{target_chat}")
            else:
                # Not a link, could be ID or username
                target_chat = target_input
                if target_chat.startswith("-"):
                    try:
                        target_chat = int(target_chat)
                    except ValueError:
                        pass
                elif target_chat.isnumeric():
                    target_chat = int(f"-100{target_chat}")

            try:
                chat = client.get_chat(target_chat)
                state["target_chat"] = chat.id
            except Exception as e:
                await message.reply_text(f"❌ Error: {e}\n\nCould not find chat `{target_input}`. Please make sure I am a member of that chat and send a valid ID/Username/Link:", reply_markup=cancel_markup)
                message.stop_propagation()
                return

            state["step"] = "WAIT_FILTERS"
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ Skip (No Filters)", callback_data="skip_filters")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_index")]
            ])
            filters_str = ", ".join(AVAILABLE_FILTERS)
            await message.reply_text(f"✅ Target Chat saved: `{chat.title or chat.username}`\n\nSend **media filters** separated by commas (e.g., `video,document`) or click **Skip** to forward everything.\n\n**Available filters:**\n`{filters_str}`", reply_markup=markup)
            message.stop_propagation()

        elif step == "WAIT_FILTERS":
            filters_list = [f.strip().lower() for f in text.split(',')]
            valid_filters = [f for f in filters_list if f in AVAILABLE_FILTERS]

            if not valid_filters:
                await message.reply_text(f"❌ No valid filters found. Available filters: `{', '.join(AVAILABLE_FILTERS)}`.\n\nPlease send valid filters or click **Skip**.", reply_markup=cancel_markup)
                message.stop_propagation()
                return

            state["filters"] = ",".join(valid_filters)
            await finalize_index(client, await message.reply_text("Processing...", quote=True), state)
            message.stop_propagation()
    except StopPropagation:
        raise
    except Exception as e:
        LOGGER.exception(e)
        if user_id in USER_STATES:
            del USER_STATES[user_id]
        await message.reply_text(f"❌ An error occurred: {e}\nInteractive session cancelled.")
        message.stop_propagation()

@Client.on_callback_query(filters.regex("^skip_target"))
async def skip_target_handler(client, query):
    user_id = query.from_user.id
    if user_id not in USER_STATES:
        await query.answer("Session expired.", show_alert=True)
        return

    state = USER_STATES[user_id]
    state["target_chat"] = None
    state["filters"] = None
    await query.answer("Skipped forwarding.")
    await finalize_index(client, query.message, state)

@Client.on_callback_query(filters.regex("^skip_filters"))
async def skip_filters_handler(client, query):
    user_id = query.from_user.id
    if user_id not in USER_STATES:
        await query.answer("Session expired.", show_alert=True)
        return

    state = USER_STATES[user_id]
    state["filters"] = None
    await query.answer("Skipped filters.")
    await finalize_index(client, query.message, state)

@Client.on_message((filters.forwarded | ((filters.regex(tg_link_regex)) & filters.text)) & filters.private & filters.incoming)
async def handler(_, message: Message):
    if message.from_user.id in USER_STATES:
        return
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    # add to quee
    duz:Message = await message.reply_text(f"✅ Your Turn: {len(quee)+1}\nWait. Dont spam with same ID.", quote=True, disable_web_page_preview=True)
    quee.append([message, duz])
    if len(quee) == 1: await run_task(message, duz)

@Client.on_message(filters.command(["help", "yardım", "yardim", "start", "h", "y"]))
async def welcome(_, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    te = "🇹🇷 Esenlikler. Bir kanal/grup kimliği gönder, tüm dosyaların toplam boyutunu hesaplaycağım." \
        "\nKanaldaki / gruptaki son mesaja tıkla, mesaj bağlantısını kopyala, bana yapıştır." \
        "\n\n🇬🇧 Hi. Send a channel/group id and I will calculate the full size of all files." \
        "\nClick the last message in the channel / group, copy the message link, paste it to me Sir.." \
        f"\n\n**@{Config.CHANNEL_OR_CONTACT}**"
    await message.reply_text(te, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@Client.on_message(filters.command("index") & filters.private)
async def index_command(client, message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    user_id = message.from_user.id
    USER_STATES[user_id] = {
        "step": "WAIT_START_LINK",
        "original_message": message,
        "last_activity": time.time()
    }
    await message.reply_text(
        "Please send the **Start Message Link**:\n(e.g., https://t.me/IslamicNasheedHQ/6)",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel_index")]])
    )

@Client.on_callback_query(filters.regex("^cancel_index"))
async def cancel_index_handler(_, query):
    user_id = query.from_user.id
    if user_id in USER_STATES:
        del USER_STATES[user_id]
    await query.message.edit_text("❌ Interactive session cancelled.")
    await query.answer()

@Client.on_message(filters.command("delay"))
async def delay_command(_, message: Message):
    global forward_delay
    if not AuthUserCheck(message): return
    if len(message.command) > 1:
        try:
            delay = int(message.command[1])
            if 0 <= delay <= 60:
                forward_delay = delay
                await message.reply_text(f"Forwarding delay has been set to {delay} seconds.")
            else:
                await message.reply_text("Please provide a delay between 0 and 60 seconds.")
        except ValueError:
            await message.reply_text("Invalid delay. Please provide a number.")
    else:
        await message.reply_text(f"Current delay is {forward_delay} seconds. Use /delay <seconds> to set a new delay.")
