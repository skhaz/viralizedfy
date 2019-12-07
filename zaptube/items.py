import re
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst


class Entry(Item):
  uid = Field()
  title = Field()
  content = Field()
  url = Field()
  spider = Field()
  timestamp = Field()
  media = Field()
  poster = Field()
  mimetype = Field()
  media_url = Field()


class EntryLoader(ItemLoader):
  title_out = Join()
  content_out = Join()
  media_in = TakeFirst()
  media_out = Join()
