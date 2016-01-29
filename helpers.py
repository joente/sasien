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

def resized_img(fn, maxwidth, maxheight=None, crop=False):
    img = Image.open(fn)

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


def unique(name, index):
    out = name
    num = 0
    while out in index:
        out = '{}-{}'.format(name, num)
        num += 1
    index.add(out)
    return out


def color_blue(s):
    # '\033[94m{}\x1b[0m'.format(s)
    return s


def color_yellow(s):
    # '\x1b[33m{}\x1b[0m'.format(s)
    return s


def get_input(default):
    return input('[{}] {}'.format(color_yellow(default), '> ') if default is not None else '> ').strip()


def ask_string(title, default=None, func=lambda x: None):
    print('\n',
          color_blue(title),
          '(druk op enter voor de default waarde)' if default is not None else '')
    while True:
        inp = get_input(default)
        if not inp:
            inp = default
        try:
            func(inp)
        except Exception as e:
            print('\n{}'.format(color_blue(e)))
        else:
            return inp


def _signal_handler(s, f):
    exit('\nJe hebt op ctrl+c gedrukt, dag dag!\n')


def handlectrlc(handler=_signal_handler):
    # Add ctrl+c to quit
    signal.signal(signal.SIGINT, handler)


def load_photo_index(path):
    with open(os.path.join(path, '.index'), 'r', encoding='utf8') as f:
        content = f.read()
    return set(content.splitlines())


def save_photo_index(index, path):
    with open(os.path.join(path, '.index'), 'w', encoding='utf8') as f:
        f.write('\n'.join(index))

def approx(expecting, value, delta=1):
    return not bool(abs(expecting - value) // (1 + delta))
