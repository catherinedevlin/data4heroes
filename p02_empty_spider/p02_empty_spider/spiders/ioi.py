
import scrapy

class IOISpider(scrapy.Spider):
    name = "ioi"
    start_urls = [
        "http://localhost:8000/pod.html",
    ]

    def parse(self, response):
        if response.status == 200:
            self.log(f"Scraped {response.url}")
            return {"contents": response.text}
