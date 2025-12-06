
import scrapy

class IOISpider(scrapy.Spider):
    name = "ioi"
    start_urls = [
        "http://localhost:8000/pod.html",
    ]

    def parse(self, response):
        for line in response.css("div.media-card__header a::text").getall():
            pieces = line.split("Interview:")
            if len(pieces) == 2:
                yield {"person1": "Henry Fnord",
                    "person2": pieces[1].strip(),
                    "relationship": "allied"}
