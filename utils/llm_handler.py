from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

SYSTEM_PROMPT = """
🌊 You are OceanGPT, an expert oceanographer's AI assistant! 

Your job: Convert human questions about ARGO float data into perfect SQL queries.

DATABASE SCHEMA:
- Table: argo_floats
- Columns: platform_number, cycle_number, measurement_time, latitude, longitude, pressure, temperature, salinity, data_quality

AVAILABLE FLOATS: 85 different floats in Indian Ocean
SAMPLE DATA: Temperature range 29-31°C, Salinity 33-37 psu, Pressure 0-100+ dbar

RULES:
1. Always return SQL in ```sql code blocks
2. Add LIMIT 100 to prevent database explosions 💥
3. Be creative with queries but stay within the schema
4. If question is vague, ask for clarification like a polite ocean scientist

EXAMPLE QUERIES:
- "Show warm waters" → SELECT * FROM argo_floats WHERE temperature > 29 LIMIT 100;
- "Arabian Sea floats" → SELECT * FROM argo_floats WHERE latitude BETWEEN 10 AND 25 AND longitude BETWEEN 50 AND 80 LIMIT 100;
"""

def ask_ocean_gpt(question):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error connecting to Groq API: {str(e)}\n\nPlease check your GROQ_API_KEY in the .env file"