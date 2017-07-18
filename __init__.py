import feedparser
import time
from os.path import dirname
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'akailash'

LOGGER = getLogger(__name__)

try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

html_parser = HTMLParser()

def clean_html(raw_html):
    """ Remove html tags from string. """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = html_parser.unescape(cleantext)
    return unicodedata.normalize('NFKD', cleantext).encode('ascii', 'ignore')

class OpenNewsSkill(MycroftSkill):
    def __init__(self):
        super(OpenNewsSkill, self).__init__(name="OpenNewsSkill")
        self.source = {'Google': 'https://news.google.com/news/?output=rss&ned=<locale>&hl=<language>&q=<topic>', 'Reddit': 'https://www.reddit.com/search.xml?q=<topic>&sort=new.rss'}
        self.process = None

    def initialize(self):
        intent = IntentBuilder("OpenNewsIntent") \
        .require("NewsKeyword") \
        .require("NewsSourceWord") \
        .optionally("SearchTerms") \
        .optionally("NewsTopicWord") \
        .build()
        self.register_intent(intent, self.handle_intent)


    def handle_intent(self, message):
        if message.data.get('NewsTopicWord'):
            topic = message.data.get("SearchTerms")
        else:
            topic = ''

        source = self.source[message.data['NewsSourceWord']]
        source = source.replace('<locale>','in')
        source = source.replace('<language>','en')
        source = source.replace('<topic>',topic)
        LOGGER.info(source)
        feed = feedparser.parse(source)
        #self.stop(self)

        self.speak_dialog('open.news')
        self.speak('Here\'s the latest headlines from ' +
                message.data['NewsSourceWord'])
        items = feed.get('items', [])

        if len(items) > 5:
            items = items[:5]

        for i in items:
            self.speak(i['title'])
#            self.speak(clean_html(i['description']))


def create_skill():
    return OpenNewsSkill()
