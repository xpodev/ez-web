import sys
import logging


__priority__ = 100


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
