from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zaptube.items import Entry, EntryLoader


class Spider(CrawlSpider):
  name = 'wt'

  allowed_domains = ['whatstube.com.br']

  start_urls = ['https://www.whatstube.com.br']

  rules = (
    Rule(
      LinkExtractor(deny=[
        'download/',
        'contato/',
        'envie-para-nos/'
        ]
      ), callback='parse_item', follow=True
    ),
  )

  def parse_item(self, response):
    loader = EntryLoader(item=Entry(), response=response)
    loader.add_css('title', 'h1.post-title::text')
    loader.add_css('content', '.article-content p::text')
    loader.add_css('href', '#player source::attr(src)')
    loader.add_css('poster', '#player ::attr(poster)')
    return loader.load_item()
