import os
import helpers
import logging
from PIL import Image
from logger import setup_logger

def resize():

    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    PHOTO_DIR = os.path.join(CURRENT_DIR, 'blog', 'photos')
    BLOG_IMAGE_WIDTH = 939

    for root, dirs, files in os.walk(PHOTO_DIR):
        for name in files:
            if not name.endswith('.jpg'):
                continue
            fn = os.path.join(root, name)
            img = Image.open(fn)
            if img.size[0] <= BLOG_IMAGE_WIDTH:
                continue
            logging.info('Resizing: {}...'.format(fn))
            img = helpers.resized_img(img, maxwidth=BLOG_IMAGE_WIDTH)
            img.save(fn)


if __name__ == '__main__':
    setup_logger('debug')
    resize()