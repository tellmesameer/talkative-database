import os
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from data_sources.aws_tickit_metadata import tickit_metadata


def get_database_configs():
    # Load Redshift URI from environment variables
    aws_rs_user = os.getenv("AMAZON_REDSHIFT_USER")
    aws_rs_password = os.getenv("AMAZON_REDSHIFT_PASSWORD")
    aws_rs_endpoint = os.getenv("AMAZON_REDSHIFT_ENDPOINT")
    aws_rs_uri = f"redshift+psycopg2://{aws_rs_user}:{aws_rs_password}@{aws_rs_endpoint}"

    # SQLite
    try:
        sqlite_db = SQLDatabase.from_uri("sqlite:///myDataBase.db")
        sqlite_info = sqlite_db.get_table_info()
    except Exception as e:
        sqlite_db = None
        sqlite_info = f"Error retrieving table info: {str(e)}"

    # BigQuery
    try:
        project_id = "bigquery-public-data"
        dataset_id = "samples"
        bq_uri = f"bigquery://{project_id}/{dataset_id}"
        bigquery_db = SQLDatabase.from_uri(bq_uri)
        bigquery_query = f"""
            SELECT 
                    table_name,
                    column_name,
                    data_type
               FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
              ORDER BY table_name, ordinal_position
        """
        bigquery_info = QuerySQLDatabaseTool(db=bigquery_db).invoke(bigquery_query)
    except Exception as e:
        bigquery_db = None
        bigquery_info = f"Error retrieving table info: {str(e)}"

    # Redshift
    try:
        redshift_db = SQLDatabase.from_uri(aws_rs_uri)
        redshift_info = tickit_metadata
    except Exception as e:
        redshift_db = None
        redshift_info = f"Error retrieving table info: {str(e)}"

    return {
        "sqlite": {
            "db": sqlite_db,
            "description": "Northwind retail dataset (e.g. customers, products, orders)",
            "table_info": sqlite_info,
        },
        "bigquery": {
            "db": bigquery_db,
            "description": "Public sample datasets from BigQuery (e.g. natality, github activity)",
            "table_info": bigquery_info,
        },
        "redshift": {
            "db": redshift_db,
            "description":  "Tickit ticketing platform sample (e.g. events, users, sales)",
            "table_info": redshift_info,
        },
    }