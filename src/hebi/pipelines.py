# coding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
#
from scrapy import signals
from scrapy.exceptions import DropItem
import json

from db.mongo import connectMongo
from db.models import Key

class DuplicatesPipeline(object):
    """Check, if such item already exists in mongo db"""

    def __init__(self):
        connectMongo()
        self.ids_seen = set()
        self.total_items = 0

    def process_item(self, item, spider):
        # Check, if such items is already in DB
        if len(Key.objects(value=item['character'])) == 1:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.total_items += 1
            # Check, if total items count is over the limit
            if self.total_items > int(spider.limit):
                spider.stop_now = True
            return item

class JsonWriterPipeline(object):
    """Dump items to JSON"""

    def __init__(self):
        self.file = open('../items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class MongoPipeline(object):
    """Dump items to mongo db"""

    def __init__(self):
        connectMongo()

    def process_item(self, item, spider):
        kanji = Key(value=item['character'], category='kanji', lang='Japanese')
        kanji.save()
        return item

