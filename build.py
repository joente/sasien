#!/usr/bin/python3
import os
import logging
import argparse
import shutil
import markdown
import functools
from slimit import minify
from csscompressor import compress
from blogs import Blogs
from blog import Blog
from trender import TRender
from logger import setup_logger
from resize import resize
import helpers


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BUILD_DIR = os.path.join(CURRENT_DIR, 'build')
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')
DEBUG = False


def rmcontent(path):
    for name in map(lambda n: os.path.join(path, n), os.listdir(path)):
        if os.path.isdir(name):
            shutil.rmtree(name)
        elif os.path.isfile(name):
            os.unlink(name)


def min_js():
    #################################################
    # Minify app js
    #################################################

    content = []

    with open(os.path.join(STATIC_DIR, 'js', 'sasien.js'), 'r') as f:
        content.append(f.read())

    with open(os.path.join(STATIC_DIR, 'js', 'wall.js'), 'r') as f:
        content.append(f.read())

    with open(os.path.join(STATIC_DIR, 'js', 'gallery.js'), 'r') as f:
        content.append(f.read())

    with open(os.path.join(STATIC_DIR, 'js', 'app.js'), 'r') as f:
        content.append(f.read())

    with open(os.path.join(STATIC_DIR, 'js', 'router.js'), 'r') as f:
        content.append(f.read())

    with open(os.path.join(STATIC_DIR, 'js', 'app.min.js'), 'w') as f:
        f.write(minify(''.join(content), mangle=True, mangle_toplevel=True))


def min_css():
    #################################################
    # Minify css
    #################################################

    with open(os.path.join(STATIC_DIR, 'css', 'style.css'), 'r') as f:
        content = f.read()

    with open(os.path.join(STATIC_DIR, 'css', 'style.min.css'), 'w') as f:
        f.write(compress(content))


if __name__ == '__main__':
    trender = functools.partial(TRender, path=os.path.join(CURRENT_DIR, 'templates'))

    parser = argparse.ArgumentParser()

    if DEBUG:
        parser.add_argument(
            '-d', '--debug',
            action='store_false',
            help='Disable debug mode')
    else:
        parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help='Enable debug mode')

    parser.add_argument(
        '-l', '--log-level',
        default='info',
        help='set the log level',
        choices=['debug', 'info', 'warning', 'error'])
    args = parser.parse_args()

    setup_logger(args.log_level)

    logging.info('Resize images...')
    resize()

    if not args.debug:
        logging.info('Minify js files...')
        min_js()

        logging.info('Minify css files...')
        min_css()

    if os.path.isdir(BUILD_DIR):
        logging.info('Empty existing build folder: {}...'.format(BUILD_DIR))
        rmcontent(BUILD_DIR)
    else:
        logging.info('Create build folder: {}...'.format(BUILD_DIR))
        os.mkdir(BUILD_DIR)

    logging.info('Create blog folder...')
    os.mkdir(os.path.join(BUILD_DIR, 'blog'))

    logging.info('Create index.html...')
    template = trender('website.template')
    with open(os.path.join(BUILD_DIR, 'index.html'), 'w', encoding='utf8') as f:
        f.write(template.render({
            'debug': args.debug,
            'title': 'Sasien Photography'}))

    logging.info('Copying website images...')
    shutil.copytree(os.path.join(STATIC_DIR, 'img'), os.path.join(BUILD_DIR, 'img'))

    logging.info('Copying blog images...')
    shutil.copytree(os.path.join(CURRENT_DIR, 'blog', 'photos'), os.path.join(BUILD_DIR, 'img', 'blog'))

    logging.info('Copying facebook images...')
    shutil.copytree(os.path.join(CURRENT_DIR, 'blog', 'fb'), os.path.join(BUILD_DIR, 'img', 'fb'))

    logging.info('Copying website stylesheets...')
    shutil.copytree(os.path.join(STATIC_DIR, 'css'), os.path.join(BUILD_DIR, 'css'))

    logging.info('Copying website javascript files...')
    shutil.copytree(os.path.join(STATIC_DIR, 'js'), os.path.join(BUILD_DIR, 'js'))

    logging.info('Copying favicon...')
    shutil.copy(os.path.join(STATIC_DIR, 'favicon.ico'), os.path.join(BUILD_DIR, 'favicon.ico'))

    logging.info('Copying json data...')
    shutil.copy(os.path.join(STATIC_DIR, 'portfolio.json'), os.path.join(BUILD_DIR, 'portfolio.json'))

    logging.info('Load blogs...')
    path = os.path.join(CURRENT_DIR, 'blog')
    blogs = Blogs()
    for fn in map(lambda n: os.path.join(path, n), [fn for fn in os.listdir(path) if fn.endswith('.meta')]):
        blogs.add(Blog(fn))
    logging.info(blogs)

    gallery_blogs = [{
        'target': blog.target,
        'title': blog.title,
        'photo': blog.photo} for blog in blogs if not blog.name.startswith('_')]

    blog_gallery_template = trender('blog-gallery.template')
    with open(os.path.join(BUILD_DIR, 'blog', 'index.html'), 'w', encoding='utf8') as f:
        f.write(blog_gallery_template.render({
            'debug': args.debug,
            'blogs': gallery_blogs}))

    for blog in blogs:
        blog_template = trender('blog.template')
        blog.path = os.path.join(BUILD_DIR, 'blog', helpers.htmlname(blog.name))
        logging.info('create blog path: {}'.format(blog.path))
        os.mkdir(blog.path)
        with open(os.path.join(blog.path, 'index.html'), 'w', encoding='utf8') as f:
            f.write(blog_template.render({
                'debug': args.debug,
                'title': blog.title,
                'blog': blog.html,
                'description': blog.description,
                'fb': blog.fb}))

