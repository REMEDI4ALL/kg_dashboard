# -*- coding: utf-8 -*-

"""Helper functions"""

import pandas as pd
from tqdm import tqdm

from py2neo import Graph
from queries import *

# Neo4J Server
FRAUNHOFER_ADMIN_NAME = "neo4j"
FRAUNHOFER_ADMIN_PASS = "remedi4all-2023"
FRAUNHOFER_URL = "neo4j+s://f43b07b7.databases.neo4j.io:7687"


def connect_to_kg():
    graph = Graph(
        FRAUNHOFER_URL,
        auth=(FRAUNHOFER_ADMIN_NAME, FRAUNHOFER_ADMIN_PASS),
    )
    return graph


def run_all_queries():
    """Run all CYPHER queries and return the results in a dictionary"""
    graph = connect_to_kg()
    queries = [
        ("location", get_location()),
        ("organization", get_organization_info()),
        ("wp", get_wp_info()),
        ("nodes", get_node_counts()),
        ("edges", get_edge_counts()),
        ("node_stats", get_node_stats()),
        ("skillgroups", get_skill_group()),
        ("skills", skill_distribution()),
        ("skills_metadata", skill_metadata()),
        ("skills_info", get_skill_info()),
        ("assays", get_all_assays()),
        ("software", get_all_software()),
        ("target_class", get_all_target_classes()),
        ("partner_info", get_partner_info()),
        ("person_info", get_person_info()),
        ("partner_data", get_all_partner_relationships()),
        ("software_data", get_tech_data("Software")),
        ("assay_data", get_tech_data("Experiment")),
        ("target_data", get_tech_data("TargetClass")),
    ]

    for file_name, query in tqdm(queries):
        df = graph.run(query).to_data_frame()
        df.to_csv(f"./data/{file_name}.csv", index=False)  # Save the data to a CSV file


if __name__ == "__main__":
    run_all_queries()
    print("Data has been successfully saved to CSV files.")
