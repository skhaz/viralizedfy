import os
import sys
import re
import hashlib
import mimetypes
import functools
from pathlib import Path
from unicodedata import normalize

from scrapy.http import Request
from scrapy.utils.python import to_bytes
from scrapy.exceptions import DropItem
from scrapy.exporters import BaseItemExporter
from scrapy.pipelines.files import FilesPipeline

import base36
from jinja2 import Environment, BaseLoader


class PreparePipeline():

  def process_item(self, item, spider):
    url = item['url'].encode('utf-8')
    title = item.get('title')
    if title is None:
      raise DropItem(f"No title were found on item: {item}")

    N = 4
    sha256 = hashlib.sha256(url).digest()
    sliced = int.from_bytes(
      memoryview(sha256)[:N].tobytes(), byteorder=sys.byteorder)
    uid = base36.dumps(sliced)

    strip = str.strip
    lower = str.lower
    split = str.split
    deunicode = lambda n: normalize('NFD', n).encode('ascii', 'ignore').decode('utf-8')
    trashout = lambda n: re.sub(r'[.-@/|*]', ' ', n)
    functions = [strip, deunicode, trashout, lower, split]
    fragments = [
      *functools.reduce(
        lambda x, f: f(x), functions, title),
      uid,
    ]

    item['uid'] = '-'.join(fragments)

    return item


class MimetypePipeline():

  def process_item(self, item, spider):
    media = item.get('media')
    if media is None:
      raise DropItem(f"No media were found on item: {item}")

    mimetype, _ = mimetypes.guess_type(media)
    if mimetype is None:
      raise DropItem(f"Cannot determine the mimetype for media: {media}")

    item['mimetype'] = mimetype

    item['ext'] = mimetypes.guess_extension(mimetype)

    return item


class DownloadPipeline(FilesPipeline):

  def get_media_requests(self, item, info):
    url = item['media']
    meta = {'uid': item['uid'], 'ext': item['ext']}
    yield Request(url, meta=meta)

  def file_path(self, request, response=None, info=None):
    uid = request.meta['uid']
    ext = request.meta['ext']
    return ''.join([uid, ext])

  def item_completed(self, results, item, info):
    item['media_url'] = "https://storage.googleapis.com/scrapy-test/" + results[0][1]['path']
    return item


class MarkdownifyPipeline():

  template = Environment(loader=BaseLoader()).from_string("""---
title: {{ title }}
tags: [""]
draft: false
---

{{ content }}

{% if media_url -%}
{% if 'video' in mimetype -%}
<video controls>
  <source src="{{ media_url }}" type="{{ mimetype }}">
</video>
{% else %}
![{{ title }}]({{ media_url }})
{% endif %}
{% endif -%}
  """)

  def process_item(self, item, spider):
    title, content, mimetype, media_url, uid = (
      item[key]
      for key in (
        'title',
        'content',
        'mimetype',
        'media_url',
        'uid',
      )
    )

    context = locals().copy()
    del context['self']

    path = Path.cwd() / 'content'
    path.mkdir(parents=True, exist_ok=True)
    markdown = self.template.render(**context)
    Path(path, '%s.md' % uid).write_text(markdown)

    return item
