E-COMMERCE DATA WAREHOUSE & ANALYTICS DASHBOARD EXPLORER
========================================================

Overview:
---------
This project demonstrates an end-to-end solution for exploring and analyzing an e-commerce 
data warehouse built on a Northwind-like database. It includes the following components:

1. ETL Pipeline:
   - Script: etl_northwind.py
   - Extracts data from CSV files (e.g., customers.csv, products.csv, orders.csv, order_details.csv),
     transforms/cleans it, and loads it into a PostgreSQL database (e.g., north_explore).
   - Uses SQLAlchemy, Pandas, and psycopg2-binary.

2. SQL Views:
   - Script: create_views.py
   - Creates standard and materialized views (e.g., customer_order_summary and monthly_sales)
     to precompute analytics.

3. Database Exploration:
   - Script: explore_db.py
   - Provides a dual-mode interface:
     a) Console Output: Uses the Rich library to display table names, column details, and sample data.
     b) Interactive Dashboard: Uses Streamlit to provide an interactive UI with three tabs:
        - Tables: View table details with column descriptions and sample data.
        - Analytics: View advanced analytics (e.g., monthly sales chart and customer segmentation pie chart).
        - SQL Runner: Execute custom SQL queries and view results.
   - Includes a sidebar for easy navigation between views.
   - When the user clicks "Exit Dashboard," the dashboard terminates and returns to the text menu.

4. CSV Generation:
   - Script: generate_big_csv.py
   - Uses the Faker library to generate synthetic "big" CSV files for Customers, Products, Orders, 
     and Order Details. These files are stored in a data/ directory and can be loaded via the ETL pipeline.
   - Logging is integrated via a custom logger.

5. Logging:
   - File: mylogger.py
   - Provides colorful, emoji-enhanced logging using Colorlog.
   - Imported by various scripts for consistent logging output.

Setup:
------
1. Create a Virtual Environment:
   - In your project directory, run:
       python3 -m venv env
       On macOS/Linux: source env/bin/activate
       On Windows: env\Scripts\activate

2. Install Dependencies:
   - Run:
       pip install -r requirements.txt
   - The requirements.txt file includes:
       sqlalchemy
       pandas
       psycopg2-binary
       rich
       streamlit
       matplotlib
       seaborn
       plotly
       thefuzz
       Faker

3. Configure Database Credentials:
   - Create a file named secret.py in the project directory with your PostgreSQL credentials:
   
         DB_USER = "your_username"
         DB_PASS = "your_password"
         DB_HOST = "localhost"
         DB_PORT = "5432"
         DB_NAME = "north_explore"

   - Add secret.py to your .gitignore to keep your credentials secure.

4. Load Sample Data:
   - Place your CSV files (customers.csv, products.csv, orders.csv, order_details.csv) 
     in a folder named data.
   - Run the ETL pipeline:
         python3 etl_northwind.py

5. Create SQL Views:
   - Run:
         python3 create_views.py
   - This will create views such as customer_order_summary and materialized view monthly_sales.

Usage:
------
1. Console Mode:
   - To explore the database in console mode, run:
         python explore_db.py
   - A text-based menu will appear with options to view console output or launch the Streamlit dashboard.

2. Interactive Dashboard:
   - From the text menu, choose option 2 to launch the interactive Streamlit dashboard.
   - Alternatively, run directly:
         STREAMLIT_MODE=1 streamlit run explore_db.py
   - The dashboard has a sidebar to select between three tabs:
         Tables: View table details (with column descriptions and sample data).
         Analytics: View interactive charts for monthly sales and customer segmentation.
         SQL Runner: Run custom SQL queries and view results.
   - Click "Exit Dashboard" to return to the text menu.

3. CSV Generation:
   - To generate large synthetic CSV files for testing, run:
         python generate_big_csv.py
   - This will populate the data/ directory with sample CSV files.

Notes:
------
- This project showcases advanced SQL techniques (views, materialized views, window functions, CTEs)
  and Python integration for ETL and interactive analytics.
- The project is designed as a portfolio piece. Feel free to extend it with more advanced analytics,
  incremental loads, REST API endpoints, or containerization.
- For any issues, refer to the project documentation or open an issue on GitHub.

Enjoy exploring your data and enhancing your e-commerce data warehouse!

--------------------------------------------------------
