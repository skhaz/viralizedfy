BOT_NAME = 'zaptube'

SPIDER_MODULES = ['zaptube.spiders']

NEWSPIDER_MODULE = 'zaptube.spiders'

ROBOTSTXT_OBEY = False

RETRY_ENABLED = False

RETRY_TIMES = 6

ITEM_PIPELINES = {
    'zaptube.pipelines.MimetypePipeline': 300,
    'zaptube.pipelines.MarkdownifyPipeline': 1000
}

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 300,
    'scrapy_magicfields.MagicFieldsMiddleware': 600,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 100,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 300,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 600,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 900
}

MAGIC_FIELDS = {
  'url': "$response:url",
  'spider': '$spider:name',
  'timestamp': "$time",
}
