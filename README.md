E-commerce Data Warehouse & Analytics Dashboard Explorer
===========================================================

Overview:
---------
This project demonstrates how to explore a PostgreSQL database using both a console (text-based)
interface and an interactive Streamlit dashboard. The project connects to a Northwind sample 
database (named "north_explore") via SQLAlchemy and displays schema details and sample data.

Key Features:
- Dual output modes: Console Output (using Rich for formatting) and an Interactive Streamlit Dashboard.
- Custom styling in Streamlit with injected CSS.
- Organized display of tables, columns, and sample data.
- Option to exit the Streamlit dashboard and return to the text-based menu.

Setup:
------
1. Create a virtual environment and activate it:
   python3 -m venv env
   source env/bin/activate   (or on Windows: env\Scripts\activate)

2. Install dependencies:
   pip install -r requirements.txt

3. Create a 'secret.py' file in the project directory with your database connection details:
   Example secret.py:
   
      DB_USER = "your_username"
      DB_PASS = "your_password"
      DB_HOST = "localhost"
      DB_PORT = "5432"
      DB_NAME = "north_explore"

   Make sure to add secret.py to your .gitignore.

Usage:
------
- To run the text-based menu:
    python explore_db.py

  The text menu will let you choose between:
    1. Console Output (explore the database using Rich formatting)
    2. Launch the Interactive Dashboard (Streamlit)
    3. Exit

- To launch the dashboard directly, run:
    STREAMLIT_MODE=1 streamlit run explore_db.py

The Streamlit dashboard displays the database tables in tabs with column details and sample data.
When you click "Exit Dashboard," the dashboard terminates and returns control to the text-based menu.

Notes:
------
- Ensure your PostgreSQL database is running and that the Northwind (north_explore) database is populated.
- Adjust the connection settings in secret.py as needed.
- For any issues or improvements, please refer to the project documentation or open an issue on GitHub.

Enjoy exploring your database!
