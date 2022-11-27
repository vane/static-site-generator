#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import lib.config
import urllib.parse


class FunctionHelper:
    @staticmethod
    def join(a, b=','):
        return b.join(a)

    @staticmethod
    def relative_url(a):
        return lib.config.Config.CONFIG['baseurl']+a

    @staticmethod
    def replace(a, b, c):
        return a.replace(b, c)

    @staticmethod
    def escape(a):
        return urllib.parse.quote(a)

    @staticmethod
    def cgi_escape(a):
        return a

    @staticmethod
    def date(a, b):
        return a.strftime(b)

    @staticmethod
    def truncatewords(a, b):
        text = strip_tags(a)
        out = '<p>'
        lines = ''.join(text).split(' ')[:b]
        for line in lines:
            if line.strip():
                out += line.strip() + ' '
        out += '...</p>'
        return out

    @staticmethod
    def highlight(*args, **kwargs):
        return ''


class Paginator:
    @property
    def posts(self):
        return lib.config.Config.CONFIG['posts']

    @property
    def total_pages(self):
        return 1


def get_helpers():
    method_list = [func for func in dir(FunctionHelper) if callable(getattr(FunctionHelper, func)) and not func.startswith('__')]
    helpers = {}
    for key in method_list:
        helpers[key] = getattr(FunctionHelper, key)
    helpers['paginator'] = Paginator()
    return helpers


def write_file(path, data):
    with open(path, 'wb+') as f:
        f.write(data.encode('utf-8'))


def read_file(path):
    with open(path) as f:
        data = f.read()
    return data


def makedirs(path):
    os.makedirs(path, exist_ok=True)


def join_path(path, *paths):
    return os.path.join(path, *paths)


def strip_tags(data):
    return re.sub('<[^<]+?>', '', data).strip()
