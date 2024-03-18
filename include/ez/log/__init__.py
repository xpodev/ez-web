from .. import logger, _style, colors


def debug(*args, sep=' '):
    msg = sep.join(map(str, args))
    msg = f"{_style('DEBUG', colors['blue'])}:".ljust(19) + msg
    logger.debug(msg)

def info(*args, sep=' '):
    msg = sep.join(map(str, args))
    msg = f"{_style('INFO', colors['green'])}:".ljust(19) + msg
    logger.info(msg)

def warning(*args, sep=' '):
    msg = sep.join(map(str, args))
    msg = f"{_style('WARNING', colors['yellow'])}:".ljust(19) + msg
    logger.warning(msg)

def error(*args, sep=' '):
    msg = sep.join(map(str, args))
    msg = f"{_style('ERROR', colors['red'])}:".ljust(19) + msg
    logger.error(msg)

def critical(*args, sep=' '):
    msg = sep.join(map(str, args))
    msg = f"{_style('CRITICAL', colors['red'])}:".ljust(19) + msg
    logger.critical(msg)
