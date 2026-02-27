import logging
from pathlib import Path


class ExtraFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "ip"):
            record.ip = "-"
        if not hasattr(record, "user_agent"):
            record.user_agent = "-"
        return super().format(record)


def get_search_logger() -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("familytree.searches")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler("logs/searches.log", encoding="utf-8", mode="a")
        handler.setFormatter(
            ExtraFormatter(
                "%(asctime)s - [IP:%(ip)s] [UA:%(user_agent)s] - %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    return logger


search_logger = get_search_logger()
