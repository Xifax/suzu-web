# coding: utf-8

# internal
import re

# external
from scrapy.contrib.spiders import (
        CrawlSpider,
        Rule
)
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from bs4 import BeautifulSoup

# own
from hebi.items import Kanji

class KanjiSpider(CrawlSpider):
    """Crawls japanese web resources and devours kanji"""

    name = "hebi"
    allowed_domains = ["ja.wikipedia.org"]
    start_urls = [
        "http://ja.wikipedia.org/",
    ]
    rules = [
            #Rule(SgmlLinkExtractor(allow=()), follow=True),
            Rule(SgmlLinkExtractor(allow=()), callback='parse_item')
    ]

    def parse_item(self, response):
        # TODO: if parser rate of found items is not high -> shut down
        # Parse the page
        hxs = HtmlXPathSelector(response)
        divs = hxs.select('//div')
        items = []
        for p in divs.select('.//p'):
            # Match kanji only
            for symbols in re.findall(ur'[\u4e00-\u9fff]+', p.extract()):
                # Iterate found kanji
                for symbol in symbols:
                    kanji = Kanji()
                    kanji['character'] = symbol
                    items.append(kanji)
        return items

