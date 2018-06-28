import os
from datetime import datetime
from feedgen.feed import FeedGenerator
import pytz
from dateutil import parser

from tohsaka.outputters.base_outputter import BaseOutputter


class Outputter(BaseOutputter):

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

    def _output(self):
        self.fg.atom_file(os.path.join(self.OUTPUT_FOLDER, self.file))


    def _add_item(self, item):
        title = item.get('title')
        description = item.get('description')
        link = item.get('link')
        pub_date = item.get('pubDate')

        entry = self.fg.add_entry()

        entry.title(title)
        entry.link(href=link)
        entry.content(content=description, type='html')
        entry.guid(link)
        try:
            pub_date = parser.parse(pub_date).replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        except:
            pub_date = datetime.now(pytz.utc).isoformat()
        entry.pubDate(pub_date)
        entry.updated(pub_date)
