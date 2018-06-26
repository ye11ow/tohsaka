from feedgen.feed import FeedGenerator
import pytz
import os
from dateutil import parser
from datetime import datetime

from tohsaka.outputters.base_outputter import BaseOutputter


class Outputter(BaseOutputter):

    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')

    @property
    def REQUIRED_FIELDS(self):
        return ['description', 'pubDate', 'title']


    def __init__(self, config):
        BaseOutputter.__init__(self, config)

        self.file = config.get('filename', 'output') + '.xml'
        self.title = config.get('title', 'Sample RSS')
        self.description = config.get('description', 'Sample')
        self.base_link = config.get('host')

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

    def done(self):
        if not os.path.isdir(self.OUTPUT_FOLDER):
            os.mkdir(self.OUTPUT_FOLDER)

        self.fg.atom_file(os.path.join(self.OUTPUT_FOLDER, self.file))


    def _output(self, item):
        title = item.get('title')
        description = item.get('description')
        link = item.get('link')
        pubDate = item.get('pubDate')

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
