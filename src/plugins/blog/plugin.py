import os
from codecs import open

from utils.logging import logging
from utils.json import pretty_json
from utils.time import datetimeformat

import yaml

import jinja2 as j
from markdown2 import Markdown

HTML = '.html'


class BlogPlugin(object):

    TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates')

    markdowner = Markdown(extras=[
        'code-friendly',
        'code-color',
        'cuddled-lists',
        'fenced-code-blocks',
        'footnotes',
        'header-ids',
        # 'link-patterns',
        'markdown-in-html',
        'metadata',
        'nofollow',
        'numbering',
        'pyshell',
        'tables',
        'use-file-vars',
        'wiki-tables',
    ])

    def __init__(self, config_dir):
        self.config_dir = config_dir

        with open(os.path.join(config_dir, 'config_blog.yaml'), 'r', 'utf8') as cfg_f:
            self.cfg = yaml.load(cfg_f)

            logging.debug('Blog plugin config:')
            logging.debug(pretty_json(**self.cfg))

            self.j2 = j.Environment(loader=j.FileSystemLoader(self.TEMPLATES_DIR),
                                    trim_blocks=True)
            self.j2.filters['datetimeformat'] = datetimeformat

    def generate(self):
        return [
            {
                'navbar': {'name': 'Articles', 'index': True},
                'file': 'blog_page_1.html',
                'multiple': True,
                'pages': self.__generate_main_pages()
            },
            {
                'navbar': {'name': 'Tags'},
                'file': 'blog_tags.html',
                'html': self.__generate_all_tags_page()
            },
            {
                'multiple': True,
                'pages': self.__generate_article_pages()
            }
        ]

    def __generate_main_pages(self):
        file_prefix = 'blog_page_'
        template = 'all_articles.html'
        res = []

        paginated_articles = BlogPlugin.__paginate_articles(
            self.cfg['articles'], per_page=self.cfg['articles_per_page'])
        for i, page in enumerate(paginated_articles):
            cur_page = i + 1

            articles = [{
                'title': a['title'],
                'date': a['date'],
                'tags': a['tags'],
                'description': a['description'],
                'link': BlogPlugin.__gen_article_file_name(a),
            } for a in page]

            pagination = {
                'total_pages': len(paginated_articles),
                'current_page': cur_page
            }

            res.append({
                'file': file_prefix + str(cur_page) + HTML,
                'html': self.j2.get_template(template).render(
                    articles=articles,
                    pagination=pagination,
                    file_prefix=file_prefix
                )
            })

        return res

    def __generate_all_tags_page(self):
        template = 'all_tags.html'

        tags = {}
        for tag in self.cfg['tags']:
            tags[tag] = []
        for article in self.cfg['articles']:
            article_tags = article['tags']
            for article_tag in article_tags:
                if article_tag not in self.cfg['tags']:
                    tags[article_tag] = []
                tags[article_tag].append({
                    'title': article['title'],
                    'date': article['date'],
                    'link': BlogPlugin.__gen_article_file_name(article),
                })

        return self.j2.get_template(template).render(tags=tags)

    def __generate_article_pages(self):
        template = 'article.html'
        res = []

        for article in self.cfg['articles']:
            with open(os.path.join(
                    self.config_dir, self.cfg['articles_dir'], article['md']),
                    'r', 'utf8') as md_f:
                res.append({
                    'file': BlogPlugin.__gen_article_file_name(article),
                    'html': self.j2.get_template(template).render(article={
                        'title': article['title'],
                        'date': article['date'],
                        'description': article['description'],
                        'tags': article['tags'],
                        'text': self.markdowner.convert(md_f.read()).replace('\n', '')
                    })
                })

        return res

    @staticmethod
    def __gen_article_file_name(article):
        prefix = 'blog_article_'
        return prefix + str(article['link']) + '.html'

    @staticmethod
    def __paginate_articles(articles, per_page=10):
        res = [[]]

        k, n = 0, 0
        for article in articles:
            if k < per_page:
                res[n].append(article)
                k += 1
            else:
                n += 1
                res.append([article])
                k = 0

        return res
