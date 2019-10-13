from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def main():
    from telegram import Bot
    from telegram.utils.request import Request
    
    import config
    
    req = Request(proxy_url=config.proxy)
    bot = Bot(config.token, request=req)
    upd = Updater(bot=bot, use_context=True)
    
    dp = upd.dispatcher
    
    upd.start_polling()
    upd.idle()
    
    
if __name__ == '__main__':
    main()
