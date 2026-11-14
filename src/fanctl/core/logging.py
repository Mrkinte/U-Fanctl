from loguru import logger

from .paths import LOG_PATH


def setup_logging() -> None:
    logger.add(str(LOG_PATH), rotation="1 MB")
