from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
import os

def load_and_embed_files(file_paths: List[str]):
    """Load PDF or TXT files, add metadata, and create a FAISS vectorstore."""
    documents = []

    for path in file_paths:
        file_name = os.path.basename(path)
        
        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif path.endswith(".txt"):
            loader = TextLoader(path)
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT are allowed.")
        
        raw_docs = loader.load()

        # Add metadata manually to each loaded document
        for doc in raw_docs:
            enriched_doc = Document(
                page_content=doc.page_content,
                metadata={
                    "source": "user_uploaded",
                    "file_name": file_name
                }
            )
            documents.append(enriched_doc)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embedding=embeddings)

    return vectorstore
