"""
logging handling module to create custom and particular loggers.
"""

import logging
from typing import Literal

from colorlog.formatter import ColoredFormatter

from src.settings import settings


class ColorfulFormatter(ColoredFormatter):
    pass


def get_logger(
    name: str = settings.app_name,
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    | None = settings.log_level,
) -> logging.Logger:
    """
    get a logger object.

    Args:
        name (:obj:`str`, optional): Specify a name if you want
            to retrieve a logger.
        log_level (:obj:`str`, optional): Specify the log level
            for this particular logger.

    Returns:
        The logger.
    """

    # create logger
    logger = logging.getLogger(name=name)
    # set log level
    if log_level is not None:
        logger.setLevel(log_level)

    # set logger handler and formating
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorfulFormatter(
            fmt=settings.logging_format,
            style="{",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )
    logger.addHandler(handler)

    return logger
