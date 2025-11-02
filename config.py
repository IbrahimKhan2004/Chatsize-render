# https://huzunluartemis.github.io/ChatSizeBot/

import os



class Config:
    
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    APP_ID = int(os.environ.get('APP_ID', 1111111))
    API_HASH = os.environ.get('API_HASH', '')
    AUTH_IDS = [int(x) for x in os.environ.get("AUTH_IDS", "0").split()] # if open to everyone give 0
    OWNER_ID = int(os.environ.get('OWNER_ID', 0)) # give your owner id # if given 0 shell will not works
    FORCE_SUBSCRIBE_CHANNEL = os.environ.get('FORCE_SUBSCRIBE_CHANNEL','') # force subscribe channel link.
    CHANNEL_OR_CONTACT = os.environ.get('CHANNEL_OR_CONTACT', "xTnmgbR6rjgCDF7iPoFfiN8YfBsez9Lv") # give your public channel or contact username

    HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY', "")
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', "")

    # customisations
    FINISHED_PROGRESS_STR = os.environ.get('FINISHED_PROGRESS_STR','●')
    UN_FINISHED_PROGRESS_STR = os.environ.get('UN_FINISHED_PROGRESS_STR','○')
    PROGRESSBAR_LENGTH = int(os.environ.get('PROGRESSBAR_LENGTH', 25))
    JOIN_CHANNEL_STR = os.environ.get('JOIN_CHANNEL_STR',
        "Merhaba / Hi {}\n\n" + \
        "🇬🇧 First subscribe my channel from button, try again.\n" + \
        "🇹🇷 Önce butondan kanala abone ol, tekrar dene.")
    YOU_ARE_BANNED_STR = os.environ.get('YOU_ARE_BANNED_STR',
        "🇬🇧 You are Banned to use me.\n🇹🇷 Banlanmışsın ezik.\n\nDestek / Support: {}")
    JOIN_BUTTON_STR = os.environ.get('JOIN_BUTTON_STR', "🇬🇧 Join / 🇹🇷 Katıl")

    # fixing vars
    if (
        FORCE_SUBSCRIBE_CHANNEL == ""
        or FORCE_SUBSCRIBE_CHANNEL == " "
        or not str(FORCE_SUBSCRIBE_CHANNEL)
    ): FORCE_SUBSCRIBE_CHANNEL = None # bu satıra dokunmayın.
    if HEROKU_API_KEY  == "" or HEROKU_API_KEY == " " or len(HEROKU_API_KEY) == 0: HEROKU_API_KEY = None # bu satıra dokunmayın.
    if HEROKU_APP_NAME  == "" or HEROKU_APP_NAME == " " or len(HEROKU_APP_NAME) == 0: HEROKU_APP_NAME = None # bu satıra dokunmayın.
