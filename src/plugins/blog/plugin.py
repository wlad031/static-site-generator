import os
from codecs import open

from utils.logging import logger
from plugins.plugin import Plugin

from markdown2 import Markdown
from CommonMark import commonmark as parse_md

HTML = '.html'


class BlogPlugin(Plugin):
    TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates')

    markdowner = Markdown(extras=[
        # 'code-friendly',
        # # 'code-color',
        # 'cuddled-lists',
        'fenced-code-blocks',
        # 'footnotes',
        # 'header-ids',
        # # 'link-patterns',
        # 'markdown-in-html',
        # 'metadata',
        # 'nofollow',
        # 'numbering',
        # 'pyshell',
        # 'tables',
        # 'use-file-vars',
        # 'wiki-tables',
    ])

    def __init__(self, config_dir):
        super().__init__('Blog', config_dir, self.TEMPLATES_DIR, 'config_blog.yaml')

    def generate(self):
        logger.info('Blog plugin pages generating...')
        res = [
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
        logger.info('Blog plugin pages generated')
        return res

    def __generate_main_pages(self):
        file_prefix = 'blog_page_'
        template = 'all_articles.html'
        res = []

        paginated_articles = BlogPlugin.__paginate_articles(
            self.cfg['articles'], per_page=self.cfg['articles_per_page'])
        for i, page in enumerate(paginated_articles):
            cur_page = i + 1

            articles = [{
                'title': article['title'],
                'date': article.get('date', None),
                'tags': article.get('tags', None),
                'description': article.get('description', None),
                'draft': bool(article.get('draft', False)),
                'link': BlogPlugin.__gen_article_file_name(article)
            } for article in page]

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

        logger.info('Main pages generated')

        return res

    def __generate_all_tags_page(self):
        template = 'all_tags.html'

        tags = {}
        for tag in self.cfg['tags']:
            tags[tag] = []
        for article in self.cfg['articles']:
            article_tags = article.get('tags', [])
            for article_tag in article_tags:
                if article_tag not in self.cfg['tags']:
                    tags[article_tag] = []
                tags[article_tag].append({
                    'title': article['title'],
                    'date': article.get('date', None),
                    'draft': bool(article.get('draft', False)),
                    'link': BlogPlugin.__gen_article_file_name(article),
                })

        page = self.j2.get_template(template).render(tags=tags)

        logger.info('All tags page generated')

        return page

    def __generate_article_pages(self):
        template = 'article.html'
        res = []

        for article in self.cfg['articles']:
            if not bool(article.get('draft', False)):
                with open(os.path.join(
                        self.config_dir, self.cfg['articles_dir'], article['md']),
                        'r', 'utf8') as md_f:
                    md_f_read = md_f.read()
                    res.append({
                        'file': BlogPlugin.__gen_article_file_name(article),
                        'html': self.j2.get_template(template).render(article={
                            'title': article['title'],
                            'date': article.get('date', None),
                            'description': article.get('description', None),
                            'tags': article.get('tags', None),
                            'text': parse_md(md_f_read)#self.markdowner.convert(md_f_read)
                        })
                    })

        logger.info('Articles pages generated')

        return res

    @staticmethod
    def __gen_article_file_name(article):
        if bool(article.get('draft', False)):
            return None
        prefix = 'blog_article_'
        return prefix + str(article['link']) + HTML

    @staticmethod
    def __paginate_articles(articles, per_page=10):
        res, k, n = [[]], 0, 0
        for article in articles:
            if k < per_page:
                res[n].append(article)
                k += 1
            else:
                res.append([article])
                k, n = 0, n + 1
        return res
