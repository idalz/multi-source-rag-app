from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from app.utils.pinecone_utils import get_vectorstore
import os


def load_and_embed_files(file_paths: List[str]):
    """Load PDF or TXT files, add metadata, and insert into Pinecone vectorstore."""
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

        for doc in raw_docs:
            enriched_doc = Document(
                page_content=doc.page_content,
                metadata={
                    "source": "user_uploaded",
                    "file_name": file_name
                }
            )
            documents.append(enriched_doc)

    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents)
    return vectorstore
