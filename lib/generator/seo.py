#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import lib.helper
from lib.generator import md

def generate(post, data, config):
    start = data.find('{%-')
    end = data.find('-%}')
    tag = data[start+3:end]
    content = ''
    if tag.find('seo') > -1:
        # print('generate seo for post {}'.format(post['url']))
        locale = 'en_US'
        title = config['title']
        description = post.get('description') or config['description']
        if 'locale' in post:
            locale = post['locale']
        if 'title' in post:
            title = post['title']
        if description is None and 'content_raw' in post:
            description = lib.helper.strip_tags(md.generate(''.join(post['content_raw'][:2]).replace('\n', '')))
        url = config['url']
        if 'url' in post:
            url += '/'+post['url']
        # schema_org
        schema_data = {
            "headline": title,
            "description": description,
            "@context": "https://schema.org",
        }
        data2 = {
            'title':title,
            'locale':locale,
            'description': description,
            'url': url,
            'site_name': config['title'],
            'headline': title,

        }
        article_content = ''
        if 'author' in post:
            schema_data.update({
                "author": {
                    "@type": "Person",
                    "name": post['author']
                },
                "mainEntityOfPage": {
                    "@id": url,
                    "type": "WebPage"
                },
                "@type": "BlogPosting",
                "dateModified": post['date'].isoformat(),
                "datePublished": post['date'].isoformat(),
            })
            article_content = """<meta property="og:type" content="article" />
<meta property="article:published_time" content="{published_time}" />
<meta name="author" content="{author}" />""".format(**{
                'published_time':post['date'].isoformat(),
                'author': post['author'],
            })
        else:
            schema_data.update({
                "@type":"WebSite",
            })
        data2.update({
            'article_content':article_content
        })
        image_content = ''
        if 'image' in post:
            schema_data.update({
                "image": {
                    "@type": "imageObject",
                    "height": post['image'].height,
                    "url": config['url']+post['image'].path,
                    "width": post['image'].width,
                },
            })
            image_content = """<meta property="og:image" content="{image_url}" />
<meta property="og:image:height" content="{image_height}" />
<meta property="og:image:width" content="{image_width}" />""".format(**{
                "image_height": post['image'].height,
                "image_url": config['url']+post['image'].path,
                "image_width": post['image'].width,
            })
        data2.update({
            'image_content': image_content,
        })
        data3 = {'json_data':json.dumps(schema_data)}
        data3.update(data2)
        content = """<meta property="og:title" content="{title}" />
<meta property="og:locale" content="{locale}" />
<meta name="description" content="{description}" />
<meta property="og:description" content="{description}" />
<link rel="canonical" href="{url}" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="{site_name}" />{image_content}{article_content}
<script type="application/ld+json">
{json_data}
</script>""".format(**data3)
    return data[:start]+content+data[end+3:]
