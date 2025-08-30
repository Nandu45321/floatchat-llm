import streamlit as st
import plotly.express as px
import pandas as pd
from utils.llm_handler import ask_ocean_gpt
from utils.sql_extractor import extract_sql_from_response, execute_sql_safely
from utils.database import test_connection

# 🎨 Page config
st.set_page_config(
    page_title="🌊 FloatChat - Ocean Data Explorer",
    page_icon="🌊",
    layout="wide"
)

# 🎭 Header with style
st.title("🌊 FloatChat - Your Ocean Data Whisperer")
st.markdown("*Ask me anything about ARGO float data in the Indian Ocean!* 🚢")

# 🔌 Connection test
with st.sidebar:
    st.header("🔌 System Status")
    try:
        record_count = test_connection()
        st.success(f"✅ Connected! {record_count:,} records ready")
        st.info("🌊 85 ARGO floats active\n📍 Indian Ocean region\n📅 2024 data")
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")

# 💬 Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "🌊 Hello! I'm your ocean data assistant. Ask me about ARGO float temperatures, salinity, locations, or anything else! Try: 'Show me the warmest surface waters' or 'Find floats near the equator'"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 🎯 User input
if prompt := st.chat_input("Ask about ocean data..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # 🤖 Process with LLM
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking about ocean data..."):

            # Get LLM response
            llm_response = ask_ocean_gpt(prompt)

            # Extract and execute SQL
            sql_query = extract_sql_from_response(llm_response)

            if sql_query:
                st.code(sql_query, language="sql")

                # Execute query
                df, status = execute_sql_safely(sql_query)
                st.info(status)

                if df is not None and not df.empty:
                    # 📊 Show results
                    st.subheader("📊 Query Results")
                    st.dataframe(df.head(20))

                    # 🗺️ BASIC Map
                    if 'latitude' in df.columns and 'longitude' in df.columns:
                        st.subheader("🗺️ Float Locations")
                        map_df = df.dropna(subset=['latitude', 'longitude'])
                        if not map_df.empty:
                            st.map(map_df[['latitude', 'longitude']])

                    # 📈 BASIC Charts
                    if 'temperature' in df.columns:
                        fig = px.histogram(df, x='temperature', title="🌡️ Temperature Distribution")
                        st.plotly_chart(fig, use_container_width=True)

                    if 'salinity' in df.columns:
                        fig = px.histogram(df, x='salinity', title="🧂 Salinity Distribution")
                        st.plotly_chart(fig, use_container_width=True)

                    # 📥 Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Results as CSV",
                        data=csv,
                        file_name=f"argo_data_results.csv",
                        mime="text/csv"
                    )

            # Show LLM response
            st.write(llm_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": llm_response})

# 🎪 Sidebar with example queries
with st.sidebar:
    st.header("💡 Try These Questions!")

    example_questions = [
        "Show me all floats with surface temperature above 30°C",
        "Find the saltiest water measurements",
        "Which floats are active near the equator?",
        "Compare temperature vs salinity",
        "Show me data from float 4903660",
        "What's the deepest measurement we have?"
    ]

    for question in example_questions:
        if st.button(f"💬 {question}", key=question):
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()

# 🏃‍♀️ Footer
st.markdown("---")
st.markdown("🏃‍♀️ *Built in 4 hours for the FloatChat challenge! Next teammate takes over at 2 PM.*")