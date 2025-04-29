import pinecone
from app.config.settings import settings
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import OpenAIEmbeddings

def init_pinecone():
    """Initialize Pinecone with API key and environment."""
    pinecone.init(
        api_key=settings.PINECONE_API_KEY,
        environment=settings.PINECONE_ENVIRONMENT,
    )

def get_vectorstore():
    """Create or connect to an existing Pinecone vectorstore."""
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY
    )
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings
    )
    return vectorstore
