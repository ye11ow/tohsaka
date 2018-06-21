from feedgen.feed import FeedGenerator
import pytz
import os
from dateutil import parser
from datetime import datetime

from tohsaka.outputters.base_outputter import BaseOutputter


class Outputter(BaseOutputter):

    @property
    def REQUIRED_FIELDS(self):
        return ['description', 'pubDate', 'title']


    def __init__(self, config, params):
        BaseOutputter.__init__(self, config, params)

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
        try:
            pubDate = parser.parse(pubDate).replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        except:
            pubDate = datetime.now(pytz.utc).isoformat()
        fe.pubDate(pubDate)
        fe.updated(pubDate)


    def done(self):
        self.fg.atom_file(self.output_path)


    def _output(self, item):
        self._add_entry(item['title'], item['description'], item['link'], item['pubDate'])
