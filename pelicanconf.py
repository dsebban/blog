#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Daniel Sebban'
SITENAME = u'Daniel Sebban\'s Blog'
SITEURL = 'http://dsebban.github.io/blog'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

THEME = 'pelican-themes/blue-penguin'


SOCIAL = (
          ('LinkedIn', 'https://www.linkedin.com/profile/view?id=14011575'),
	  ('github','https://github.com/dsebban'),	
)

ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'


