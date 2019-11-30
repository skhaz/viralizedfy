import re

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join


class Entry(Item):
  title = Field()
  content = Field()
  url = Field()
  spider = Field()
  timestamp = Field()
  href = Field()


def nuke_word(word, pattern=r'^descri[cç][aã]o:?\s+'):
  return re.sub(pattern, '', word, flags=re.IGNORECASE)


class EntryLoader(ItemLoader):
  content_in = MapCompose(nuke_word, str.strip)
  content_out = Join()
