import re
import pandas as pd
from utils.database import get_db_connection


def extract_sql_from_response(llm_response):
    """Extract SQL from LLM response like a pro detective 🔍"""
    # Find SQL code blocks
    sql_pattern = r'```sql\n(.*?)\n```'
    matches = re.findall(sql_pattern, llm_response, re.DOTALL)

    if matches:
        return matches[0].strip()

    # Fallback: look for SELECT statements
    select_pattern = r'(SELECT.*?;)'
    matches = re.findall(select_pattern, llm_response, re.DOTALL | re.IGNORECASE)

    if matches:
        return matches[0].strip()

    return None


def execute_sql_safely(sql_query):
    """Execute SQL with safety nets (no database destruction allowed!) 🛡️"""

    if not sql_query:
        return None, "❌ No valid SQL query found in the response"

    # Security check - only allow SELECT
    if not sql_query.upper().strip().startswith('SELECT'):
        return None, "❌ Only SELECT queries allowed! No database destruction here!"

    # Add LIMIT if missing (prevent accidental data tsunamis)
    if 'LIMIT' not in sql_query.upper():
        sql_query = sql_query.rstrip(';') + ' LIMIT 100;'

    try:
        engine = get_db_connection()
        df = pd.read_sql(sql_query, engine)
        return df, f"✅ Query executed! Found {len(df)} records."
    except Exception as e:
        return None, f"💥 SQL Error: {str(e)}"