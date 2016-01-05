#!/usr/bin/python3.5
import os
import re
import argparse
import signal
import datetime
import configparser
import logging
from PIL import Image


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BLOG_DIR = os.path.join(CURRENT_DIR, 'blog')
BLOG_GALLERY_IMAGE_WIDTH = 317

def color_blue(s):
    return '\033[94m{}\x1b[0m'.format(s)


def color_yellow(s):
    return '\x1b[33m{}\x1b[0m'.format(s)


def get_input(default):
    return input('[{}] {}'.format(color_yellow(default), '> ') if default is not None else '> ').strip()


def get_blog_files(title):
    filename = title.lower().replace(' ', '_')

    filter_chars = re.compile('[^a-zA-Z0-9_]')
    filename = filter_chars.sub('', filename)

    if not filename:
        raise ValueError('Hmm, we kunnen geen juiste bestanden maken voor titel: {!r}'.format(title))

    metafile = os.path.join(BLOG_DIR, '{}.meta'.format(filename))
    mdfile = os.path.join(BLOG_DIR, '{}.md'.format(filename))
    jpgfile = os.path.join(BLOG_DIR, '{}.jpg'.format(filename))

    return metafile, mdfile, jpgfile


def resized_img(fn, maxwidth, maxheight=None, crop=False):
    img = Image.open(fn)

    wpercent = maxwidth / float(img.size[0])
    wsize, hsize = maxwidth, int(float(img.size[1]) * float(wpercent))

    if (not crop and maxheight and hsize > maxheight) or (crop and maxheight and hsize < maxheight):
        hpercent = maxheight / float(img.size[1])
        wsize, hsize =int(float(img.size[0]) * float(hpercent)), maxheight

    return img.resize((wsize, hsize), Image.ANTIALIAS)


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


def check_title(title):
    if not title:
        raise ValueError('Een titel is echt nodig!')

    for fn in get_blog_files(title):
        if os.path.exists(fn):
            raise ValueError('Bestand {!r} bestaat al!'.format(fn))


def check_photo(photo):
    if not photo:
        raise ValueError('Een foto heeft je blog echt nodig!')

    if not os.path.isfile(photo):
        raise ValueError('Sorry, ik kan foto {!r} niet vinden!'.format(photo))


def check_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except:
        raise ValueError('Ik verwacht een datum zoals de verjaardag van ons Iriske: 2013-02-06')


def signal_handler(s, f):
    exit('\nJe hebt op ctrl+c gedrukt, dag dag!\n')


def create_post(args):
    metafile, mdfile, jpgfile = get_blog_files(args.title)

    config = configparser.RawConfigParser()
    config['blog_post'] = {
        'Title': args.title,
        'Date': args.date,
        'Photo': jpgfile,
        'Content': mdfile
    }
    with open(metafile, 'w', encoding='utf-8') as f:
        config.write(f)

    with open(mdfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join([args.title, '=' * len(args.title)]))

    img = resized_img(fn=args.photo, maxwidth=BLOG_GALLERY_IMAGE_WIDTH)
    img.save(jpgfile)

    print('Finished creating blog \'{}\''.format(color_yellow(args.title)))



if __name__ == '__main__':
    # Add ctrl+c to quit
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--title',
        type=str,
        default='',
        help='Blog titel')

    parser.add_argument(
        '-d',
        '--date',
        type=str,
        default='',
        help='Blog datum')

    parser.add_argument(
        '-p',
        '--photo',
        type=str,
        default='',
        help='Blog (title) photo')

    args = parser.parse_args()

    try:
        check_title(args.title)
    except:
        args.title = ask_string(
            title='Type een titel voor je nieuwe blog post',
            func=check_title)

    try:
        check_date(args.date)
    except:
        args.date = ask_string(
            title='Type een datum voor je nieuwe blog post',
            default=str(datetime.date.today()),
            func=check_date)

    try:
        check_date(args.photo)
    except:
        args.photo = ask_string(
            title='Type de locatie van de foto die je wilt gebruiken voor je nieuwe blog post',
            default='src/blog.jpg',
            func=check_photo)

    create_post(args)