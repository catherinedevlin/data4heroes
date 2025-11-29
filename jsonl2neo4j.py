import jsonlines
from neo4j import GraphDatabase, RoutingControl

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "4justice")


def save(driver, row):
    relationship = row["relationship"].upper()
    type2 = row["entity_2"]["type"]
    driver.execute_query(
        f"MERGE (entity_1:Person {{name: $name}}) "
        f"MERGE (entity_2:{type2} {{name: $name_2}}) "
        f"MERGE (entity_1)-[:{relationship}]->(entity_2) ",
        name=row["entity_1"]["name"],
        name_2=row["entity_2"]["name"],
        database_="neo4j",
    )


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with jsonlines.open("heroes.jsonl") as reader:
        for row in reader:
            save(driver, row)
