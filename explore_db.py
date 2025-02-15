import sys
import os
import datetime
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, inspect, text
import secret  # Contains DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# Import our custom logger from mylogger.py
from mylogger import logger

# For console output using Rich:
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

##########################################
# GLOBAL FUNCTIONS (Console Mode)
##########################################
def get_pivot_advanced_global():
    connection_string = f"postgresql://{secret.DB_USER}:{secret.DB_PASS}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    engine = create_engine(connection_string)
    inspector = inspect(engine)
    return inspector, engine

def get_pivot_traditional_global():
    return get_pivot_advanced_global()

def run_console_mode():
    connection_string = f"postgresql://{secret.DB_USER}:{secret.DB_PASS}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    engine = create_engine(connection_string)
    inspector = inspect(engine)
    
    console.print(Panel.fit("[bold blue]Exploring the Database[/bold blue]"))
    
    tables = inspector.get_table_names(schema="public")
    if not tables:
        console.print("[bold red]No tables found in the database.[/bold red]")
        return
    
    console.print(Panel.fit("[bold green]Tables in the Database:[/bold green]"))
    for table in tables:
        console.print(f"[yellow]- {table}[/yellow]")
    
    for table in tables:
        console.print(Panel.fit(f"[bold green]Details for table: {table}[/bold green]"))
        columns = inspector.get_columns(table, schema="public")
        table_obj = Table(title=f"Columns in {table}", show_lines=True)
        table_obj.add_column("Column Name", style="bold cyan")
        for col in columns:
            table_obj.add_row(col["name"])
        console.print(table_obj)
        try:
            df = pd.read_sql_table(table, engine, schema="public")
            console.print("[bold green]Sample Data:[/bold green]")
            console.print(df.head().to_string())
        except Exception as e:
            console.print(f"[bold red]Error retrieving data for table {table}: {e}[/bold red]")
        console.print("\n" + "-"*50 + "\n")

##########################################
# STREAMLIT DASHBOARD FUNCTIONS
##########################################
def run_streamlit_app():
    import streamlit as st
    import time
    import plotly.express as px

    # Inject custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main .block-container {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Northwind Database Explorer Dashboard")
    st.write("Use the sidebar to choose a view.")

    # Build connection
    connection_string = f"postgresql://{secret.DB_USER}:{secret.DB_PASS}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    engine = create_engine(connection_string)
    inspector = inspect(engine)

    tables = inspector.get_table_names(schema="public")
    if not tables:
        st.error("No tables found in the database.")
        return

    # Create a sidebar selectbox to choose a view.
    available_views = ["Tables", "Analytics", "SQL Runner"]
    selected_view = st.sidebar.selectbox("Choose a view", available_views)

    if selected_view == "Tables":
        st.header("Table Details")
        selected_table = st.selectbox("Select a table", tables)
        # Column descriptions dictionary
        column_descriptions = {
            "customers": {
                "customer_id": "Unique ID for each customer",
                "name": "Customer's full name",
                "email": "Customer email address",
                "registration_date": "Date when the customer registered"
            },
            "products": {
                "product_id": "Unique product identifier",
                "name": "Name of the product",
                "category": "Product category",
                "price": "Unit price",
                "stock_quantity": "Quantity in stock"
            },
            "orders": {
                "order_id": "Unique order identifier",
                "customer_id": "ID of the customer who placed the order",
                "order_date": "Order placement date",
                "total_amount": "Total order amount"
            },
            "order_details": {
                "order_item_id": "Unique ID for each order line",
                "order_id": "Associated order ID",
                "product_id": "Product identifier",
                "quantity": "Quantity ordered",
                "price_at_order": "Price at the time of order"
            }
        }
        st.subheader(f"Details for table: {selected_table}")
        columns = inspector.get_columns(selected_table, schema="public")
        cols_info = ""
        for col in columns:
            desc = column_descriptions.get(selected_table, {}).get(col["name"], "No description available")
            cols_info += f"- **{col['name']}**: {desc}\n"
        st.markdown("### Columns:")
        st.markdown(cols_info)
        try:
            df = pd.read_sql_table(selected_table, engine, schema="public")
            st.markdown("### Sample Data:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error retrieving data for table {selected_table}: {e}")

    elif selected_view == "Analytics":
        st.header("Advanced Analytics")
        st.markdown("### Monthly Sales")
        try:
            query = "SELECT month, orders_count, total_sales FROM monthly_sales ORDER BY month;"
            df_sales = pd.read_sql_query(query, engine)
            df_sales['month'] = pd.to_datetime(df_sales['month'])
            fig = px.line(df_sales, x='month', y='total_sales', title="Monthly Sales")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error retrieving monthly sales data: {e}")

        st.markdown("### Customer Segmentation")
        try:
            query = """
            WITH customer_orders AS (
                SELECT customer_id, COUNT(order_id) AS order_count
                FROM orders
                GROUP BY customer_id
            )
            SELECT customer_id, order_count,
                   CASE 
                     WHEN order_count >= 10 THEN 'High Frequency'
                     WHEN order_count >= 5 THEN 'Medium Frequency'
                     ELSE 'Low Frequency'
                   END AS segment
            FROM customer_orders
            ORDER BY order_count DESC;
            """
            df_seg = pd.read_sql_query(query, engine)
            df_grouped = df_seg.groupby("segment").size().reset_index(name="count")
            fig2 = px.pie(df_grouped, names='segment', values='count', title="Customer Segmentation")
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error retrieving customer segmentation data: {e}")

    elif selected_view == "SQL Runner":
        st.header("SQL Runner")
        st.markdown("Enter your SQL query below and click **Run SQL**.")
        sql_query = st.text_area("SQL Query", height=200)
        if st.button("Run SQL"):
            try:
                with engine.connect() as conn:
                    result = conn.execute(text(sql_query))
                    try:
                        df = pd.DataFrame(result.fetchall(), columns=result.keys())
                        st.dataframe(df)
                    except Exception as e:
                        st.write("Query executed successfully, but no tabular result to display.")
            except Exception as e:
                st.error(f"Error executing SQL query: {e}")
    
    st.markdown("---")
    st.write("Click the button below to exit the dashboard and return to the text-based menu.")
    if st.button("Exit Dashboard"):
        st.write("Exiting dashboard...")
        logger.info("Dashboard exit triggered by user.")
        time.sleep(1)
        os._exit(0)

