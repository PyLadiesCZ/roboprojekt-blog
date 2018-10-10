from danube_delta.settings import *

AUTHOR = 'PyLadies Brno'
SITENAME = 'RoboProjekt'
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

if PRODUCTION:
    SITEURL = 'https://pyladiescz.github.io/roboprojekt-blog'
