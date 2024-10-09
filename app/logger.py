import logging
from logging.handlers import RotatingFileHandler
from .config import LOG_OUT_PATH, LOG_MAX_BYTES, LOG_BACKUP_COUNT, LOG_LEVEL
import sys

logger = logging.getLogger("api_logger")
logger.setLevel(LOG_LEVEL)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# console_handler = logging.StreamHandler(sys.stdout)  # Console output
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    LOG_OUT_PATH,
    maxBytes=LOG_MAX_BYTES,
    backupCount=LOG_BACKUP_COUNT
    )
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
