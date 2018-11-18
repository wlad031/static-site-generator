import os

from utils.logging import logger
from plugins.plugin import Plugin


class AboutPlugin(Plugin):
    TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates')

    def __init__(self, config_dir):
        super().__init__('About', config_dir, self.TEMPLATES_DIR, 'config_about.yaml')

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
