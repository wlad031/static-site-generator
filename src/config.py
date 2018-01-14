from plugins.blog import BlogPlugin
from plugins.about import AboutPlugin

OUTPUT_DIR = '../build'
TEMPLATES_DIR = '../templates'
STATIC_DIR = '../static'
PLUGINS = [
    {
        'plugin': BlogPlugin,
        'params': {
            'args': ['--blog-config'],
            'kwargs': {'type': str, 'required': True}
        }
    },
    {
        'plugin': AboutPlugin
    }
]

TITLE = 'Site Title'
FOOTER_CONTENT = 'Copyright &copy; Site copyright 2018'
