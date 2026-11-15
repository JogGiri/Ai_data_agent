import psycopg
import pandas as pd
from sqlalchemy import create_engine
from langchain.tools import tool


# Using a single URI connection string:
# DATABASE_URL = "postgresql://joggiri@localhost:5432/postgres"
#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE


engine = create_engine(
"postgresql+psycopg://joggiri@localhost:5432/postgres"
)

def _run_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        return df.to_string(index=False)

@tool
def execute_query(query):
    '''
    Use this tool to execute any SQL query on the database
    '''
    return _run_query(query)

@tool
def get_schema():
    '''
    Use this tool to get schema of table
    '''
    query = """
        select
        cols.table_name,
        cols.column_name,
        cols.data_type
        from information_schema.columns cols
        where cols.table_schema = 'public'
        order by cols.table_name,cols.ordinal_position;
        """
    return _run_query(query)