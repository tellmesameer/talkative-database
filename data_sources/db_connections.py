from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME", "zumloadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "zumlo@5003")
DB_HOSTNAME = os.getenv("DB_HOSTNAME", "zumlodb.database.windows.net")
DB_NAME = os.getenv("DB_NAME", "dev_db")

# Use the driver that worked in your test
ODBC_DRIVER = "ODBC Driver 18 for SQL Server"

# Sample manually constructed table_info
mssql_info = """
Available schemas and tables:

- ai.AIConversations
- wellness.vw_UserWellnessJson
- wellness.SP_HolisticGoalView
- user.Users
- document.Documents
...

Example queries:
SELECT TOP 5 * FROM [ai].[AIConversations] ORDER BY 1 DESC;
SELECT * FROM wellness.vw_UserWellnessJson WHERE UserId = 1322;
SELECT * FROM [wellness].[SP_HolisticGoalView] WHERE GoalId = '595' AND UserId = 386 AND Duration = 'Month';
"""




def get_database_configs():
    configs = {}

    # SQLite
    try:
        sqlite_db = SQLDatabase.from_uri("sqlite:///myDataBase.db")
        configs["sqlite"] = {
            "db": sqlite_db,
            "description": "Local SQLite DB — Northwind retail data",
            "table_info": mssql_info ,
        }
    except Exception as e:
        configs["sqlite"] = {
            "db": None,
            "description": "SQLite unavailable",
            "table_info": f"SQLite error: {str(e)}"
        }

    # MSSQL (Azure)
    try:
        print("\nAttempting SQLAlchemy MSSQL connection...")

        odbc_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={DB_HOSTNAME};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )

        params = quote_plus(odbc_str)
        conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
        print("SQLAlchemy connection string:", conn_str)

        mssql_db = SQLDatabase.from_uri(conn_str)

        # 💡 Replace get_table_info with a simple test query
        result = mssql_db.run("SELECT TOP 1 name FROM sys.tables")
        print("✅ MSSQL test query result:", result)

        configs["mssql"] = {
            "db": mssql_db,
            "description": "Azure MSSQL DB — Your production data",
            "table_info": "Manually loaded - skipped get_table_info() for now"
        }
    except Exception as e:
        print("❌ MSSQL connection failed:", e)
        configs["mssql"] = {
            "db": None,
            "description": "MSSQL unavailable",
            "table_info": f"MSSQL error: {str(e)}"
        }


    return configs
