import streamlit as st
from query_engine.sql_query_graph import answer_question  # Custom graph you built

# --- Custom CSS ---

st.title("📊 SQL Assistant")

# Sidebar: Data source context
st.sidebar.title("🗂️ Data Sources")

st.sidebar.markdown("""
**Connected Databases:**

- `sample_data_dev.tickit`  
  Ticketing platform data — events, users, venues, listings, and sales  

- `sqlite` (Northwind)  
  Classic retail dataset — customers, orders, products, employees  

- `bigquery-public-data.samples`  
  Public Google BigQuery samples — includes `natality`, `github_nested`, `weather_stations`, etc.

💡 *Try asking:*  
- "List all customers from Germany."  
- "List all the schemas in MS SQL database."                      
- "Which event had the most ticket sales?"  
- "What’s the average birth weight in the natality dataset?"
""")


# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Each item is a dict: {"question", "sql", "answer"}

# --- Chat UI rendering (top to bottom) ---
for item in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(f"**🧠 Question:** {item['question']}")
    with st.chat_message("assistant"):
        st.markdown(f"**🛠️ SQL Query:**\n```sql\n{item['sql']}\n```")
        st.markdown(f"**🤖 Answer:** {item['answer']}")

# --- User input at the bottom ---
user_question = st.chat_input("Ask your data question:")

# --- Run graph and update memory ---
if user_question:
    with st.spinner("Thinking..."):

        result = {}
        for update in answer_question(user_question):  # your streaming graph
            result.update(update)

        sql_query = result.get("write_query", {}).get("query", "No SQL query generated.")
        answer = result.get("generate_answer", {}).get("answer", "No answer available.")

        # Save to memory
        st.session_state.chat_history.append({
            "question": user_question,
            "sql": sql_query,
            "answer": answer
        })
       # st.experimental_rerun()
    for item in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(f"**🧠 Question:** {item['question']}")
        with st.chat_message("assistant"):
            st.markdown(f"**🛠️ SQL Query:**\n```sql\n{item['sql']}\n```")
            st.markdown(f"**🤖 Answer:** {item['answer']}")