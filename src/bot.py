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
        text= 'سلام به ربات تلگرامی رهگیری مرسولات پستی شرکت ملی پست ایران خوش آمدید.\n برای رهگیری بسته پستی خود، لطفا کد رهگیری تان را ارسال نمایید.'
    )   
    await main()

async def main():
    code = input("Enter the code : ")
    async with AsyncClient() as client:
        try:
            data = await get_tracking_post(client=client, tracking_code=code)
            print(data)
        except TrackingNotFoundError as e:
            print(e)


if __name__ == '__main__':
    # print('in main')                              
    app = ApplicationBuilder().token(token= settings.bot_token).proxy(proxy= 'socks5://127.0.0.1:2080').build()
    startHandler = CommandHandler(command= 'start', callback= start)
    app.add_handlers(
        [
            startHandler,
        ]
    )

    logging.info('bot starting')
    # print('bot running')
    app.run_polling()

    # asyncio.run(main())
