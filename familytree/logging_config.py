import logging
from pathlib import Path


class ExtraFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "ip"):
            record.ip = "-"
        if not hasattr(record, "user_agent"):
            record.user_agent = "-"
        return super().format(record)


def get_structured_logger(
    name: str,
    filename: str,
    level: int = logging.INFO
) -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler(f"logs/{filename}", encoding="utf-8", mode="a")
        handler.setFormatter(
            ExtraFormatter(
                "%(asctime)s - [IP:%(ip)s] [UA:%(user_agent)s] - %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
    
    return logger


search_logger = get_structured_logger("familytree.searches", "searches.log")
feedback_logger = get_structured_logger("familytree.feedbacks", "feedbacks.log")
