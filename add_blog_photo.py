#!/usr/bin/python3.5
import os
import re
import argparse
import signal
import datetime
import configparser
import logging
import helpers


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PHOTO_DIR = os.path.join(CURRENT_DIR, 'blog', 'photos')
BLOG_IMAGE_WIDTH = 939


def get_name(photo):
    name = helpers.filename(os.path.splitext(os.path.basename(photo))[0])
    if not name:
        raise ValueError('Sorry, kun je de foto een andere naam geven? van deze naam snap ik niets...')
    return name


def check_photo(photo):
    if not photo:
        raise ValueError('Een foto heeft je blog echt nodig!')

    if not os.path.isfile(photo):
        raise ValueError('Sorry, ik kan foto {!r} niet vinden!'.format(photo))

    if not photo.lower().endswith('.jpg'):
        raise ValueError('Sorry, ik span alleen .jpg foto\'s!')

    get_name(photo)


def add_photo(args):
    photo_index = helpers.load_photo_index(path=PHOTO_DIR)
    jpgfile = '{}.jpg'.format(os.path.join(
        PHOTO_DIR,
        helpers.unique(get_name(args.photo), photo_index)))

    if os.path.isfile(jpgfile):
        os.unlink(jpgfile)

    helpers.save_photo_index(photo_index, path=PHOTO_DIR)

    img = helpers.resized_img(fn=args.photo, maxwidth=BLOG_IMAGE_WIDTH)
    img.save(jpgfile)

    print('Je kunt de foto gebruiken met {}'.format(helpers.color_yellow('![Title]({})'.format(
        os.path.join('/', 'img', 'blog', os.path.basename(jpgfile))))))


if __name__ == '__main__':
    helpers.handlectrlc()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p',
        '--photo',
        type=str,
        default='',
        help='Blog (title) photo')

    args = parser.parse_args()

    try:
        check_photo(args.photo)
    except:
        args.photo = helpers.ask_string(
            title='Type de locatie van de foto die je wilt gebruiken voor je nieuwe blog post',
            default='src/blog.jpg',
            func=check_photo)

    add_photo(args)

    input()