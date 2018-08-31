import os
import hashlib
import time
from datetime import datetime
from feedgen.feed import FeedGenerator
import pytz
from dateutil import parser
from utils import file_util
from utils import log_util

from outputters.base_outputter import BaseOutputter

logger = log_util.get_logger('tohsaka.rss')

SECONDS_OF_DAY = 60*60*24

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
        self.temp_dir = file_util.get_temp_dir()

        self.fg = FeedGenerator()
        self._create_feed()

        self.item_count = 0
        self.filtered_count = 0

    def _create_feed(self):
        fg = self.fg
        fg.id(self.base_link)
        fg.title(self.title)
        fg.language('zh-CN')
        fg.link(href=self.base_link, rel='self')
        fg.description(self.description)
        fg.author(name='Tohsaka')

    def _valid(self, item):
        self.item_count += 1
        valid = BaseOutputter._valid(self, item)

        if valid:
            filename = hashlib.md5(item.get('link').encode('utf-8')).hexdigest()
            valid = not file_util.touch(os.path.join(self.temp_dir, filename))
            if not valid:
                logger.debug('%s is filtered', item.get('title'))
                self.filtered_count += 1

        return valid

    def _clear_obsolete_cache(self, days):
        files = os.listdir(self.temp_dir)
        now = time.time()
        removed_count = 0

        for f in files:
            filename = os.path.join(self.temp_dir, f)
            diff = now - os.path.getmtime(filename)
            if diff > SECONDS_OF_DAY * days:
                os.remove(filename)
                removed_count +=1

        if removed_count > 0:
            logger.info('Removing %d obsolete cache', removed_count)

    def _output(self):
        filename = os.path.join(self.output_folder, self.file)
        logger.info('Output to file %s. Total items %d, filtered %d', filename, self.item_count, self.filtered_count)
        self.fg.atom_file(filename)

        self._clear_obsolete_cache(14)

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
