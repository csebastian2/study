from logging import getLogger


logger = getLogger(__name__)


def debug(*args, **kwargs):
    logger.debug(kwargs)
