import os
import sys
import logging
import argparse
import shutil
from trender import TRender
try:
    import colorlog
except ImportError:
    pass

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BUILD_DIR = os.path.join(CURRENT_DIR, 'build')
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')

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

def rmcontent(path):
    for name in map(lambda n: os.path.join(path, n), os.listdir(path)):
        if os.path.isdir(name):
            shutil.rmtree(name)
        elif os.path.isfile(name):
            os.unlink(name)


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Build in debug mode')
    parser.add_argument(
        '-l', '--log-level',
        default='info',
        help='set the log level',
        choices=['debug', 'info', 'warning', 'error'])
    args = parser.parse_args()

    args.debug = True

    setup_logger(args)

    if os.path.isdir(BUILD_DIR):
        logging.info('Empty existing build folder: {}...'.format(BUILD_DIR))
        rmcontent(BUILD_DIR)
    else:
        logging.info('Create build folder: {}...'.format(BUILD_DIR))
        os.mkdir(BUILD_DIR)

    logging.info('Create index.html...')
    template = TRender('base.template', os.path.join(CURRENT_DIR, 'templates'))
    with open(os.path.join(BUILD_DIR, 'index.html'), 'w', encoding='utf8') as f:
        f.write(template.render({'debug': args.debug}))

    logging.info('Copying website images...')
    shutil.copytree(os.path.join(STATIC_DIR, 'img'), os.path.join(BUILD_DIR, 'img'))

    logging.info('Copying website stylesheets...')
    shutil.copytree(os.path.join(STATIC_DIR, 'css'), os.path.join(BUILD_DIR, 'css'))

    logging.info('Copying website javascript files...')
    shutil.copytree(os.path.join(STATIC_DIR, 'js'), os.path.join(BUILD_DIR, 'js'))

    logging.info('Copying favicon...')
    shutil.copy(os.path.join(STATIC_DIR, 'favicon.ico'), os.path.join(BUILD_DIR, 'favicon.ico'))

    logging.info('Copying json data...')
    shutil.copy(os.path.join(STATIC_DIR, 'portfolio.json'), os.path.join(BUILD_DIR, 'portfolio.json'))
