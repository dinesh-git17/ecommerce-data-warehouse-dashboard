from sqlalchemy import create_engine, text
import secret  # Contains DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


def main():
    # Build connection string from secret.py
    connection_string = (
        f"postgresql://{secret.DB_USER}:{secret.DB_PASS}"
        f"@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    )
    engine = create_engine(connection_string)

    # SQL to create a standard view: customer_order_summary
    view_customer_order_summary = """
    CREATE OR REPLACE VIEW customer_order_summary AS
    SELECT 
      c.customer_id,
      c.name,
      COUNT(o.order_id) AS order_count,
      COALESCE(SUM(o.total_amount), 0) AS total_sales
    FROM 
      customers c
    LEFT JOIN 
      orders o ON c.customer_id = o.customer_id
    GROUP BY 
      c.customer_id, c.name;
    """

    # Updated SQL to create a materialized view: monthly_sales
    materialized_view_monthly_sales = """
    CREATE MATERIALIZED VIEW monthly_sales AS
    SELECT 
      DATE_TRUNC('month', order_date::timestamp) AS month,
      COUNT(order_id) AS orders_count,
      SUM(total_amount) AS total_sales
    FROM 
      orders
    GROUP BY 
      DATE_TRUNC('month', order_date::timestamp)
    ORDER BY 
      month;
    """

    # Connect to the database and execute the commands
    with engine.connect() as conn:
        try:
            conn.execute(text(view_customer_order_summary))
            print("Created view: customer_order_summary")
        except Exception as e:
            print("Error creating view customer_order_summary:", e)

        try:
            conn.execute(text(materialized_view_monthly_sales))
            print("Created materialized view: monthly_sales")
        except Exception as e:
            print("Error creating materialized view monthly_sales:", e)

        # Commit the changes
        conn.commit()


if __name__ == "__main__":
    main()
