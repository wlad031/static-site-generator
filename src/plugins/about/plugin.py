import os
from codecs import open

import yaml

from utils.logging import logger
from utils.watch import watcher

import jinja2 as j


class AboutPlugin(object):
    TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates')

    def __init__(self, config_dir):
        self.config_dir = config_dir

        watcher.add_watch(self.TEMPLATES_DIR)

        with open(os.path.join(config_dir, 'config_about.yaml'),
                  'r', 'utf8') as cfg_f:
            self.cfg = yaml.load(cfg_f)

            self.j2 = j.Environment(loader=j.FileSystemLoader(self.TEMPLATES_DIR),
                                    trim_blocks=True)

            logger.info('About plugin configured')

    def generate(self):
        logger.info('About plugin generating')
        res = [
            {
                'navbar': {'name': 'About me'},
                'file': 'about_me.html',
                'html': self.__generate_main_page()
            }
        ]
        logger.info('About plugin pages generated')
        return res

    def __generate_main_page(self):
        template = 'about.html'
        res = self.j2.get_template(template).render(text=self.cfg['html'])
        logger.info('Main page generated')
        return res
