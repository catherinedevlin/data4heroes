from pathlib import Path
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "ioi_blog"
    start_urls = [
        "http://localhost:8000/blog.html",
    ]

    def parse(self, response):
        if response.status == 200:
            self.log(f"Scraped {response.url}")
            return {"contents": response.text}