import jsonlines
from neo4j import GraphDatabase, RoutingControl
import sys

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "4justice")

def save(driver, row):
    relationship = row["relationship"].upper()
    type2 = row["entity_2"]["type"]
    qry = (
        f"MERGE (entity_1:Person {{name: $name}}) \n"
        f"MERGE (entity_2:{type2} {{name: $name_2}}) \n"
        f"MERGE (entity_1)-[:{relationship}]->(entity_2) \n"
    )
    print(qry)
    driver.execute_query(
        qry,
        name=row["entity_1"]["name"],
        name_2=row["entity_2"]["name"],
        database_="neo4j",
    )


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with jsonlines.open(sys.argv[1]) as reader:
        for row in reader:
            save(driver, row)
