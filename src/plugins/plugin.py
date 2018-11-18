import os
from codecs import open

from utils.logging import logger
from utils.time import datetimeformat
from utils.watch import watcher

import yaml

import jinja2 as j


class Plugin(object):

    def __init__(self, plugin_name, config_dir, templates_dir, config_file_name):
        self.plugin_name = plugin_name
        self.config_dir = config_dir
        self.templates_dir = templates_dir
        self.config_file_name = config_file_name

        watcher.add_watch(self.templates_dir)

        config_path = os.path.join(self.config_dir, self.config_file_name)
        with open(config_path, 'r', 'utf8') as cfg_f:
            self.cfg = yaml.load(cfg_f)
            self.j2 = j.Environment(loader=j.FileSystemLoader(self.templates_dir),
                                    trim_blocks=True)
            self.j2.filters['datetimeformat'] = datetimeformat
            logger.debug(self.plugin_name + ' plugin configured')
