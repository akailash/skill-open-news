import feedparser
import time
from os.path import dirname
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util import play_mp3
from mycroft.util.log import getLogger

__author__ = 'akailash'

LOGGER = getLogger(__name__)


def clean_html(raw_html):
    """ Remove html tags from string. """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = html_parser.unescape(cleantext)
    return unicodedata.normalize('NFKD', cleantext).encode('ascii', 'ignore')

class OpenNewsSkill(MycroftSkill):
    def __init__(self):
        super(OpenNewsSkill, self).__init__(name="OpenNewsSkill")
        self.source = {'Google': 'https://news.google.com/news/?output=rss&ned=<locale>&hl=<language>&q=<topic>'}
        self.process = None

    def initialize(self):
        intent = IntentBuilder("OpenNewsIntent")
        .require("NewsKeyword")
        .require("NewsSourceWord")
        .build()
        self.register_intent(intent, self.handle_intent)

        intent = IntentBuilder("OpenNewsStopIntent")
        .require("NewsStopVerb")
        .require("NewsKeyword")
        .require("NewsSourceWord")
        .build()
        self.register_intent(intent, self.handle_stop)


    def handle_intent(self, message):
        try:
            if message.data['NewsTopicWord']:
                topic = message.data.get('utterance', '')
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
                self.speak(clean_html(i['description'])

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_stop(self, message):
        #self.stop(self)
        self.speak_dialog('open.news.stop')

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()


def create_skill():
    return OpenNewsSkill()
