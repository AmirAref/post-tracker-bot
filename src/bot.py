from post_tracker.utils import get_tracking_post
from post_tracker.errors import TrackingNotFoundError
from httpx import AsyncClient
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    error,
)

from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
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
async def start_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=messages.START_MESSAGE,
        reply_to_message_id=update.message.id,
    )


async def tracking_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    # check the code
    code: str = update.message.text
    if not code.isdigit():
        # invalid code
        await update.message.reply_text(
            text=messages.INVALID_CODE,
            reply_to_message_id=update.message.id,
        )
        return

    try:
        # TODO : inject async client as a dependency
        async with AsyncClient() as client:
            # get data from post-tracker
            tracking_data = await get_tracking_post(client=client, tracking_code=code)
        # create reply keyboard markap
        keyboard = [
            [
                InlineKeyboardButton(
                    messages.UPDATE_BUTTON_TEXT,
                    callback_data=f"update_{update.message.text}",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text=create_tracking_message(tracking_info=tracking_data),
            reply_to_message_id=update.message.id,
            reply_markup=reply_markup,
        )
    except TrackingNotFoundError:
        await update.message.reply_text(
            text=messages.TRACKING_NOT_FOUND, reply_to_message_id=update.message.id
        )
    except Exception as e:
        # unhandled error
        logging.exception(e)
        await update.message.reply_text(
            text=messages.UNHANDLED_ERROR,
            reply_to_message_id=update.message.id,
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN,
        )


async def update_details_code_callbackquery(
    update: Update, _: ContextTypes.DEFAULT_TYPE
) -> None:
    # Parses the CallbackQuery and updates the message text.
    query = update.callback_query
    query_data = query.data
    if not query_data.startswith("update_"):
        return
    tracking_code = query_data.split("update_")[1]
    try:
        async with AsyncClient() as client:
            # get data from post-tracker
            tracking_data = await get_tracking_post(
                client=client, tracking_code=tracking_code
            )
        keyboard = [
            [
                InlineKeyboardButton(
                    messages.UPDATE_BUTTON_TEXT, callback_data=query_data
                )
            ]
        ]
        # create reply keyboard markap
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=create_tracking_message(tracking_info=tracking_data),
            reply_markup=reply_markup,
        )
        await query.answer(messages.ALERT_UPDATE_SUCCESS, show_alert=True)
    except TrackingNotFoundError:
        await query.answer(messages.TRACKING_NOT_FOUND)

    except error.BadRequest:
        # "Message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
        await query.answer(messages.ALERT_UPDATE_NOT_MODIFIED, show_alert=True)

    except Exception as e:
        # unhandled error
        logging.exception(e)
        await query.answer(messages.ALERT_UPDATE_ERROR, show_alert=True)


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
            CommandHandler(command="start", callback=start_callback),
            MessageHandler(
                filters=filters.TEXT & filters.ChatType.PRIVATE,
                callback=tracking_callback,
            ),
            CallbackQueryHandler(update_details_code_callbackquery),
        ]
    )

    logging.info("bot starting")
    app.run_polling()
