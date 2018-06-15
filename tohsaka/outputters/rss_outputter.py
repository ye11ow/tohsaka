from feedgen.feed import FeedGenerator
import os


REQUIRED_FIELDS = ['description', 'pubDate', 'title']

class Outputter(object):

    def __init__(self, config):
        self.file = config.get('filename', 'output') + '.xml'
        folder = os.path.join(os.getcwd(), 'output')
        self.output_path = os.path.join(folder, self.file)
        self.title = config.get('title', 'Sample RSS')
        self.description = config.get('description', 'Sample')
        self.base_link = config.get('host')

        if not os.path.isdir(folder):
            os.mkdir(folder)

        self.fg = FeedGenerator()
        self._create_feed()

    def _create_feed(self):
        fg = self.fg
        fg.id(self.base_link)
        fg.title(self.title)
        fg.language('zh-CN')
        fg.link(href=self.base_link, rel='self')
        fg.description(self.description)
        fg.author(name='Tohsaka')

        fg.atom_file(self.output_path)
        return

    def _add_entry(self, title, description, link, pubDate):
        fe = self.fg.add_entry()

        fe.title(title)
        fe.link(href=link)
        fe.content(content=description, type='html')
        fe.guid(link)
        fe.pubDate(pubDate)
        fe.updated(pubDate)

    def done(self):
        self.fg.atom_file(self.output_path)


    def _valid(self, item):
        for field in REQUIRED_FIELDS:
            if field not in item:
                return False

        return True

    def _output(self, item):
        self._add_entry(item['title'], item['description'], item['link'], item['pubDate'])


    def go(self, item):
        if self._valid(item):
            return self._output(item)
        else :
            return False
