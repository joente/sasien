import os
import re
import signal
from PIL import Image

MONTHS_MAP = (
    'januari',
    'februari',
    'maart',
    'april',
    'mei',
    'juni',
    'juli',
    'augustus',
    'september',
    'oktober',
    'november',
    'december')

def month(date):
    return MONTHS_MAP[date.month-1]

def resized_img(img, maxwidth, maxheight=None, crop=False):
    if isinstance(img, str):
        img = Image.open(img)

    wpercent = maxwidth / float(img.size[0])
    wsize, hsize = maxwidth, int(float(img.size[1]) * float(wpercent))

    if (not crop and maxheight and hsize > maxheight) or (crop and maxheight and hsize < maxheight):
        hpercent = maxheight / float(img.size[1])
        wsize, hsize =int(float(img.size[0]) * float(hpercent)), maxheight

    return img.resize((wsize, hsize), Image.ANTIALIAS)


def htmlname(name, filter_chars=re.compile('[^a-zA-Z0-9_\-]')):
    name = name.lower().replace(' ', '-').replace('_', '-')
    return filter_chars.sub('', name)

# alias for htmlname
filename = htmlname


def get_input(default):
    return input('[{}] {}'.format(default, '> ') if default is not None else '> ').strip()


def ask_string(title, default=None, func=lambda x: None):
    print('\n',
          title,
          '(druk op enter voor de default waarde)' if default is not None else '')
    while True:
        inp = get_input(default)
        if not inp:
            inp = default
        try:
            func(inp)
        except Exception as e:
            print('\n{}'.format(e))
        else:
            return inp


def _signal_handler(s, f):
    exit('\nJe hebt op ctrl+c gedrukt, dag dag!\n')


def handlectrlc(handler=_signal_handler):
    # Add ctrl+c to quit
    signal.signal(signal.SIGINT, handler)


def approx(expecting, value, delta=1):
    return not bool(abs(expecting - value) // (1 + delta))
