#!/usr/bin/env python
# -*- coding: utf-8 -*-
import markdown
import markdown.extensions
import markdown.preprocessors
import pygments
import pygments.lexers
import pygments.formatters
import lib.helper

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
                    print('inline : {}'.format(code))
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


class SitemapGenerator():
    @staticmethod
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
        lib.helper.write_file(fpath, data)

class RobotsTxtGenerator():
    @staticmethod
    def generate(config, output, data=None):
        if not data:
            data = """User-Agent: *
Disallow: 
Sitemap: {}/sitemap.xml
""".format(config['url'])
        fpath = lib.helper.join_path(output, 'robots.txt')
        lib.helper.write_file(fpath, data)

def md(content):
    return markdown.markdown(''.join(content), extensions=[HighlightExtension()])
