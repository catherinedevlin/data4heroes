from pathlib import Path
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "ioi_blog"
    start_urls = [
        "http://localhost:8000/blog.html",
    ]

    def parse(self, response):
        for line in response.css("div.media-card__header a::text").getall():
            pieces = line.split("Interview:")
            if len(pieces) == 2:
                yield {"person1": "Henry Fnord",
                       "person2": pieces[1].strip(),
                       "relationship": "allied"}