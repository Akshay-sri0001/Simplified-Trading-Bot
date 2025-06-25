# logger_setup.py
import logging
import sys

def setup_logger():
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler
    fh = logging.FileHandler('trading_bot.log')
    fh.setLevel(logging.DEBUG) # Log more details to file
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Get the logger instance
log = setup_logger()