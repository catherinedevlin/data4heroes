import json

import ollama
import scrapy

class ClevelandLLMSpider(scrapy.Spider):
    name = "cleveland_llm"
    start_urls = [
        "http://localhost:8000/virtue-strongarm.html",
    ]

    def parse(self, response):

        title = response.css("title::text").get()
        article_content = response.css("div.entry-content")
        paragraphs = article_content.css("p::text").getall()
        text = "\n\n".join([title, *paragraphs])
        yield from ask_llm(text)


PROMPT = """
I'm going to give you the text of a newspaper article that involves
one or more superpowered beings (heroes and/or villains).  Please 
briefly summarize the article in JSON format, with an array of 
objects (no more than 5) using a format following this example.
entity_1 should always be a Person.  Relationship should be one
or two words describing how entity_2 interacted with entity_2.  
entity_1 and entity_2 should always have a "name" and a "type".

[ {"entity_1": {"type": "Person", "name": "Motown Menace"}, "entity_2": {"type": "Person", "name": "Captain Columbus"}, "relationship": "fought"},
{"entity_1": {"type": "Person", "name": "Indiana Jane"}, "entity_2": {"type": "Person", "name": "Captain Columbus"}, "relationship": "helped"}, ]

Here is the article to summarize:
"""


def ask_llm(text):
    response = ollama.generate(model="llama3.2", prompt=PROMPT + text)
    # Empirically, JSON is included in 2nd paragraph
    paragraphs = response.response.split("\n\n")
    return json.loads(paragraphs[1])

# 'Here is a summary of the article in JSON format:\n\n[\n{"entity_1": {"type": "Person", "name": "Mud Hen"}, "entity_2": {"type": "Nell Strongarm\'s Crime Capsule"}, "relationship": "defended"},\n{"entity_1": {"type": "Nell Strongarm\'s Crime Capsule"}, "entity_2": {"type": "Toledo Police Department", "relationship": "contacted"}},\n]\n\nNote that I did not include the mention of Captain Columbus in the summary as it was a quote and not directly related to the event. If you would like me to include it, please let me know.\n\nAlso, I assumed that Nell Strongarm\'s Crime Capsule is an entity with its own type (e.g. Vehicle), but since it\'s not explicitly stated in the article, I did not add it as a separate object.'
