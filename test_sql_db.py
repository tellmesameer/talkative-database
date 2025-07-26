import os
from dotenv import load_dotenv
import pyodbc

# Azure Database Credentials
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME", "zumloadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "zumlo@5003")
DB_HOSTNAME = os.getenv("DB_HOSTNAME", "zumlodb.database.windows.net")
DB_NAME = os.getenv("DB_NAME", "dev_db")
DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

# List of ODBC Drivers to try
odbc_drivers = ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]

def test_connection(driver):
    try:
        print(f"Trying with driver: {driver}")
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={DB_HOSTNAME};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        conn = pyodbc.connect(connection_string)
        print("✅ Connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Failed to connect using {driver}. Error:\n{e}")

if __name__ == "__main__":
    for driver in odbc_drivers:
        test_connection(driver)