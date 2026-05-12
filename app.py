import streamlit as st
import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from utils import is_safe_sql
from sqlalchemy import create_engine
import re


st.set_page_config(page_title="QueryTalk AI", layout="wide")
st.title("QueryTalk: AI Data Assistant")


STABLE_MODEL = "gemini-3.1-flash-lite" 
MY_KEY = "AIzaSyCHkmmcO16tg4kJaDUbfytG2yxD6tsT-H0"
db_path = "Chinook_Sqlite.sqlite"

if not os.path.exists(db_path):
    st.error(f"Database file '{db_path}' not found!")
    st.stop()

try:
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    engine = create_engine(f"sqlite:///{db_path}")

    llm = ChatGoogleGenerativeAI(
        model=STABLE_MODEL, 
        google_api_key=MY_KEY,
        temperature=0
    )

    db_chain = SQLDatabaseChain.from_llm(
        llm, 
        db, 
        verbose=True, 
        return_intermediate_steps=True
    )
    
    st.sidebar.success(f"AI Engine Connected")

except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

question = st.text_input("Ask a question about your database:", placeholder="e.g., How many tracks are in the database?")

if question:
    with st.spinner("AI is querying the database..."):
        raw_sql = "No SQL generated yet" 
        
        try:
            result = db_chain(question)
            
            
            steps = result.get("intermediate_steps", [])
            for step in steps:
                if isinstance(step, str) and "SELECT" in step.upper():
                    raw_sql = step
                    break
            
            clean_sql = re.sub(r'^(SQLQuery:|Answer:|SQL:|SQL Query:)', '', raw_sql, flags=re.IGNORECASE).strip()
            clean_sql = clean_sql.replace('```sql', '').replace('```', '').strip()
            clean_sql = clean_sql.split(';')[0] + ';' 
            
            st.markdown("## Summary")
            st.info(result["result"])
            
            df = pd.read_sql_query(clean_sql, engine)
            
            st.markdown("### Data Result")
            if not df.empty:
            
                if df.shape == (1, 1):
                    val = df.iloc[0, 0]
                    st.metric(label="Total Result", value=val)
                else:
                
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("Query executed but returned no data rows.")

            with st.expander(" View SQL Logic"):
                st.code(clean_sql, language="sql")

        except Exception as e:
            st.error("I hit a snag while running the query.")
            with st.expander("Technical Traceback"):
                st.write(f"Model Used: {STABLE_MODEL}")
                st.write(f"Raw Output from AI: {raw_sql}")
                st.write(f"Error Details: {e}")