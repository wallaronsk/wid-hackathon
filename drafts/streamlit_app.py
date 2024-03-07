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

# create a streamlit selectbox to select a table
tableName = st.selectbox('Select a table', tableNames)

# get the first 100 rows of the selected table
cursor.execute(f"SELECT * FROM {tableName}")

# create pandas dataframe from the results
import pandas as pd
df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

# display the dataframe
st.write(df)

# get rows where 'HASHTAGS' column contains the word 'metoo' or 'MeToo
cursor.execute(f"SELECT * FROM {tableName} WHERE HASHTAGS LIKE '%metoo%' OR HASHTAGS LIKE '%MeToo%'")

# create pandas dataframe from the results
df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

# save the data as a csv in data/
df.to_csv('data/metooIn{}.csv'.format(tableName), index=False)

# create selectbox to select two columns from the dataframe
column1 = st.selectbox('Select a column', df.columns)
column2 = st.selectbox('Select another column', df.columns)


# display the dataframe
st.write(df)

# fetch the results
rows = cursor.fetchall()
