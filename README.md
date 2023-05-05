## ChatSizeBot

🇹🇷 Telegram Kanal / Grup boyutu hesaplayıcı bot

🇬🇧 Telegram Channel / Group size calculator bot

Demo in telegram: [@ChatSizeBot](https://t.me/ChatSizeBot)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/HuzunluArtemis/ChatSizeBot)

## Features

- Task Quee
- Public, private chats
- Calculates: `document, video, audio, photo, animation, voice, video_note`
- Progress
- Auth users or public
- Force Subscribe
- Server stats & Dyno usage for heroku. Use: /stats
- Logger, Pinger, Shell executer

## Bot Commands (Set in [@BotFather](https://t.me/BotFather))

```
start - bot help
ping - check bot online status
stats - bot statistics
shell - execute shell command ❗ admin only
log - send bot logs ❗ admin only
```
## usage

forworder function(with chat size)

   last-Msg-url-of-source-chat_target-chat-id_first-msg-id(default1)
   
          https://t.me/c/180763750/915_-100110678269_800 
      
   first messege id maybe omitted
   
          https://t.me/c/180763370/200_-100181067869
      
      
chat size calculater

   normally
   
   last-Msg-url-of-source-chat
   
   ex-```https://t.me/c/180763750/915```
   
   with first msg id
   
   last-Msg-url-of-source-chat_first-msg-id_first-msg-id
   
   ex-```https://t.me/c/180763750/91_10_10```
   
   
   
## Environment Variables

- `BOT_TOKEN`: Telegram Bot Token. Example: `3asd2a2sd32:As56das65d2as:ASd2a6s3d26as`
- `APP_ID`: Telegram App ID. Example: `32523453`
- `API_HASH`: Telegram Api Hash. Example: `asdasdas6d265asd26asd6as1das`
- `AUTH_IDS`: Auth only some groups or users. If you want public, leave it empty or give `0`. Example: `-100656 56191 -10056561`
- `OWNER_ID`: Bot's owner id. Send `/id` to `t.me/MissRose_bot` in private to get your id.
- `HEROKU_API_KEY`: For dyno usage in /stats - Optional.
- `HEROKU_APP_NAME`: For dyno usage in /stats - Optional.
- `CHANNEL_OR_CONTACT`: your users contact link. give your username. example: HuzunluArtemis
- `FORCE_SUBSCRIBE_CHANNEL`: forcesub channel. optional. give channel id like `-1006616516165` or channel username like `HuzunluArtemis`
- You can use heroku-18, 20, 22 or docker deploy.
- `PROGRESSBAR_LENGTH`: Progressbar length. See `config.py`.
- `FINISHED_PROGRESS_STR`: Finished Progress Char. Default: `●`
- `UN_FINISHED_PROGRESS_STR`: Unfinished Progress Char. Default: `○`
- `JOIN_CHANNEL_STR`: Join channel warning string. See `config.py`.
- `YOU_ARE_BANNED_STR`: Banned user string. See `config.py`.
- `JOIN_BUTTON_STR`: Join button string. See `config.py`.

## Lisans

![](https://www.gnu.org/graphics/gplv3-127x51.png)

You can use, study share and improve it at your will. Specifically you can redistribute and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
