import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(name)s - %(levelname)s - %(asctime)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)
handler.setFormatter(formatter)

logger.addHandler(handler)
