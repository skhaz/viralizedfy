from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from tube.items import Entry, EntryLoader


class WhatstubeSpider(CrawlSpider):
  name = 'whatstube'

  allowed_domains = ['whatstube.com.br']

  start_urls = ['https://www.whatstube.com.br']

  rules = (
    Rule(
      LinkExtractor(deny=[
        'download/',
        'contato/',
        'envie-para-nos/'
        ]
      ), callback='parse_v1', follow=True
    ),

    Rule(
      LinkExtractor(allow='download/'), callback='parse_v2', follow=True
    ),
  )

  def _build_loader(self, response):
    return EntryLoader(item=Entry(), response=response)

  def parse_v1(self, response):
    loader = self._build_loader(response)
    loader.add_css('title', 'h1.post-title::text')
    loader.add_css('content', '.article-content p::text')
    return loader.load_item()

  def parse_v2(self, response):
    loader = self._build_loader(response)
    loader.add_css('title', '.pis-title-link a::text')
    loader.add_css('content', '.quad-baixar p::text')
    loader.add_css('href', '.main-body script', re=r"href='(.*)';")
    return loader.load_item()
