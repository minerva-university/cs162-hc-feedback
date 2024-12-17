# logging_config.py
import logging

def get_logger(name):
    """Create and return a logger with the given name"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger

# Create and export a default logger
logger = get_logger('ai.default')

# Make sure both are available for import
__all__ = ['get_logger', 'logger']