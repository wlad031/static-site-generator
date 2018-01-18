import os
from codecs import open

import config

from utils.logging import logger
from utils.json import pretty_json
from utils.file import copytree, rmtree, copyfile
from utils.watch import watcher

import argparse
import jinja2 as j

plugins = config.PLUGINS

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BUILD_DIR = os.path.join(CUR_DIR, config.OUTPUT_DIR)
STATIC_DIR = os.path.join(CUR_DIR, '../static')
TEMPLATES_DIR = os.path.join(CUR_DIR, '../templates')


def main(config_dir):
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
    if os.path.exists(BUILD_DIR):
        rmtree(BUILD_DIR)
    copytree(STATIC_DIR, BUILD_DIR)

    j2 = j.Environment(loader=j.FileSystemLoader(TEMPLATES_DIR),
                       trim_blocks=True)

    generated = []
    navs = []
    index = None

    for p in plugins:
        plugin_obj = p(config_dir=config_dir)
        pages = plugin_obj.generate()

        for page in pages:
            navbar = page.get('navbar', None)
            if navbar is not None:
                navs.append({'name': navbar['name'], 'link': page['file']})
                if navbar.get('index', False):
                    index = page['file']

        generated.append(pages)

    if index is None:
        raise Exception('Please specify one index page')

    for g in generated:
        for page in g:
            if bool(page.get('multiple', False)):
                for _p in page['pages']:
                    html = _p['html']
                    html = j2.get_template('index.html').render(
                        title=config.TITLE,
                        footer_content=config.FOOTER_CONTENT,
                        content=html,
                        navs=navs
                    )
                    with open(os.path.join(BUILD_DIR, _p['file']), 'w', 'utf8') as f:
                        f.write(html)

            else:
                file = page['file']
                html = page['html']
                html = j2.get_template('index.html').render(
                    title=config.TITLE,
                    footer_content=config.FOOTER_CONTENT,
                    content=html,
                    navs=navs
                )
                with open(os.path.join(BUILD_DIR, file), 'w', 'utf8') as f:
                    f.write(html)

    copyfile(os.path.join(BUILD_DIR, index), os.path.join(BUILD_DIR, 'index.html'))


def main_watch(config_dir):

    def fun():
        main(config_dir)
        logger.info('Changes watching...')
    watcher.set_fun(lambda: fun())

    watcher.add_watch(TEMPLATES_DIR)
    watcher.add_watch(STATIC_DIR)
    watcher.add_watch(config_dir)

    init_plugins(config_dir)
    main(config_dir)

    logger.info('Changes watching starting...')
    watcher.start()


def init_plugins(config_dir):
    return [p(config_dir=config_dir) for p in plugins]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Static Blog Generator')
    parser.add_argument('--config', required=True, type=str)
    parser.add_argument('--watch', required=False, action='store_true')

    args = vars(parser.parse_args())

    logger.debug('Program arguments:')
    logger.debug(pretty_json(**args))

    config_dir = args['config']
    if not os.path.exists(config_dir):
        logger.error('Config directory does not exist')
        exit(1)

    if args['watch']:
        main_watch(config_dir)
    else:
        init_plugins(config_dir)
        main(config_dir)
