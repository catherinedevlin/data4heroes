import sys

import jsonlines
import pandas as pd

URL = "http://localhost:8000/ohio-supers.html"

def json_rows(row):
    if row["Based in"]:
        yield {
            "entity_1": {
                "type": "Person",
                "name": row.Name,
            },
            "entity_2": {"type": "Place", "name": row["Based in"]},
            "relationship": "based_in",
        }
    for power_num in range(1, 4):
        field = f"Power {power_num}"
        if row[field]:
            yield {
                "entity_1": {
                    "type": "Person",
                    "name": row.Name,
                },
                "entity_2": {"type": "Power", "name": row[field]},
                "relationship": "has",
            }

frames = pd.read_html(URL)
df = frames[0].fillna('')
with jsonlines.Writer(sys.stdout) as writer:
    for idx, row in df.iterrows():
        writer.write_all(json_rows(row))

