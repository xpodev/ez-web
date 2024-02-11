import sys
import logging

colors = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'blue': '\033[94m',
    'end': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m',
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def _style(msg, *styles):
    return ''.join(styles) + msg + colors['end']

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
