# test_mssql_connection.py

from data_sources.db_connections import get_database_configs

def test_mssql():
    configs = get_database_configs()
    mssql_config = configs.get("mssql")

    print("\n--- MSSQL Connection Test ---")
    if mssql_config is None or mssql_config.get("db") is None:
        print("❌ MSSQL connection failed:")
        if mssql_config is not None:
            print(mssql_config.get("table_info"))
        else:
            print("No configuration found for MSSQL.")
    else:
        print("✅ Connected to MSSQL")
        print("ℹ️ Description:", mssql_config["description"])
        print("🔎 Sample Table Info:\n", mssql_config["table_info"][:500])

if __name__ == "__main__":
    test_mssql()
