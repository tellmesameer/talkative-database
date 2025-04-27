from langchain_community.utilities import SQLDatabase
from langchain import hub
from typing import TypedDict
import os
from typing_extensions import Annotated
from langgraph.graph import START, StateGraph
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from query_engine.model import init_llm
from langchain.prompts import PromptTemplate
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from data_sources.db_connections import get_database_configs
from PIL import Image
llm = init_llm()

prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

# Connect to the SQLite database
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    db: SQLDatabase
    db_info: str

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def choose_db(state: State) -> str:
    """
    Choose the database to query.
    """
    # Here you can implement logic to choose the database based on the question
    # For now, we are just returning the current database

    db_configs = get_database_configs()

    prompt_template = PromptTemplate.from_template(
        """"
        You are a database router. Choose the most appropriate database to answer the user's question.

        Databases:
        {db_descriptions}

        Question: {question}

        Return the name of the most suitable database only (e.g., bigquery, sqlite, redshift).
        """
    )

    prompt = prompt_template.invoke(
        {"db_descriptions": db_configs, "question": state["question"]}
    )

    answer = llm.invoke(prompt)

    chosen_db = db_configs[answer.content]

    return {"db": chosen_db["db"], "db_info": chosen_db["table_info"]}

def write_query(state: State) -> str:

    prompt = prompt_template.invoke(
        {
            "dialect": state["db"].dialect,
            "top_k": 5,
            "table_info": state["db_info"],
            "input": state["question"],
        }
    )
    result = llm.with_structured_output(QueryOutput).invoke(prompt)

    return {"query": result["query"]}

def execute_query(state: State):
    execute_query_tool = QuerySQLDatabaseTool(db=state["db"])
    return {"result": execute_query_tool.invoke(state["query"])}

def generate_answer(state: State):
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)

    return {"answer": response.content}


def answer_question(question: str) -> str:
    """
    Given a question, return the answer.
    """
    graph_builder = StateGraph(State).add_sequence(
        [choose_db,write_query, execute_query, generate_answer]
    )
    graph_builder.add_edge(START, "choose_db")
    graph = graph_builder.compile()

    return graph.stream({"question": question})

