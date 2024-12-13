import logging
from logging import Logger


def configure_logger(
    name: str = __name__, log_file: str = None, level: int = logging.DEBUG
) -> Logger:
    """
    Configure and return a logger instance.

    Args:
        name (str): The name of the logger, defaults to the module name.
        log_file (str): Optional log file path. If provided, logs will also be saved to this file.
        level (int): Logging level, defaults to DEBUG.

    Returns:
        Logger: Configured logger instance.
    """
    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Define the log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # Configure file handler if a log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Example: Get a default logger
logger = configure_logger()

# Usage:
# You can now import and use `logger` or call `configure_logger` to create custom loggers
# logger.info("Logger is configured successfully!")
