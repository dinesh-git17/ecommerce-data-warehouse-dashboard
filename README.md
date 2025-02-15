E-COMMERCE DATA WAREHOUSE & ANALYTICS DASHBOARD EXPLORER
========================================================

Overview:
---------
This project demonstrates an end-to-end data warehouse and analytics solution
using the Northwind sample database. It includes:

  - An ETL pipeline (etl_northwind.py) that extracts data from CSV files, cleans
    and transforms it, and loads it into a PostgreSQL database.
  - SQL scripts (create_views.py) to create standard and materialized views for
    advanced analytics.
  - A database exploration script (explore_db.py) offering a choice between
    console output (using Rich) and an interactive Streamlit dashboard.

Setup:
------
1. Virtual Environment:
   Create and activate a virtual environment:
     python3 -m venv env
     source env/bin/activate         (or on Windows: env\Scripts\activate)

2. Install Dependencies:
   Install the required packages:
     pip install -r requirements.txt

3. Configure Database Credentials:
   Create a file named secret.py with the following content (update with your actual credentials):

       DB_USER = "your_username"
       DB_PASS = "your_password"
       DB_HOST = "localhost"
       DB_PORT = "5432"
       DB_NAME = "north_explore"

   Be sure to add secret.py to your .gitignore to protect sensitive data.

4. Load Sample Data:
   Run the ETL pipeline to load Northwind data from CSV files:
     python3 etl_northwind.py

5. Create Views:
   Create the standard and materialized views by running:
     python3 create_views.py

Usage:
------
- To view database exploration in Console mode:
     python3 explore_db.py
  Then follow the on-screen menu options.

- To launch the Interactive Dashboard (Streamlit):
     STREAMLIT_MODE=1 streamlit run explore_db.py

Notes:
------
This project is designed to showcase advanced SQL skills and Python integration
for data warehousing and analytics. 

