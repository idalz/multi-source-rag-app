from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from app.config.settings import settings

def get_wikipedia_retriever():
    """Returns retriever for Wikipedia documents stored in Pinecone."""
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY
    )
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace="wikipedia"  
    )
    retriever = vectorstore.as_retriever()
    return retriever