##########################################
# TEXT-BASED MENU FUNCTIONS
##########################################
def run_text_menu():
    console = Console()
    while True:
        console.print(Panel.fit(Text("E-commerce Data Warehouse & Analytics Dashboard", style="bold magenta"), title="Main Menu", border_style="magenta"))
        console.print("Select an option:")
        console.print("1. Console Output (Explore Database)")
        console.print("2. Launch Interactive Dashboard (Streamlit)")
        console.print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            run_console_mode()
        elif choice == "2":
            console.print(Panel.fit(Text("Launching Streamlit Dashboard...", style="bold green"), title="Dashboard", border_style="green"))
            subprocess.run(["streamlit", "run", __file__], env={**os.environ, "STREAMLIT_MODE": "1"})
        elif choice == "3":
            console.print(Panel.fit(Text("Goodbye!", style="bold blue"), title="Exit", border_style="blue"))
            sys.exit(0)
        else:
            console.print(Panel.fit(Text("Invalid choice. Please try again.", style="bold red"), title="Error", border_style="red"))

##########################################
# TERMINAL MODE FUNCTIONS (Dummy Recommendations)
##########################################
def terminal_recommendation(console):
    console.print(Panel.fit(Text("Generating traditional recommendations...", style="bold blue"), title="Engine", border_style="blue"))
    connection_string = f"postgresql://{secret.DB_USER}:{secret.DB_PASS}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    engine = create_engine(connection_string)
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema="public")
    console.print("\nEnter a table name for recommendations (partial names accepted):")
    table_query = input("Table Name: ").strip()
    from thefuzz import process
    match, score = process.extractOne(table_query, tables)
    best_match = match if score >= 70 else None
    if best_match is None:
        console.print(Panel.fit("No close match found for your query. Please try again.", style="bold red", border_style="red"))
        return
    console.print(Panel.fit(f"Best match found: [bold green]{best_match}[/bold green]", border_style="green"))
    console.print(f"Recommendations for {best_match}:")
    console.print(" - Recommendation 1")
    console.print(" - Recommendation 2")
    console.print(" - Recommendation 3")

def terminal_advanced_recommendation(console):
    console.print(Panel.fit(Text("Generating advanced recommendations using NMF...", style="bold blue"), title="Advanced Engine", border_style="blue"))
    inspector, engine = get_pivot_advanced_global()
    tables = inspector.get_table_names(schema="public")
    console.print("\nEnter a table name for advanced recommendations (partial names accepted):")
    table_query = input("Table Name: ").strip()
    from thefuzz import process
    match, score = process.extractOne(table_query, tables)
    best_match = match if score >= 70 else None
    if best_match is None:
        console.print(Panel.fit("No close match found for your query. Please try again.", style="bold red", border_style="red"))
        return
    console.print(Panel.fit(f"Best match found: [bold green]{best_match}[/bold green]", border_style="green"))
    console.print(f"Advanced recommendations for {best_match}:")
    console.print(" - Advanced Recommendation 1")
    console.print(" - Advanced Recommendation 2")
    console.print(" - Advanced Recommendation 3")

##########################################
# MAIN EXECUTION
##########################################
if __name__ == "__main__":
    import subprocess
    if os.environ.get("STREAMLIT_MODE") == "1":
        run_streamlit_app()
    else:
        run_text_menu()
