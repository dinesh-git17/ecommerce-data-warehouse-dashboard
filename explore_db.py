from sqlalchemy import create_engine, inspect
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import secret  # Import your connection details from secret.py

console = Console()


def print_tables(inspector, schema="public"):
    tables = inspector.get_table_names(schema=schema)
    if not tables:
        console.print("[bold red]No tables found in the schema.[/bold red]")
        return []
    console.print(
        Panel.fit(
            "[bold green]Tables in the Northwind (north_explore) Database:[/bold green]"
        )
    )
    for table in tables:
        console.print(f"[yellow]- {table}[/yellow]")
    return tables


def print_table_details(inspector, table, schema="public"):
    columns = inspector.get_columns(table, schema=schema)
    table_obj = Table(title=f"Table: {table}", show_lines=True)
    table_obj.add_column("Column Name", style="bold cyan")
    table_obj.add_column("Data Type", style="bold magenta")
    for col in columns:
        table_obj.add_row(col["name"], str(col["type"]))
    console.print(table_obj)


def print_sample_data(engine, table, schema="public"):
    try:
        df = pd.read_sql_table(table, engine, schema=schema)
        if df.empty:
            console.print(f"[red]No data found in table {table}.[/red]")
            return
        table_obj = Table(title=f"Sample Data: {table}", show_lines=True)
        for col in df.columns:
            table_obj.add_column(col, style="green")
        for _, row in df.head().iterrows():
            table_obj.add_row(*[str(x) for x in row])
        console.print(table_obj)
    except Exception as e:
        console.print(
            f"[bold red]Could not retrieve data for table {table}: {e}[/bold red]"
        )


def main():
    # Construct the connection string using details from secret.py
    connection_string = (
        f"postgresql://{secret.DB_USER}:{secret.DB_PASS}"
        f"@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    )
    engine = create_engine(connection_string)
    inspector = inspect(engine)

    console.print(
        Panel.fit(
            "[bold blue]Exploring the Northwind (north_explore) Database[/bold blue]"
        )
    )

    tables = print_tables(inspector, schema="public")
    if tables:
        for table in tables:
            console.print(
                Panel.fit(f"[bold green]Details for table: {table}[/bold green]")
            )
            print_table_details(inspector, table, schema="public")
            console.print()  # Blank line
            print_sample_data(engine, table, schema="public")
            console.print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
