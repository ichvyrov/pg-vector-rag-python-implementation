import asyncio
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# See docker command above to launch a postgres instance with pgvector enabled.
connection = "postgresql+psycopg://postgres:postgres@localhost:5432/rag_pg_vector"  # Uses psycopg3!
collection_name = "my_docs"


vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

file_path = (
    "rasp.pdf"
)

async def get_pages():
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

result = asyncio.run(get_pages())

vector_store.add_documents(result, ids=[doc.metadata["page"] for doc in result])

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})
