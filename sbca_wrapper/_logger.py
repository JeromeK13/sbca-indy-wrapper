import logging


# Create logger with custom configuration
def get_sbca_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        handler: logging.Handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(name)s | %(message)s'))
        logger.addHandler(handler)
        logger.propagate = False
    return logger
