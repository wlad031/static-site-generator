import os
from codecs import open

import yaml

from utils.logging import logging
from utils.json import pretty_json

import jinja2 as j


class AboutPlugin(object):
    TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates')

    def __init__(self, config_dir):
        with open(os.path.join(config_dir, 'config_about.yaml'),
                  'r', 'utf8') as cfg_f:
            self.cfg = yaml.load(cfg_f)

            logging.debug('About plugin config:')
            logging.debug(pretty_json(**self.cfg))

            self.j2 = j.Environment(loader=j.FileSystemLoader(self.TEMPLATES_DIR),
                                    trim_blocks=True)

    def generate(self):
        return [
            {
                'navbar': {'name': 'About me'},
                'file': 'about_me.html',
                'html': self.__generate_main_page()
            }
        ]

    def __generate_main_page(self):
        template = 'about.html'
        return self.j2.get_template(template).render(text=self.cfg['html'])
