# logging_config.py
import logging

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Get a logger instance (optional, useful if you want a default logger)
logger = logging.getLogger(__name__)