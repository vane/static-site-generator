#!/usr/bin/env python
# -*- coding: utf-8 -*-
import markdown
import pygments
import pygments.lexers
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from pygments.formatters.html import HtmlFormatter
# for performance
lexer_cache = {}


class HighlightPreprocessor(Preprocessor):

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
                    # print('code hightlight inline : {}'.format(code))
            if have_code == 1 and not skip:
                code += line+'\n'
            if have_code == 2:
                if not language in lexer_cache:
                    # long running operation so cache it
                    lexer = pygments.lexers.get_lexer_by_name(language)
                    lexer_cache[language] = lexer
                else:
                    lexer = lexer_cache[language]
                line = pygments.highlight(code=code, lexer=lexer, formatter=HtmlFormatter())
                have_code = 0
                code = ''
            if have_code == 0:
                output.append(line)
            skip = False
        return output


class HighlightExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(HighlightPreprocessor(md), 'highlight', 0)


def generate(content):
    return markdown.markdown(''.join(content), extensions=[HighlightExtension()])
