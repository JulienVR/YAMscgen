import logging

GREY = "\x1b[38;20m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
RESET = "\x1b[0m"

LEVEL_TO_COLOR = {
    logging.DEBUG: GREY,
    logging.INFO: GREEN,
    logging.WARNING: YELLOW,
    logging.ERROR: RED,
    logging.CRITICAL: RED,
}


class ColoredFormatter:

    def get_log_fmt(self, record):
        color = LEVEL_TO_COLOR.get(record.levelno)
        return "%(asctime)s - %(name)s - " + color + "%(levelname)s" + RESET + " - %(message)s (%(filename)s:%(lineno)d)"

    def format(self, record):
        log_fmt = self.get_log_fmt(record)
        return logging.Formatter(log_fmt).format(record)
