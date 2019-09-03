#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lib.helper


def generate(posts, config, output):
    data = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    for p in posts:
        url = config['url']+'/'+p.url
        partial = """<url>
<loc>{}</loc>
<lastmod>{}</lastmod>
</url>""".format(url, p.date.isoformat())
        data += partial
    data += """</urlset>"""
    fpath = lib.helper.join_path(output, 'sitemap.xml')
    print('generate sitemap')
    lib.helper.write_file(fpath, data)
