import asyncio
from dotenv import load_dotenv
import bs4
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import OpenAIEmbeddings

load_dotenv()
memory = MemorySaver()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

# See docker command above to launch a postgres instance with pgvector enabled.
connection = "postgresql+psycopg://postgres:postgres@localhost:5432/rag_pg_vector"  # Uses psycopg3!
collection_name = "my_docs"


vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)


retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})

tool = create_retriever_tool(
    retriever,
    "Distribution_regulations",
    "Выполняет поиск и возвращает отрывки из документа о порядке распределения и перераспределения.",
)
tools = [tool]


agent_executor = create_react_agent(llm, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc12"}}


query = "что нужно чтобы оформить перераспределение?"

for event in agent_executor.stream(
    {"messages": [HumanMessage(content=query)]},
    config=config,
    stream_mode="values",
):
    event["messages"][-1].pretty_print()
