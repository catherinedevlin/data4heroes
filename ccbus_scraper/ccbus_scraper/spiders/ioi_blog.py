import scrapy

EP_TITLE = "div.media-card__header a::text"
NAV_BUTTON = "nav.justify-center a.btn::attr(href)"


class QuotesSpider(scrapy.Spider):
    name = "ioi_blog"
    start_urls = [
        "http://localhost:8000/blog.html",
    ]

    def parse(self, response):
        for line in response.css(EP_TITLE).getall():
            pieces = line.split("Interview:")
            if len(pieces) == 2:
                yield {
                    "person1": "Henry Fnord",
                    "person2": pieces[1].strip(),
                    "relationship": "allied",
                }
        for link in response.css(NAV_BUTTON).getall():
            yield scrapy.Request(response.urljoin(link))
