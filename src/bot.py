from post_tracker.errors import TrackingNotFoundError

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    error,
)

from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from src.deps import PostTrackerWrapper
from src.settings import settings
from src.utils import create_tracking_message, persian_to_en_numbers
from src.logger import get_logger
from src import messages

# ------------------------------
logger = get_logger(name="post-tracker-bot")


# function handler
async def start_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("start command received.")
    await update.message.reply_text(
        text=messages.START_MESSAGE,
        reply_to_message_id=update.message.id,
    )


async def tracking_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    # check the code
    code: str = update.message.text
    code = persian_to_en_numbers(text=code)
    if not code.isdigit():
        # invalid code
        logger.debug(f"invalid tracking code number : {code}")
        await update.message.reply_text(
            text=messages.INVALID_CODE,
            reply_to_message_id=update.message.id,
        )
        return
    # send waiting message
    wait_msg = await update.message.reply_text(
        text=messages.WAITING_MESSAGE,
        reply_to_message_id=update.message.id,
    )

    try:
        logger.info(f"start get tracking data for code : {code}")
        tracker_app = post_tracker_wrapper()
        # get data from post-tracker
        tracking_data = await tracker_app.get_tracking_post(tracking_code=code)
        logger.info(f"tracking data for code : {code} received successfully !")
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
        await wait_msg.edit_text(
            text=create_tracking_message(tracking_info=tracking_data),
            reply_markup=reply_markup,
        )
    except TrackingNotFoundError:
        logger.debug(f"tracking data for code : {code} not found !")
        await wait_msg.edit_text(text=messages.TRACKING_NOT_FOUND)
    except Exception:
        # unhandled error
        logger.exception("getting tracking data raised an error :")
        await wait_msg.edit_text(
            text=messages.UNHANDLED_ERROR,
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
        logger.info(f"update tracking data for code : {tracking_code}")
        tracker_app = post_tracker_wrapper()
        # get data from post-tracker
        tracking_data = await tracker_app.get_tracking_post(tracking_code=tracking_code)
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
        logger.info(
            "tracking state did not changed (editing the message raised Bad Request)"
        )
        await query.answer(messages.ALERT_UPDATE_NOT_MODIFIED, show_alert=True)

    except Exception:
        # unhandled error
        logger.exception("updating tracking data raised an error :")
        await query.answer(messages.ALERT_UPDATE_ERROR, show_alert=True)


async def startup_handler(_: Application) -> None:
    logger.info("starting PostTracker app ...")
    post_tracker_wrapper.start()


async def shutdown_hadnler(_: Application) -> None:
    logger.info("stoping PostTracker app ...")
    await post_tracker_wrapper.stop()


if __name__ == "__main__":
    # setup bot
    app = ApplicationBuilder().token(token=settings.bot_token)
    # set proxy
    if settings.proxy_url is not None:
        app.proxy(proxy=settings.proxy_url)
        app.get_updates_proxy(get_updates_proxy=settings.proxy_url)

    # startup and shutdown handlers
    post_tracker_wrapper = PostTrackerWrapper()
    app.post_init(startup_handler)
    app.post_shutdown(shutdown_hadnler)
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

    logger.info("bot starting")
    app.run_polling()
