#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import yaml
import dateutil.parser
import lib.generator

class Config:
    INPUT = None
    OUTPUT = None
    CONFIG = '_config.yml'
    POSTS = '_posts'
    LAYOUT = '_layouts'
    DRAFTS = '_drafts'
    STYLE = '_sass'
    STYLE_INPUT_FILE_NAME = 'main.scss'
    STYLE_OUTPUT_FILE_NAME = 'main.css'
    STYLE_OUTPUT_DIR = 'assets/css'
    ASSETS = 'assets'


class ConfigObject:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, item):
        if item not in self.data:
            raise RuntimeError('problem')
        if item == 'content':
            return lib.generator.md(self.data[item])
        return self.data[item]

    @staticmethod
    def create(data):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = ConfigObject.create(value)
        return ConfigObject(data)


def read_config():
    path = os.path.join(Config.INPUT, Config.CONFIG)
    with open(path) as f:
        Config.CONFIG = yaml.safe_load(f)
