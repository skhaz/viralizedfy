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
    guid = base36.dumps(sliced)

    strip = str.strip
    lower = str.lower
    split = str.split
    deunicode = lambda n: normalize('NFD', n).encode('ascii', 'ignore').decode('utf-8')
    trashout = lambda n: re.sub(r'[.-@/|*]', ' ', n)
    functions = [strip, deunicode, trashout, lower, split]
    fragments = [
      *functools.reduce(
        lambda x, f: f(x), functions, title),
      guid,
    ]

    item['guid'] = '-'.join(fragments)

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

    extension = mimetypes.guess_extension(mimetype)
    if not extension:
      raise DropItem(f"Cannot determine the extension for mimetype: {mimetype}")
    item['extension'] = extension

    return item


class DownloadPipeline(FilesPipeline):
  def get_media_requests(self, item, info):
    extension, guid, url = (item[key]
      for key in ('extension', 'guid', 'url'))
    yield Request(url, meta=dict(filename=''.join([guid, extension])))

  def file_path(self, request, response=None, info=None):
    return request.meta['filename']

  def item_completed(self, results, item, info):
    item['ready'] = bool(results[0][0])
    return item


jinja2 = Environment(loader=BaseLoader()).from_string("""
---
title: {{ title }}
tags: [""]
draft: false
---

{{ content }}

{% if 'video' in mimetype -%}
<video controls>
  <source src="{{ filename }}" type="{{ mimetype }}">
</video>
{% elif 'image' in mimetype %}
![{{ title }}]({{ filename }})
{% elif 'audio' in mimetype %}
<audio controls>
  <source src="{{ filename }}" type="{{ mimetype }}">
</audio>
{% endif -%}
""")


class MarkdownifyPipeline():
  def process_item(self, item, spider):
    content, extension, mimetype, guid, title = (
      item[key] for key in (
        'content',
        'extension',
        'mimetype',
        'guid',
        'title',
      ))

    context = locals().copy()
    context['filename'] = f'{guid}{extension}'
    del context['self']

    path = Path.cwd() / 'output'
    path.mkdir(parents=True, exist_ok=True)
    markdown = jinja2.render(**context)
    Path(path, f'{guid}').write_text(markdown)

    return item
