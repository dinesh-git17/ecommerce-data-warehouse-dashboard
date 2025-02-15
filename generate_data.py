import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import os
from mylogger import logger  # Make sure mylogger.py is in your project directory

fake = Faker()

# Ensure the data directory exists
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    logger.info("Created 'data' directory.")

# ---------------------
# Generate customers.csv
# ---------------------
num_customers = 1000  # Adjust as needed
customers_file = os.path.join(data_dir, "customers.csv")
try:
    with open(customers_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["customer_id", "name", "email", "registration_date"])
        for i in range(1, num_customers + 1):
            registration_date = fake.date_between(start_date="-5y", end_date="today")
            writer.writerow([i, fake.name(), fake.email(), registration_date])
    logger.info(f"Generated {num_customers} rows in {customers_file}")
except Exception as e:
    logger.error(f"Error generating {customers_file}: {e}")

# ---------------------
# Generate products.csv
# ---------------------
num_products = 200  # Adjust as needed
products_file = os.path.join(data_dir, "products.csv")
try:
    with open(products_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["product_id", "name", "category", "price", "stock_quantity"])
        categories = ["Widgets", "Gadgets", "Doohickeys", "Accessories"]
        for i in range(1, num_products + 1):
            product_name = fake.word().capitalize() + " " + fake.word().capitalize()
            category = random.choice(categories)
            price = round(random.uniform(5.0, 100.0), 2)
            stock_quantity = random.randint(50, 500)
            writer.writerow([i, product_name, category, price, stock_quantity])
    logger.info(f"Generated {num_products} rows in {products_file}")
except Exception as e:
    logger.error(f"Error generating {products_file}: {e}")

# ---------------------
# Generate orders.csv
# ---------------------
num_orders = 5000  # Adjust as needed
orders_file = os.path.join(data_dir, "orders.csv")
try:
    with open(orders_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["order_id", "customer_id", "order_date", "total_amount"])
        start_date = datetime.now() - timedelta(days=365 * 3)
        for i in range(1, num_orders + 1):
            order_date = fake.date_between(start_date=start_date, end_date="today")
            customer_id = random.randint(1, num_customers)
            total_amount = round(random.uniform(20, 500), 2)
            writer.writerow([i, customer_id, order_date, total_amount])
    logger.info(f"Generated {num_orders} rows in {orders_file}")
except Exception as e:
    logger.error(f"Error generating {orders_file}: {e}")

# ---------------------
# Generate order_details.csv
# ---------------------
num_order_details = 10000  # Adjust as needed
order_details_file = os.path.join(data_dir, "order_details.csv")
try:
    with open(order_details_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["order_item_id", "order_id", "product_id", "quantity", "price_at_order"]
        )
        for i in range(1, num_order_details + 1):
            order_id = random.randint(1, num_orders)
            product_id = random.randint(1, num_products)
            quantity = random.randint(1, 10)
            price_at_order = round(random.uniform(5, 100), 2)
            writer.writerow([i, order_id, product_id, quantity, price_at_order])
    logger.info(f"Generated {num_order_details} rows in {order_details_file}")
except Exception as e:
    logger.error(f"Error generating {order_details_file}: {e}")

logger.info("CSV generation process completed successfully.")
