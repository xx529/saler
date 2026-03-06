import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        (logger
         .opt(depth=6, exception=record.exc_info)
         .bind(name=record.name)
         .log(record.levelname, record.getMessage()))


logger.remove()

short_format = (
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> '
    '<magenta>[{extra[name]}]</magenta> '
    '<level>[{level}]</level> '
    '<magenta>{file.name}</magenta>:<yellow>{line}</yellow> '
    '- '
    '{message}'
)

logger.configure(
    handlers=[
        dict(
            sink=sys.stdout,
            enqueue=True,
            format=short_format,
            colorize=True,
            level='INFO',
        )
    ]
)


def get_logger(name: str = 'default'):
    return logger.bind(name=name)

