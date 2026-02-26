import logging
from pathlib import Path


def get_search_logger() -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("familytree.searches")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler("logs/searches.log", encoding="utf-8", mode="a")
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        )
        logger.addHandler(handler)

    return logger


search_logger = get_search_logger()
