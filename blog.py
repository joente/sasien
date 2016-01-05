import os
import datetime
import configparser
import markdown


SECTION = 'blog_post'


class Blog:

    def __init__(self, metafile):
        config = configparser.RawConfigParser()
        config.read(metafile)

        self.date = datetime.datetime.strptime(config.get(SECTION, 'Date'), '%Y-%m-%d')
        self.title = config.get(SECTION, 'Title')
        self.photo = config.get(SECTION, 'Photo')
        mdfile = config.get(SECTION, 'Content')

        with open(mdfile, 'r', encoding='utf-8') as f:
            self.html = markdown.markdown(f.read(), output_format='html5')

    def __str__(self):
        return '<blog date={}, title={}>'.format(self.date, self.title)


if __name__ == '__main__':
    b = Blog('blog/bb.meta')
    print(b.date, b.title, b.html)