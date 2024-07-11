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
