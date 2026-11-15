import psycopg
import pandas as pd
from sqlalchemy import create_engine


# Using a single URI connection string:
# DATABASE_URL = "postgresql://joggiri@localhost:5432/postgres"
#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE

engine = create_engine(
"postgresql+psycopg://joggiri@localhost:5432/postgres"
)

def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        return df

# print(execute_query("SELECT count(*) as total_records FROM public.returns"))