from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst


class Entry(Item):
  content = Field()
  extension = Field()
  guid = Field()
  media = Field()
  mimetype = Field()
  poster = Field()
  ready = Field()
  spider = Field()
  timestamp = Field()
  title = Field()
  url = Field()


class EntryLoader(ItemLoader):
  content_out = Join()
  media_in = TakeFirst()
  media_out = Join()
  poster_out = Join()
  title_out = Join()
