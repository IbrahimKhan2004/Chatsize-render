# ChatSizeBot

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

ChatSizeBot is a powerful and versatile Telegram bot that calculates the total size of files in a channel or group. It can also be used as an advanced tool for forwarding messages between chats, with support for filtering by media type.

## Features

* **Task Queue**: Manages multiple requests efficiently, ensuring smooth and reliable performance.
* **Public and Private Chat Support**: Works seamlessly in both public and private chats.
* **Comprehensive File Type Support**: Calculates the total size of documents, videos, audio files, photos, animations, voice messages, and video notes.
* **Advanced Message Forwarding**: Forward messages from one chat to another, with support for specific message ranges.
* **Media Filtering**: When forwarding, you can specify which media types to include (e.g., only `video` and `document`).
* **Real-Time Progress Updates**: Keeps you informed with a real-time progress bar.
* **Flexible Authentication**: Can be configured to serve all users or be restricted to a specific set of authorized users.
* **Forced Subscription**: Can be set up to require users to subscribe to a designated channel before they can use the bot.
* **Server Statistics**: Provides detailed server statistics for advanced users.

## Getting Started

### Prerequisites

* A Telegram account  
* A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Installation

1. **Deploy to Render**: Click the "Deploy to Render" button above to deploy the bot to Render.  
2. **Set Environment Variables**: In the Render dashboard, go to the "Environment" section and add the environment variables listed in the "Configuration" section below.  
3. **Set Bot Commands**: In Telegram, open a chat with [@BotFather](https://t.me/BotFather), select your bot, and use the `/setcommands` command to add the following commands:

    ```
    start - bot help
    ping - check bot online status
    stats - bot statistics
    shell - execute shell command (admin only)
    log - send bot logs (admin only)
    ```

## Usage

The bot operates by parsing a specially formatted Telegram message link.

### 1. Calculate Chat Size

To calculate the total size of all media in a chat, send the URL of the last message in that chat.

**Example (all messages):**

https://t.me/c/180763750/915

You can also specify a starting message ID to calculate the size of a specific range of messages.

**Example (from message `10` to `91`):**

https://t.me/c/180763750/91_10

### 2. Forward Messages

The bot can also be used as a forwarder to send messages from one chat to another.

The command structure is as follows:

`{SOURCE_LAST_MESSAGE_URL}_{TARGET_CHAT_ID}_{SOURCE_FIRST_MESSAGE_ID}`

* `SOURCE_LAST_MESSAGE_URL`: The URL of the **last message** in the desired range from the source chat.  
* `TARGET_CHAT_ID`: The ID of the channel or group where the messages will be forwarded.  
* `SOURCE_FIRST_MESSAGE_ID`: (Optional) The ID of the **first message** in the range you want to forward.

**Example Scenario:**

Imagine you want to forward all messages from message ID `20214` to `20378` from a source channel (`-1001854653008`) to a target channel (`-1003169274606`).

To execute this, you would send the following command to the bot:

https://t.me/c/1854653008/20378_-1003169274606_20214

The bot will then start forwarding all messages from message ID `20214` to `20378` to the target channel.

### 3. Filtering by Media Type

When forwarding a range of messages, you can choose to forward only specific types of media by adding a `--filter` flag. This is useful for migrating only videos, documents, or any other media type.

**Command Structure:**

`{FORWARDING_COMMAND} --filter {media_type_1},{media_type_2}`

**Available Media Types:**
* `photo`
* `document`
* `video`
* `sticker`
* `audio`
* `voice`
* `video_note`
* `animation`

**Example:**

To forward only the **videos** and **documents** from the previous example, you would modify the command like this:

https://t.me/c/1854653008/20378_-1003169274606_20214 --filter video,document

The bot will now skip all other message types (like text, photos, audio, etc.) and only forward the videos and documents in that range.

## Configuration

The bot is configured using environment variables. The following variables are required:

* `BOT_TOKEN`: Your Telegram bot token.  
* `APP_ID`: Your Telegram App ID.  
* `API_HASH`: Your Telegram API Hash.  

The following variables are optional:

* `AUTH_IDS`: A space-separated list of user or group IDs that are authorized to use the bot. If you want to make the bot public, leave this variable empty or set it to `0`.  
* `OWNER_ID`: The ID of the bot's owner.  
* `CHANNEL_OR_CONTACT`: A link to your channel or contact.  
* `FORCE_SUBSCRIBE_CHANNEL`: The ID or username of a channel that users must subscribe to before they can use the bot.  
* `PROGRESSBAR_LENGTH`: The length of the progress bar.  
* `FINISHED_PROGRESS_STR`: The character to use for the finished portion of the progress bar.  
* `UN_FINISHED_PROGRESS_STR`: The character to use for the unfinished portion of the progress bar.  
* `JOIN_CHANNEL_STR`: The message to send to users who have not yet joined the forced subscription channel.  
* `YOU_ARE_BANNED_STR`: The message to send to banned users.  
* `JOIN_BUTTON_STR`: The text for the "Join Channel" button.  

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
