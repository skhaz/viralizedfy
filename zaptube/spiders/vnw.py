from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zaptube.items import Entry, EntryLoader


class Spider(CrawlSpider):
  name = 'vnw'

  allowed_domains = ['videosnowhats.com']

  start_urls = ['http://www.videosnowhats.com']

  rules = (
    Rule(
      LinkExtractor(allow=[
        'zap/',
        'zap-zap/',
        'amor/',
        'bizarros/'
        ],
        deny=[
          'categoria/',
          'audios/',
          'imagens/',
          'frases-para-status/',
          'charadas-para-whatsapp/',
        ]
      ), callback='parse_video', follow=True
    ),
    Rule(
      LinkExtractor(allow=[
          'categoria/',
          'audios/',
          'imagens/'
        ],
        deny=[
          'frases-para-status/',
          'charadas-para-whatsapp/',
        ]
      ), callback='parse_other', follow=True
    ),
  )

  def _build_loader(self, response):
    return EntryLoader(item=Entry(), response=response)

  def parse_video(self, response):
    loader = self._build_loader(response)
    loader.add_xpath('title', '//*[@class="cs-post-single-header"]/h1/text()')
    loader.add_xpath('content', '//header/h3/text()')
    loader.add_xpath('href', '//*[@id="player"]/source/@src')
    loader.add_xpath('poster', '//*[@id="player"]/@poster')
    return loader.load_item()

  def parse_other(self, response):
    loader = self._build_loader(response)
    loader.add_xpath('title', '//h1[@class="section h5"]/text()')
    loader.add_xpath('content', '//div/p/text()')
    loader.add_xpath('href', '//div/img/@src')
    return loader.load_item()
