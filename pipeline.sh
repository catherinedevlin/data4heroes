uv run get-html.py > supers.jsonl
cd ccbus_scraper 
uv run scrapy crawl ioi -o ../supers.jsonl
uv run scrapy crawl cleveland -o ../supers.jsonl
cd ..
uv run jsonl2neo4j.py supers.jsonl 