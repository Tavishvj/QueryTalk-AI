#  QueryTalk: AI-Powered SQL Interface
**Democratizing data access through Natural Language Processing.**

##  Overview
QueryTalk is a Business Intelligence tool that allows non-technical users to query databases using plain English. It leverages **Gemini 1.5 Flash** and **LangChain** to translate questions into executable SQL, providing instant data insights.

##  Key Features
- **NL-to-SQL Translation:** Converts unstructured English questions into structured SQLite queries.
- **Automated Data Rendering:** Results are automatically formatted into Pandas dataframes or high-level metrics.
- **SQL Guardrails:** Implemented regex-based parsing to ensure clean SQL execution and prevent syntax errors.
- **Trust Layer:** An "AI Logic" expander shows the generated SQL for transparency and validation.

##  Tech Stack
- **LLM:** Google Gemini 1.5 Flash
- **Framework:** LangChain (SQLDatabaseChain)
- **Frontend:** Streamlit
- **Language:** Python
