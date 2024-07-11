from post_tracker.utils import HourMinute, TrackingResult

from src.messages import TRACKING_STATUS


def time_to_str(time: HourMinute) -> str:
    # TODO: implement this to post-tracker library
    return f"{time.hour:02}:{time.hour:02}"


def create_tracking_message(tracking_info: TrackingResult) -> str:
    messages = [
        TRACKING_STATUS.format(
            date=ts.date,
            time=time_to_str(ts.time),
            location=ts.location,
            status=ts.status,
        )
        for ts in tracking_info.tracking_list
    ]
    message = "\n------------------\n".join(messages)

    return message
