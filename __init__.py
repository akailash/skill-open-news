import feedparser
import time
from os.path import dirname
import re
from pycountry import countries

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
        self.headlines = None

    def initialize(self):
        for country in countries:
            self.register_vocabulary(country.name, "NewsLocaleWord")
            LOGGER.info(country)

        intent = IntentBuilder("OpenNewsIntent") \
        .require("NewsKeyword") \
        .require("NewsSourceWord") \
        .optionally("SearchTerms") \
        .optionally("NewsTopicWord") \
        .optionally("NewsLocaleWord") \
        .build()
        self.register_intent(intent, self.handle_intent)


    def handle_intent(self, message):
        if message.data.get('NewsTopicWord'):
            topic = message.data.get("SearchTerms")
        else:
            topic = ''

        if message.data.get('NewsLocaleWord'):
            locale = countries.get(message.data.get('NewsLocaleWord')).alpha_2
        else:
            locale = 'in'

        source = self.source[message.data['NewsSourceWord']]
        source = source.replace('<locale>',locale)
        source = source.replace('<language>','en') #Currently support only English
        source = source.replace('<topic>',topic)
        LOGGER.info(source)
        feed = feedparser.parse(source)

        self.speak('Here\'s the latest headlines from ' +
                message.data['NewsSourceWord'])
        items = feed.get('items', [])

        if len(items) > 5:
            items = items[:5]
        self.headlines = items
        for i in items:
            self.speak(i['title'])
            LOGGER.info(i['link'])
            time.sleep(2)
        self.speak_dialog(open.news.stop)

    def handle_more_intent(self, message):
        if message.data.get('NewsTopicWord'):
            topic = message.data.get("SearchTerms")
        else:
            self.speak("Sorry, I don't understand. Tell me which headline you want to read more about.")
            for i in self.headlines:
                self.speak(i['title'])
            return
        for i in self.headlines:
            if any(topic in i):
                self.speak(i['published'])
                self.speak(clean_html(i['description']))
                time.sleep(2)
        self.speak_dialog(open.news.stop)


def create_skill():
    return OpenNewsSkill()
