#!/usr/bin/env python
# -*- coding: utf-8 -*-

def generate(post, data, config):
    start = data.find('{%-')
    end = data.find('-%}')
    tag = data[start+3:end]
    content = ''
    if start == -1 or end == -1:
        return data
    if tag.find('feed_meta') > -1:
        content = """<link type="{type}" rel="alternate" href="{url}/feed.xml" title="{title}" />""".format(**{
            'type': 'application/atom+xml',
            'url': config['url'],
            'title': config['title'],
        })
        # print('generate feed_meta for post {}'.format(post['url']))
    return data[:start]+content+data[end+3:]
