#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import lib.helper
from datetime import datetime
from lib.generator import md


def generate(posts, config, output, generator='vane.pl', generator_url='https://vane.pl'):
    data = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" >
<generator uri="{generator_url}" version="0.0.1">{generator}</generator>
<link href="{url}/feed.xml" rel="self" type="application/atom+xml" />
<link href="{url}" rel="alternate" type="text/html" />
<updated>{now}</updated>
<id>{url}/feed.xml</id>
<title type="html">{title}</title>
<subtitle>{subtitle}</subtitle>
""".format(**{
        'url':config['url'],
        'now':datetime.now().isoformat(),
        'title': config['title'],
        'subtitle': config['description'],
        'generator': generator,
        'generator_url': generator_url,
    })
    for p in posts[:10]:
        category = ['<category term="{}" />'.format(c) for c in p.tags]
        summary = md.generate(''.join(p.content_raw[:3]).replace('\n', ''))
        summary = lib.helper.strip_tags(summary)
        data += """<entry>
<title type="html">{title}</title>
<link href="{url}" rel="alternate" type="text/html" title="{title}" />
<published>{published}</published>
<updated>{published}</updated>
<id>{url}</id>
<content type="html" xml:base="{url}">
{content}
</content>
<author>
<name>{author}</name>
</author>
{category}
<summary type="html">{summary}</summary>
<media:thumbnail xmlns:media="http://search.yahoo.com/mrss/" url="{image_path}" />
</entry>
""".format(**{
            'url': config['url']+'/'+p.url,
            'title': p.title,
            'content': urllib.parse.quote(p.content),
            'published': p.date.isoformat(),
            'category': category,
            'author': p.author,
            'summary': summary,
            'image_path': config['url']+p.image.path
        })
    data += '</feed>'
    fpath = lib.helper.join_path(output, 'feed.xml')
    print('generate feed.xml')
    lib.helper.write_file(fpath, data)
