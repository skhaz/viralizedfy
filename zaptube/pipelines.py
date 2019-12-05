import sys
import re
import hashlib
import mimetypes
import functools
from pathlib import Path
from unicodedata import normalize

from scrapy.exceptions import DropItem
from scrapy.exporters import BaseItemExporter

import base36
from jinja2 import Environment, BaseLoader


class MimetypePipeline():

  def process_item(self, item, spider):
    href = item.get('href')
    if href is None:
      raise DropItem(f"No href were found on item: {item}")

    mimetype, _ = mimetypes.guess_type(href)
    if mimetype is None:
      raise DropItem(f"Cannot determine the mimetype for href: {href}")

    item['mimetype'] = mimetype

    return item


class MarkdownifyPipeline():

  template = Environment(loader=BaseLoader()).from_string("""
---
title: {{ title }}
tags: [""]
draft: false
---

{{ content }}

{% if 'video' in mimetype -%}
<link rel="preload" href="{{ href }}" as="video" type="video/mp4">
<video controls>
  <source src="{{ href }}" type="video/mp4">
</video>
{% else %}
![{{ title }}]({{ href }})
{% endif %}
""")

  path = Path('markdowns')

  def open_spider(self, spider):
    self.path.mkdir(parents=True, exist_ok=True)

  def process_item(self, item, spider):
    title, content, url, mimetype, href = (
      item[key]
      for key in (
        'title',
        'content',
        'url',
        'mimetype',
        'href',
      )
    )

    N = 4
    sha256 = hashlib.sha256(url.encode('utf-8')).digest()
    sliced = int.from_bytes(
      memoryview(sha256)[:N].tobytes(), byteorder=sys.byteorder)
    uid = base36.dumps(sliced)

    strip = str.strip
    lower = str.lower
    split = str.split
    deunicode = lambda n: normalize('NFD', n).encode('ascii', 'ignore').decode('utf-8')
    trashout = lambda n: re.sub(r'[.-@/|*]', ' ', n)
    funcs = [strip, deunicode, trashout, lower, split]

    fragments = [
      *functools.reduce(
        lambda x, f: f(x), funcs, title
      ),
      uid,
    ]

    context = locals().copy()
    del context['self']

    markdown = self.template.render(**context)
    ext = 'md'
    filename = f"{'-'.join(fragments)}.{ext}"
    Path(self.path, filename).write_text(markdown)

    return item
