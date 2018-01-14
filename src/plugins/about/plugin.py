import os

import jinja2 as j


class AboutPlugin(object):

    def __init__(self, args):
        self.templates_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'templates')

        self.j2 = j.Environment(loader=j.FileSystemLoader(self.templates_dir),
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
        return self.j2.get_template(template).render()
