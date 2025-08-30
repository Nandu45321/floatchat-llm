import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql://neondb_owner:npg_qV9a3dQRAeBm@ep-still-field-a17hi4xm-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_db_connection():
    return create_engine(DATABASE_URL)

def test_connection():
    engine = get_db_connection()
    df = pd.read_sql("SELECT COUNT(*) as total_records FROM argo_floats LIMIT 1", engine)
    return df['total_records'].iloc[0]

# Test it works!
if __name__ == "__main__":
    print(f"🎉 Connected! We have {test_connection()} records in our ocean database!")