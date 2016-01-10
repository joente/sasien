import os
import datetime
import configparser
import markdown
import helpers

SECTION = 'blog_post'


class Blog:

    def __init__(self, metafile):
        config = configparser.RawConfigParser()
        config.read(metafile)

        self.date = datetime.datetime.strptime(config.get(SECTION, 'date'), '%Y-%m-%d')
        self.title = config.get(SECTION, 'title')
        self.photo = os.path.join('/', 'img', 'blog', config.get(SECTION, 'photo'))
        self.name = config.get(SECTION, 'name')
        self.target = os.path.join('/', 'blog', helpers.htmlname(self.name))
        self.description = config.get(SECTION, 'fb-description')
        self.fb = {
            'url': 'http://sasien.nl/blog/{}/'.format(helpers.htmlname(self.name)),
            'type': 'article',
            'image': 'http://sasien.nl/img/fb/{}'.format(config.get(SECTION, 'fb-image')),
            'title': config.get(SECTION, 'fb-title'),
            'description': self.description}

        mdfile = os.path.join(os.path.dirname(metafile), config.get(SECTION, 'content'))
        with open(mdfile, 'r', encoding='utf-8') as f:
            self.html = markdown.markdown(f.read(), output_format='html5')

    def __str__(self):
        return '<blog date={}, title={}>'.format(self.date, self.title)


if __name__ == '__main__':
    b = Blog('blog/bb.meta')
    print(b.date, b.title, b.html)