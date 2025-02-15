import os
import pandas as pd
from sqlalchemy import create_engine, text
import secret  # Contains DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


def get_engine():
    """Construct the SQLAlchemy engine using credentials from secret.py."""
    connection_string = (
        f"postgresql://{secret.DB_USER}:{secret.DB_PASS}"
        f"@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    )
    engine = create_engine(connection_string)
    return engine


def extract_data(file_path):
    """Extract data from a CSV file using Pandas."""
    try:
        df = pd.read_csv(file_path)
        print(f"Extracted {len(df)} rows from {file_path}")
        return df
    except Exception as e:
        print(f"Error extracting {file_path}: {e}")
        return None


def transform_data(df):
    """
    Perform data transformation and cleaning.
    For example: strip whitespace from all string columns.
    """
    if df is None:
        return None
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    return df


def drop_table_cascade(engine, table_name):
    """
    Drop the table if it exists, using CASCADE to remove dependent objects.
    Uses engine.connect() with text() for SQL execution.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS public.{table_name} CASCADE"))
            conn.commit()  # Commit the DDL change
        print(f"Dropped table {table_name} with CASCADE.")
    except Exception as e:
        print(f"Error dropping table {table_name}: {e}")


def load_data(engine, table_name, df):
    """
    Load the DataFrame into the specified table in the database.
    Drops the table with CASCADE first, then creates it fresh.
    """
    try:
        drop_table_cascade(engine, table_name)
        df.to_sql(table_name, engine, schema="public", if_exists="replace", index=False)
        print(f"Loaded data into table: {table_name}")
    except Exception as e:
        print(f"Error loading data into table {table_name}: {e}")


def main():
    # Directory where CSV files are stored
    data_dir = "data"

    # Mapping of CSV filenames to database table names
    files_to_tables = {
        "customers.csv": "customers",
        "products.csv": "products",
        "orders.csv": "orders",
        "order_details.csv": "order_details",
    }

    engine = get_engine()

    for filename, table_name in files_to_tables.items():
        file_path = os.path.join(data_dir, filename)
        df = extract_data(file_path)
        df = transform_data(df)
        if df is not None:
            load_data(engine, table_name, df)

    print("ETL process completed successfully.")


if __name__ == "__main__":
    main()
