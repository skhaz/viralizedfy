BOT_NAME = 'tube'

SPIDER_MODULES = ['tube.spiders']

NEWSPIDER_MODULE = 'tube.spiders'

RETRY_ENABLE = True

RETRY_TIMES = 6

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
    'scrapy_magicfields.MagicFieldsMiddleware': 200,
}

DELTAFETCH_ENABLED = True

MAGIC_FIELDS = {
  'url': "$response:url",
  'spider': '$spider:name',
  'timestamp': "$time",
}
