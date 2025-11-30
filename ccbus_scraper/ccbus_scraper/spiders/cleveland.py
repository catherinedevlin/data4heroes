import itertools
import re

import scrapy
from flair.data import Sentence
from flair.nn import Classifier

EP_TITLE = "div.media-card__header a::text"
EP_BODY = "div.media-card__body p::text"
DATELINE = re.compile(r"\n([^\n]*?) \-\- ")

NAV_BUTTON = "nav.justify-center a.btn::attr(href)"
tagger = Classifier.load("ner")


class ClevelandSpider(scrapy.Spider):
    name = "cleveland"
    start_urls = [
        "http://localhost:8000/strongarm.html",
    ]

    def parse(self, response):

        title = response.css("title::text").get()
        article_content = response.css("div.entry-content")
        paragraphs = article_content.css("p::text").getall()
        text = "\n\n".join([title, *paragraphs])
        location = DATELINE.search(text).group(1).title()
        people = get_people(text)
        yield from relations(location, people)
        for anchor in article_content.css("a"):
            yield response.follow(anchor)


def get_people(text):
    text = Sentence(text)
    tagger.predict(text)

    last_names = {}
    for label in text.get_labels():
        if label.value != "PER":
            continue
        last_name = label.data_point.text.split()[-1]
        if last_name not in last_names:
            last_names[last_name] = label.data_point.text
    yield from last_names.values()

    # "Nell Strongarm" and "Strongarm" -> same
    # Orville and Wilbur Wrong -> different!


def relations(location, people):
    for person in people:
        yield {
            "entity_1": {"type": "Person", "name": person},
            "entity_2": {"type": "Place", "name": location},
            "relationship": "active_in",
        }
    for person1, person2 in itertools.combinations(people, 2):
        yield {
            "entity_1": {"type": "Person", "name": person1},
            "entity_2": {"type": "Person", "name": person2},
            "relationship": "encountered",
        }
