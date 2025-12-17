import logging
from logging.handlers import RotatingFileHandler
import os

# 1. Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 2. Log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 3. Create file handler
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3
)

# 4. Log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler.setFormatter(formatter)

# 5. Create logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# 6. Attach handler (avoid duplicate logs)
if not logger.handlers:
    logger.addHandler(file_handler)
