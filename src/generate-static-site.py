import argparse
import os

import config

from utils.logging import logging
from utils.json import pretty_json
from utils.file import copytree, rmtree, copyfile

import jinja2 as j

plugins = config.PLUGINS


def main(args):
    logging.debug('Program arguments:')
    logging.debug(pretty_json(**args))

    cur_dir = os.path.dirname(os.path.realpath(__file__))

    static_dir = os.path.join(cur_dir, config.STATIC_DIR)
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    out_dir = os.path.join(cur_dir, config.OUTPUT_DIR)
    if os.path.exists(out_dir):
        rmtree(out_dir)
    copytree(static_dir, out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    templates_dir = os.path.join(cur_dir, config.TEMPLATES_DIR)
    j2 = j.Environment(loader=j.FileSystemLoader(templates_dir),
                       trim_blocks=True)

    generated = []
    navs = []
    index = None

    for p in plugins:
        plugin_obj = p['plugin'](args)
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
                for concrete_page in page['pages']:
                    html = concrete_page['html']
                    html = j2.get_template('index.html').render(
                        title=config.TITLE,
                        footer_content=config.FOOTER_CONTENT,
                        content=html,
                        navs=navs
                    )
                    with open(os.path.join(out_dir, concrete_page['file']), 'w') as f:
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
                with open(os.path.join(out_dir, file), 'w') as f:
                    f.write(html)

    copyfile(os.path.join(out_dir, index), os.path.join(out_dir, 'index.html'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Static Blog Generator')

    for plugin in plugins:
        arg = plugin.get('params', None)
        if arg is not None:
            parser.add_argument(*arg['args'], **arg['kwargs'])

    main(vars(parser.parse_args()))
