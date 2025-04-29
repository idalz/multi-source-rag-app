from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from app.config.settings import settings

def get_arxiv_retriever():
    """Returns retriever for Arxiv documents stored in Pinecone."""
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY
    )
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,  
        embedding=embeddings,
        namespace="arxiv"  
    )
    retriever = vectorstore.as_retriever()
    return retriever
