import re
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst


class Entry(Item):
  title = Field()
  content = Field()
  url = Field()
  spider = Field()
  timestamp = Field()
  href = Field()
  poster = Field()
  mimetype = Field()


def nuke_trash(text, pattern=r'^descri[cç][aã]o:?\s+'):
  return re.sub(pattern, '', text, flags=re.IGNORECASE)


class EntryLoader(ItemLoader):
  title_out = Join()
  content_in = MapCompose(nuke_trash, str.strip)
  content_out = Join()
  href_out = TakeFirst()
  poster_out = Join()
