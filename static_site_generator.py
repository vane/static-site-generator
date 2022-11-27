#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import io
import shutil
import operator
import yaml
import liquid
import sass
import csscompressor
import dateutil.parser
import lib.helper
from lib.generator import feed_url, md, robots_txt, rss, seo, sitemap
from lib.config import ConfigObject, Config


def read_layouts(helpers):
    layout = {}
    path = lib.helper.join_path(Config.INPUT, Config.LAYOUT)
    for i, fname in enumerate(os.listdir(path)):
        fpath = lib.helper.join_path(path, fname)
        data = lib.helper.read_file(fpath)
        layout_name = fname.split('.')[0]
        layout[layout_name] = liquid.Liquid(data, **helpers)
    Config.LAYOUT = layout


def generate_style():
    style_path = lib.helper.join_path(Config.INPUT, Config.STYLE)
    fpath = lib.helper.join_path(style_path, Config.STYLE_INPUT_FILE_NAME)
    with open(fpath) as f:
        sass_content = f.read()
    data = sass.compile(string=sass_content, include_paths=[style_path])
    dst = lib.helper.join_path(Config.OUTPUT, Config.STYLE_OUTPUT_DIR)
    lib.helper.makedirs(dst)
    data = csscompressor.compress(data)
    lib.helper.write_file(lib.helper.join_path(dst, Config.STYLE_OUTPUT_FILE_NAME), data)


def load_page(path, fname, split_fname=True):
    content = ''
    page_config = io.StringIO()
    date_data = None
    with open(lib.helper.join_path(path, fname)) as f:
        lines = f.readlines()
        is_content = 0
        for i, line in enumerate(lines):
            if line.startswith('---'):
                is_content += 1
                continue
            if is_content == 2:
                content = lines[i:]
                break
            page_config.write(line)
            # https://github.com/yaml/pyyaml/pull/113
            if line.startswith('date'):
                date_data = ':'.join(line.split(':')[1:])
    page_config.seek(0)
    page_config = yaml.safe_load(page_config)
    page_config['content'] = content
    page_config['content_raw'] = content
    if date_data is not None:
        page_config['date'] = dateutil.parser.parse(date_data)
    if split_fname:
        url = '-'.join(fname.split('.')[0].split('-')[3:])
    else:
        url = fname.split('.')[0]
    page_config['url'] = url
    if 'title' not in page_config:
        page_config['title'] = ''
    if 'keywords' not in page_config:
        page_config['keywords'] = []
    return page_config


def generate_page(page_config, helpers=None):
    if not helpers:
        helpers = {}
    layout = Config.LAYOUT[page_config['layout']]
    ret = layout.render(page=ConfigObject.create(page_config),
                        site=ConfigObject.create(Config.CONFIG),
                        **helpers)
    ret = seo.generate(page_config, ret, Config.CONFIG)
    ret = feed_url.generate(page_config, ret, Config.CONFIG)
    out_path = lib.helper.join_path(Config.OUTPUT, page_config['url'])
    os.makedirs(out_path, exist_ok=True)
    lib.helper.write_file(lib.helper.join_path(out_path, 'index.html'), ret)


def generate_index(posts, helpers):
    page_config = {'layout': 'default', 'url': ''}
    comparator = operator.attrgetter('date')
    posts.sort(key=comparator, reverse=True)
    Config.CONFIG['posts'] = posts
    print('generate index')
    generate_page(page_config=page_config, helpers=helpers)


def copy_assets():
    src = lib.helper.join_path(Config.INPUT, Config.ASSETS)
    dst = lib.helper.join_path(Config.OUTPUT, Config.ASSETS)
    print('copy assets', src, dst)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def generate():
    helpers = lib.helper.get_helpers()
    lib.config.read_config()
    read_layouts(helpers)
    path = lib.helper.join_path(Config.INPUT, Config.POSTS)
    posts = []
    for i, fname in enumerate(os.listdir(path)):
        page_config = load_page(path, fname)
        print('generate post {}'.format(page_config['url']))
        posts.append(ConfigObject.create(page_config))
        page_config['description'] = lib.helper.strip_tags(md.generate(''.join(page_config['content_raw'][:2]).replace('\n', '')))
        generate_page(page_config)
    for i, fname in enumerate(os.listdir(Config.INPUT)):
        if fname.endswith('.markdown'):
            page_config = load_page(Config.INPUT, fname, split_fname=False)
            print('generate page {}'.format(page_config['url']))
            data = {'content': md.generate(page_config['content'])}
            generate_page(page_config, data)
    generate_index(posts, helpers)
    copy_assets()
    generate_style()
    sitemap.generate(posts, Config.CONFIG, output=Config.OUTPUT)
    robots_txt.generate(Config.CONFIG, output=Config.OUTPUT)
    rss.generate(posts, Config.CONFIG, output=Config.OUTPUT)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input directory')
    parser.add_argument('-o', '--output', help='Output directory')
    args = parser.parse_args()
    Config.INPUT = args.input
    Config.OUTPUT = args.output
    if not Config.INPUT and not Config.OUTPUT:
        raise RuntimeError('No output and input directory')
    generate()
