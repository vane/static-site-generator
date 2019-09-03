#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lib.helper
from datetime import datetime


def generate(config, output, data=None):
    if not data:
        data = """User-Agent: *
Disallow: 
Sitemap: {}/sitemap.xml
""".format(config['url'])
    fpath = lib.helper.join_path(output, 'robots.txt')
    print('generate robots.txt')
    lib.helper.write_file(fpath, data)
