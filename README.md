# ChatSizeBot

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

ChatSizeBot is a powerful and versatile Telegram bot that calculates the total size of files in a channel or group. It is designed to be easy to use, with a straightforward command interface and clear, concise instructions.

## Features

*   **Task Queue**: Manages multiple requests efficiently, ensuring smooth and reliable performance.
*   **Public and Private Chat Support**: Works seamlessly in both public and private chats.
*   **Comprehensive File Type Support**: Calculates the total size of documents, videos, audio files, photos, animations, voice messages, and video notes.
*   **Real-Time Progress Updates**: Keeps you informed with a real-time progress bar.
*   **Flexible Authentication**: Can be configured to serve all users or be restricted to a specific set of authorized users.
*   **Forced Subscription**: Can be set up to require users to subscribe to a designated channel before they can use the bot.
*   **Server Statistics**: Provides detailed server statistics and dyno usage for Heroku deployments.

## Getting Started

### Prerequisites

*   A Telegram account
*   A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Installation

1.  **Deploy to Render**: Click the "Deploy to Render" button above to deploy the bot to Render.
2.  **Set Environment Variables**: In the Render dashboard, go to the "Environment" section and add the environment variables listed in the "Configuration" section below.
3.  **Set Bot Commands**: In Telegram, open a chat with [@BotFather](https://t.me/BotFather), select your bot, and use the `/setcommands` command to add the following commands:

    ```
    start - bot help
    ping - check bot online status
    stats - bot statistics
    shell - execute shell command (admin only)
    log - send bot logs (admin only)
    ```

## Usage

### Chat Size Calculator

To calculate the size of a chat, simply send the URL of the last message in the chat to the bot.

**Example:**

```
https://t.me/c/180763750/915
```

You can also specify a starting message ID to calculate the size of a specific range of messages.

**Example:**

```
https://t.me/c/180763750/91_10
```

### Forwarder

The bot can also be used as a forwarder to send messages from one chat to another.

**Example:**

```
https://t.me/c/180763750/915_-100110678269
```

## Configuration

The bot is configured using environment variables. The following variables are required:

*   `BOT_TOKEN`: Your Telegram bot token.
*   `APP_ID`: Your Telegram App ID.
*   `API_HASH`: Your Telegram API Hash.

The following variables are optional:

*   `AUTH_IDS`: A space-separated list of user or group IDs that are authorized to use the bot. If you want to make the bot public, leave this variable empty or set it to `0`.
*   `OWNER_ID`: The ID of the bot's owner.
*   `CHANNEL_OR_CONTACT`: A link to your channel or contact.
*   `FORCE_SUBSCRIBE_CHANNEL`: The ID or username of a channel that users must subscribe to before they can use the bot.
*   `PROGRESSBAR_LENGTH`: The length of the progress bar.
*   `FINISHED_PROGRESS_STR`: The character to use for the finished portion of the progress bar.
*   `UN_FINISHED_PROGRESS_STR`: The character to use for the unfinished portion of the progress bar.
*   `JOIN_CHANNEL_STR`: The message to send to users who have not yet joined the forced subscription channel.
*   `YOU_ARE_BANNED_STR`: The message to send to banned users.
*   `JOIN_BUTTON_STR`: The text for the "Join Channel" button.

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
