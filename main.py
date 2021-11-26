import api_only

if __name__ == '__main__':
    bot = api_only.TelegramBot()

    while True:
        bot.get_updates()
