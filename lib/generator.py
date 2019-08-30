#!/usr/bin/env python
# -*- coding: utf-8 -*-
import markdown
import markdown.extensions
import markdown.preprocessors
import pygments
import pygments.lexers
import pygments.formatters
import lib.helper
import urllib.parse
import json
from datetime import datetime

# for performance
lexer_cache = {}

class HighlightPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md=None):
        super().__init__(md)
        self.start = '{% highlight'
        self.end = '{% endhighlight %}'

    def run(self, lines):
        code = ''
        language = None
        have_code = 0
        output = []
        start_line = 0
        skip = False
        for i, line in enumerate(lines):
            if line.find(self.start) > -1:
                have_code = 1
                start_line = i
                code = ''
                language = line[len(self.start):].strip().split(' ')[0]
                # print(language)
                skip = True
            if line.find(self.end) > -1:
                have_code = 2
                if start_line == i:
                    start = line.find('%}')+2
                    end = line.find(self.end)
                    code = line[start:end]
                    print('code hightlight inline : {}'.format(code))
            if have_code == 1 and not skip:
                code += line+'\n'
            if have_code == 2:
                if not language in lexer_cache:
                    # long running operation so cache it
                    lexer = pygments.lexers.get_lexer_by_name(language)
                    lexer_cache[language] = lexer
                else:
                    lexer = lexer_cache[language]
                line = pygments.highlight(code=code, lexer=lexer, formatter=pygments.formatters.HtmlFormatter())
                have_code = 0
                code = ''
            if have_code == 0:
                output.append(line)
            skip = False
        return output

class HighlightExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('highllight', HighlightPreprocessor(md), '_begin')


def sitemap(posts, config, output):
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

def robots_txt(config, output, data=None):
    if not data:
        data = """User-Agent: *
Disallow: 
Sitemap: {}/sitemap.xml
""".format(config['url'])
    fpath = lib.helper.join_path(output, 'robots.txt')
    print('generate robots.txt')
    lib.helper.write_file(fpath, data)

def feed_xml(posts, config, output, generator='vane.pl', generator_url='https://vane.pl'):
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
        summary = md(''.join(p.content_raw[:3]).replace('\n', ''))
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

def seo_generate(post, data, config):
    start = data.find('{%-')
    end = data.find('-%}')
    tag = data[start+3:end]
    content = ''
    if tag.find('seo') > -1:
        print('generate seo for post {}'.format(post['url']))
        locale = 'en_US'
        title = config['title']
        description = config['description']
        if 'locale' in post:
            locale = post['locale']
        if 'title' in post:
            title = post['title']
        if 'content_raw' in post:
            description = lib.helper.strip_tags(md(post['content_raw'][0]))
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

def feed_meta_generate(post, data, config):
    start = data.find('{%-')
    end = data.find('-%}')
    tag = data[start+3:end]
    content = ''
    if tag.find('feed_meta') > -1:
        content = """<link type="{type}" rel="alternate" href="{url}/feed.xml" title="{title}" />""".format(**{
            'type': 'application/atom+xml',
            'url':config['url'],
            'title':config['title'],
        })
        print('generate feed_meta for post {}'.format(post['url']))
    return data[:start]+content+data[end+3:]

def md(content):
    return markdown.markdown(''.join(content), extensions=[HighlightExtension()])
