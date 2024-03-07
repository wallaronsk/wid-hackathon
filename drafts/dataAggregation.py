import streamlit as st

import snowflake.connector

# Set up the connection parameters
account = 'aa34152.eu-west-2'
user = 'ROBERT'
password = ''
warehouse = 'WID_COMPUTE_WH'
database = 'WID_HACKATHON_PRIVATE_DATASETS'
schema = 'BRIGHT_DATA_DATASETS'

# Create a connection object
conn = snowflake.connector.connect(
    account=account,
    user=user,
    password=password,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# get all table names in bright_data_datasets
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
tableNames = [table[1] for table in tables]
print(tableNames)