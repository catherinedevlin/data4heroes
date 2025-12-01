import scrapy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

EP_TITLE = "div.media-card__header a::text"
EP_BODY = "div.media-card__body p::text"

NAV_BUTTON = "nav.justify-center a.btn::attr(href)"
analyzer = SentimentIntensityAnalyzer()


class IOISpider(scrapy.Spider):
    name = "ioi"
    start_urls = [
        "http://localhost:8000/pod.html",
    ]

    def parse(self, response):
        for card in response.css("div.media-card"):
            line = card.css(EP_TITLE).get()
            # `card` supports css paths like `response` does
            pieces = line.split("Interview:")
            if len(pieces) == 2:
                body = "\n".join(card.css(EP_BODY).getall())
                sentiment = analyzer.polarity_scores(body)["compound"]
                relationship = "allied" if sentiment > -0.5 else "opposed"
                yield {
                    "entity_1": {"type": "Person", "name": "Henry Fnord"},
                    "entity_2": {"type": "Person", "name": pieces[1].strip()},
                    "relationship": relationship,
                }

        for link in response.css(NAV_BUTTON).getall():
            yield scrapy.Request(response.urljoin(link))
