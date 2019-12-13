BOT_NAME = 'zaptube'

SPIDER_MODULES = ['zaptube.spiders']

NEWSPIDER_MODULE = 'zaptube.spiders'

LOG_LEVEL = 'INFO'

ROBOTSTXT_OBEY = False

RETRY_ENABLED = True

RETRY_TIMES = 6

MEDIA_ALLOW_REDIRECTS = True

ITEM_PIPELINES = {
  'zaptube.pipelines.PreparePipeline': 100,
  'zaptube.pipelines.MimetypePipeline': 200,
  # 'zaptube.pipelines.DownloadPipeline': 300,
  # 'zaptube.pipelines.MarkdownifyPipeline': 1000
}

FILES_STORE = 'gs://scrapy-test/'  # 'gs://gcs.viralizedfy.ai/'

GCS_PROJECT_ID = 'viralizedfy'

FILES_EXPIRES = 356

FILES_STORE_GCS_ACL = 'publicRead'

SPIDER_MIDDLEWARES = {
    # 'scrapy_deltafetch.DeltaFetch': 300,
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
}
