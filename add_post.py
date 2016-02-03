#!/usr/bin/python3.5
import os
import re
import argparse
import signal
import datetime
import configparser
import helpers

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BLOG_DIR = os.path.join(CURRENT_DIR, 'blog')
PHOTO_DIR = os.path.join(BLOG_DIR, 'photos')
BLOG_GALLERY_IMAGE_WIDTH = 317
BLOG_GALLERY_IMAGE_HEIGHT = 211
FB_IMAGE_WIDTH = 1200


def get_blog_files(title):
    filename = helpers.filename(title)

    if not filename:
        raise ValueError('Hmm, we kunnen geen juiste bestanden maken voor titel: {!r}'.format(title))

    metafile = os.path.join(BLOG_DIR, '{}.meta'.format(filename))
    mdfile = os.path.join(BLOG_DIR, '{}.md'.format(filename))
    jpgfile = os.path.join(BLOG_DIR, 'photos', '{}.jpg'.format(filename))
    fbimage = os.path.join(BLOG_DIR, 'fb', '{}.jpg'.format(filename))

    return metafile, mdfile, jpgfile, fbimage, filename


def check_title(title):
    if not title:
        raise ValueError('Een titel is echt nodig!')

    for fn in get_blog_files(title):
        if os.path.exists(fn):
            raise ValueError('Bestand {!r} bestaat al!'.format(fn))


def check_description(description):
    if not description:
        raise ValueError('Een omschrijving is echt nodig!')


def check_photo(photo):
    if not photo:
        raise ValueError('Een foto heeft je blog echt nodig!')

    if not os.path.isfile(photo):
        raise ValueError('Sorry, ik kan foto {!r} niet vinden!'.format(photo))

    if not photo.lower().endswith('.jpg'):
        raise ValueError('Sorry, ik span alleen .jpg foto\'s!')

    img = helpers.resized_img(img=photo, maxwidth=BLOG_GALLERY_IMAGE_WIDTH)
    if not helpers.approx(BLOG_GALLERY_IMAGE_HEIGHT, img.size[1]):
        raise ValueError('Sorry, de foto moet een verhouding hebben van 3x2 en deze foto is {}x{}!'.format(img.size[0], img.size[1]))

def check_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except:
        raise ValueError('Ik verwacht een datum zoals de verjaardag van ons Iriske: 2013-02-06')


def create_post(args):
    metafile, mdfile, jpgfile, fbimage, name = get_blog_files(args.title)

    date = datetime.datetime.strptime(args.date, '%Y-%m-%d')

    with open(mdfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join([args.title, '=' * len(args.title), '', '###{} {} {}'.format(
            date.day, helpers.month(date), date.year)]))

    post_img = helpers.resized_img(img=args.photo, maxwidth=BLOG_GALLERY_IMAGE_WIDTH)
    post_img.save(jpgfile)

    fb_img = helpers.resized_img(img=args.photo, maxwidth=FB_IMAGE_WIDTH)
    fb_img.save(fbimage)

    config = configparser.RawConfigParser()
    config['blog_post'] = {
        'name': name,
        'title': args.title,
        'date': args.date,
        'photo': os.path.basename(jpgfile),
        'content': os.path.basename(mdfile),
        'fb-title': args.title,
        'fb-description': args.description,
        'fb-image': os.path.basename(fbimage),
        'fb-image-type': 'image/jpeg',
        'fb-image-width': fb_img.size[0],
        'fb-image-height': fb_img.size[1]
    }

    with open(metafile, 'w', encoding='utf-8') as f:
        config.write(f)

    os.mkdir(os.path.join(BLOG_DIR, 'photos', name))

    print('Finished creating blog \'{}\''.format(args.title))


if __name__ == '__main__':
    helpers.handlectrlc()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--title',
        type=str,
        default='',
        help='Blog titel')

    parser.add_argument(
        '-i',
        '--description',
        type=str,
        default='',
        help='Blog description (facebook)')

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
        args.title = helpers.ask_string(
            title='Type een titel voor je nieuwe blog post',
            func=check_title)

    try:
        check_description(args.description)
    except:
        args.description = helpers.ask_string(
            title='Type een omschrijving (voor facebook)',
            func=check_description)

    try:
        check_date(args.date)
    except:
        args.date = helpers.ask_string(
            title='Type een datum voor je nieuwe blog post',
            default=str(datetime.date.today()),
            func=check_date)

    try:
        check_photo(args.photo)
    except:
        args.photo = helpers.ask_string(
            title='Type de locatie van de foto die je wilt gebruiken voor je nieuwe blog post',
            default='src/blog.jpg',
            func=check_photo)

    create_post(args)