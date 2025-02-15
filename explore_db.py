from sqlalchemy import create_engine, inspect
import pandas as pd
import secret  # Import our secrets file


def main():
    # Construct the connection string using details from secrets.py
    connection_string = (
        f"postgresql://{secret.DB_USER}:{secret.DB_PASS}"
        f"@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    )
    engine = create_engine(connection_string)

    # Create an inspector to retrieve metadata about the database
    inspector = inspect(engine)

    # Get the list of tables in the 'public' schema
    tables = inspector.get_table_names(schema="public")
    print("Tables in the Northwind (north_explore) database:")
    for table in tables:
        print(f"- {table}")

    # For each table, print its columns and a sample of data
    for table in tables:
        print("\n======================")
        print(f"Table: {table}")
        print("======================")

        # Get column details for the table
        columns = inspector.get_columns(table, schema="public")
        print("Columns:")
        for col in columns:
            print(f"  {col['name']} ({col['type']})")

        # Retrieve and print a sample of data (first 5 rows)
        try:
            df = pd.read_sql_table(table, engine, schema="public")
            print("\nSample Data:")
            print(df.head())
        except Exception as e:
            print(f"Could not retrieve data for table {table}: {e}")


if __name__ == "__main__":
    main()
