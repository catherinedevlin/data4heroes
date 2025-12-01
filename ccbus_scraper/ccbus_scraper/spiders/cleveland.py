import scrapy


class ClevelandSpider(scrapy.Spider):
    name = "cleveland"
    start_urls = [
        "http://localhost:8000/strongarm.html",
    ]

    def parse(self, response):

        article_content = response.css("div.entry-content")
        yield {"url": response.url}
        for anchor in article_content.css("a"):
            yield response.follow(anchor)
