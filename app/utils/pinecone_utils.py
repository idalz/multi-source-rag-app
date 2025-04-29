from app.config.settings import settings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

def get_vectorstore():
    """Create or connect to a Pinecone vectorstore (modern way)."""
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY
    )
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings
    )
    return vectorstore
