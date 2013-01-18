# Scrapy settings for hebi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'hebi'

SPIDER_MODULES = ['hebi.spiders']
NEWSPIDER_MODULE = 'hebi.spiders'

# Filter duplicates and save to mongo
ITEM_PIPELINES = [
    'hebi.pipelines.DuplicatesPipeline',
    'hebi.pipelines.MongoPipeline',
    #'hebi.pipelines.JsonWriterPipeline',
]

EXTENSIONS = {
    'scrapy.contrib.closespider.CloseSpider' : 500,
}

# In seconds (5 minutes)
#CLOSESPIDER_TIMEOUT = 300

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hebi (+http://www.yourdomain.com)'
