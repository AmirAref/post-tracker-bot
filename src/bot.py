from post_tracker.utils import get_tracking_post
from post_tracker.errors import TrackingNotFoundError
from httpx import AsyncClient
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from src.settings import settings
from src.utils import create_tracking_message
from src import messages

# ------------------------------
# TODO : setup custom logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


# function handler
async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text="سلام به ربات تلگرامی رهگیری مرسولات پستی شرکت ملی پست ایران خوش آمدید.\n برای رهگیری بسته پستی خود، لطفا کد رهگیری تان را ارسال نمایید.",
        reply_to_message_id=update.message.id,
    )


async def tracking_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    # check the code
    code: str = update.message.text
    if not code.isdigit() or len(code) != 24:
        # invalid code
        await update.message.reply_text(
            text=messages.INVALID_CODE, reply_to_message_id=update.message.id
        )
        return

    try:
        # TODO : inject async client as a dependency
        async with AsyncClient() as client:
            # get data from post-tracker
            tracking_data = await get_tracking_post(client=client, tracking_code=code)
        await update.message.reply_text(
            text=create_tracking_message(tracking_info=tracking_data),
            reply_to_message_id=update.message.id,
        )
    except TrackingNotFoundError:
        await update.message.reply_text(
            text=messages.TRACKING_NOT_FOUND, reply_to_message_id=update.message.id
        )
    except Exception as e:
        # unhandled error
        logging.exception(e)
        await update.message.reply_text(
            text=messages.UNHANDLED_ERROR, reply_to_message_id=update.message.id
        )


if __name__ == "__main__":
    # setup bot
    app = ApplicationBuilder().token(token=settings.bot_token)
    # set proxy
    if settings.proxy_url is not None:
        app.proxy(proxy=settings.proxy_url)
        app.get_updates_proxy(get_updates_proxy=settings.proxy_url)
    # build bot
    app = app.build()
    # add handlers
    app.add_handlers(
        [
            CommandHandler(command="start", callback=start),
            MessageHandler(
                filters=filters.TEXT & filters.ChatType.PRIVATE,
                callback=tracking_callback,
            ),
        ]
    )

    logging.info("bot starting")
    app.run_polling()
