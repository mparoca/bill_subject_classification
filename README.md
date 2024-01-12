# Spark NLP for Bill Classification and Graph-Based Insights with Neo4j

## Description
This repository contains the code and documentation for a data processing and analysis pipeline focused on legislative bill data from OpenStates. The project aims to categorize bills from the New York State Assembly session 2022-2023 into distinct subject and load the results into a Neo4j graph database. 

## Data Source
The data is sourced from [OpenStates](https://open.pluralpolicy.com/data/session-csv/), focusing on the latest NYS Assembly session. The dataset includes bill identifiers, titles, abstracts, names, and sponsoring legislators. The data was bulk downloaded to overcome API request limitations.

## Pipeline Components
1. `fetch_data.py`  - Downloads and stores legislative data in `data/raw`
2. `data_preprocessing.py` - Filters data to the specified session and splits it into `NY_Assembly_bills.json` and `NY_Assembly_bill_sponsors.json`.
3. `zero_shot_classification.py`  - Uses [PySpark](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data.) and [Spark NLP](https://sparknlp.org/) for classifying bills into predefined topics using the BERT model for zero-shot classification.
4. `neo4j_ingestion.py`  - Ingests processed data into [Neo4j Aura](https://neo4j.com/cloud/platform/aura-graph-database/), a cloud-based graph database for advanced analysis and visualization.

## Graph Database Schema
The Neo4j graph database schema includes:
- Nodes: Bill, Legislator, Subject
- Relationships: IS_SPONSOR (between Legislator and Bill), HAS_SUBJECT (between Bill and Subject)

## Acknowledgements
This project utilizes data from OpenStates and technologies like Apache Spark, Spark NLP, and Neo4j Aura.

- The Apache Software Foundation. (2023). SparkR: R front end for 'Apache Spark'. [Apache Spark](https://spark.apache.org)
- Lan, Z., Chen, M., Goodman, S., Gimpel, K., Sharma, P., & Soricut, R. (2019). Albert: A lite bert for self-supervised learning of language representations. [arXiv preprint arXiv:1909.11942](https://arxiv.org/abs/1909.11942).
- Kocaman, V., & Talby, D. (2021). Spark NLP: natural language understanding at scale. Software Impacts, 8, 100058. DOI: [10.1016/j.simpa.2021.100058](https://doi.org/10.1016/j.simpa.2021.100058).

## Contact

For more information please contact:  

| Name            |            Email                       |
|-----------------|:--------------------------------------:|
| Maria Aroca     | mparoca@iu.edu or mp.arocav2@gmail.com |




