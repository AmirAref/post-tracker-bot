from post_tracker.utils import get_tracking_post
from post_tracker.errors import TrackingNotFoundError
from httpx import AsyncClient
import asyncio
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
)
from src.settings import settings
# ------------------------------

logging.basicConfig(level= logging.INFO, format= '%(asctime)s - %(message)s')

# function handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text= 'سلام به ربات تلگرامی رهگیری مرسولات پستی شرکت ملی پست ایران خوش آمدید.\n برای رهگیری بسته پستی خود، لطفا کد رهگیری تان را ارسال نمایید.',
        reply_to_message_id=update.message.id
    )   

if __name__ == '__main__':
    # setup bot 
    app = ApplicationBuilder().token(token= settings.bot_token)
    # set proxy
    if settings.proxy_url is not None:
        app.proxy(proxy= settings.proxy_url)
        app.get_updates_proxy(get_updates_proxy=settings.proxy_url)
    # build bot
    app = app.build()
    # add handlers
    startHandler = CommandHandler(command= 'start', callback= start)
    app.add_handlers(
        (
            startHandler,
        )
    )

    logging.info('bot starting')
    app.run_polling()

