from post_tracker.utils import TrackingResult

from src.messages import TRACKING_STATUS


def create_tracking_message(tracking_info: TrackingResult) -> str:
    messages = [
        TRACKING_STATUS.format(
            date=ts.date,
            time=ts.time,
            location=ts.location,
            status=ts.status,
        )
        for ts in tracking_info.tracking_list
    ]
    message = "\n------------------\n".join(messages)

    return message


def persian_to_en_numbers(text: str) -> str:
    persian = [
        "۰",
        "۱",
        "۲",
        "۳",
        "۴",
        "۵",
        "۶",
        "۷",
        "۸",
        "۹",
    ]
    english = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]
    # convert persian to english digits
    for i in range(len(persian)):
        text = text.replace(persian[i], english[i])

    return text
