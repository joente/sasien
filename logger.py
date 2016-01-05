import sys
import logging
try:
    import colorlog
except ImportError:
    pass


_MAP_LOGLEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

_LOG_DATE_FMT = '%y%m%d %H:%M:%S'

def setup_logger(args):
    '''Setup logger.

    Positional arguments:
        args: usually an argparse object since we expect attributes like
        args.log_level etc.
    '''
    if 'colorlog' in sys.modules:
        # setup colorized formatter
        formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(levelname)1.1s %(asctime)s %(module)s' +
                ':%(lineno)d]%(reset)s %(message)s',
            datefmt=_LOG_DATE_FMT,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'},
            secondary_log_colors={},
            style='%')
    else:
        # setup formatter without using colors
        formatter = logging.Formatter(
            fmt='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] ' +
                '%(message)s',
            datefmt=_LOG_DATE_FMT,
            style='%')

    # create logger # TODO: Check if this is working
    logger = logging.getLogger()

    logger.setLevel(_MAP_LOGLEVELS[args.log_level.upper()])

    # create console handler
    ch = logging.StreamHandler()

    # we can set the handler level to DEBUG since we control the root level
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)