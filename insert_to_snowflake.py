import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import json

# Load Snowflake credentials from external file
with open('snowflake_credentials.json') as f:
    snowflake_creds = json.load(f)
snowflake_user = snowflake_creds['user']
snowflake_password = snowflake_creds['password']
snowflake_account = snowflake_creds['account']
snowflake_warehouse = snowflake_creds['warehouse']
snowflake_database = snowflake_creds['database']
snowflake_schema = snowflake_creds['schema']
snowflake_role = snowflake_creds.get('role', None)

# Read CSV data into DataFrame
csv_file_path = './docker/source-data/sales_data.csv'
df = pd.read_csv(csv_file_path)

# ...existing code...
df = pd.read_csv(csv_file_path)
df.columns = [col.upper().replace(' ', '_') for col in df.columns]

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema,
    role=snowflake_role
)

# Create table if not exists (adjust types as needed)
create_table_sql = """
CREATE TABLE IF NOT EXISTS SALES_DATA (
    ROW_ID INTEGER,
    ORDER_ID STRING,
    ORDER_DATE DATE,
    SHIP_DATE DATE,
    SHIP_MODE STRING,
    CUSTOMER_ID STRING,
    CUSTOMER_NAME STRING,
    SEGMENT STRING,
    COUNTRY STRING,
    CITY STRING,
    STATE STRING,
    POSTAL_CODE STRING,
    REGION STRING,
    PRODUCT_ID STRING,
    CATEGORY STRING,
    SUB_CATEGORY STRING,
    PRODUCT_NAME STRING,
    SALES FLOAT,
    QUANTITY INTEGER,
    DISCOUNT FLOAT,
    PROFIT FLOAT
)
"""
cur = conn.cursor()
cur.execute(create_table_sql)

# Insert data using write_pandas
success, nchunks, nrows, _ = write_pandas(conn, df, 'SALES_DATA', auto_create_table=False)
print(f'Success: {success}, Chunks: {nchunks}, Rows: {nrows}')

cur.close()
conn.close()