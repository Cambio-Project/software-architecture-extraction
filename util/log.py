import sys
import inspect
import logging
import traceback

DEBUG = False;
FORMATTED_LOGGING = True

USE_STYLE = FORMATTED_LOGGING
RESET, BOLD = '\033[0m', '\033[1m'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, DEFAULT, WHITE = [30, 31, 32, 33, 34, 35, 36, 39, 97]

logger = logging.getLogger('HAZARD')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '{0}{1} [{2}] | {3}{4}: {5}{6}'.format(
        BOLD if USE_STYLE else '',
        '%(asctime)s',
        '%(_filename)s:L%(_lineno) 5d',
        '%(color)s',
        '%(levelname)-8s',
        '%(message)s',
        RESET if USE_STYLE else ''),
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
logger.addHandler(handler)


def fmt(color=WHITE):
    frame = inspect.getouterframes(inspect.currentframe())[2]
    file = frame[1].replace('\\', '/')
    file = file[file.rfind('/') + 1:]
    line = frame[2]
    return {'_filename': file, '_lineno': line, 'color': '\033[{}m'.format(color) if USE_STYLE else ''}


def pretty_print(*what):
    return ', '.join(map(str, what))


def debug(*what):
    logger.debug(pretty_print(*what), extra=fmt(GREEN))


def info(*what):
    logger.info(pretty_print(*what), extra=fmt(CYAN))


def warning(*what):
    logger.warning(pretty_print(*what), extra=fmt(YELLOW))


def error(*what):
    logger.error(pretty_print(*what), extra=fmt(RED))


def critical(*what):
    logger.critical(pretty_print(*what), extra=fmt(MAGENTA))


def tb(e: BaseException) -> str:
    """
    Creates a traceback message.
    @param e: Latest thrown exception
    @return: A string containing the latest exception and the object causing it.
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    msg = 'Exception: "{}" of type "{}" for object "{} ({})"\n{}'
    return msg.format(e, exc_type, exc_tb, type(exc_tb), traceback.format_exc())
