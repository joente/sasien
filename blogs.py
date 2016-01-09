class Blogs:

    def __init__(self):
        self.blogs = []

    def add(self, blog):
        for n, b in enumerate(self.blogs):
            if blog.date > b.date:
                break
        else:
            n = len(self.blogs)
        self.blogs.insert(n, blog)

    def __iter__(self):
        return iter(self.blogs)

    def __str__(self):
        return '\nNumber of blogs: {}\n{}\n{}'.format(
            len(self.blogs),
            '='*40,
            '\n'.join(map(str, self.blogs)))


if __name__ == '__main__':
    b = Blogs()
    import blog
    b.add(blog.Blog('blog/bb.meta'))
    b.add(blog.Blog('blog/aa.meta'))
    b.add(blog.Blog('blog/hoi_hoi.meta'))
    print(b)