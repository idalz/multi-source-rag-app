from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from app.retrievers.arxiv_retriever import get_arxiv_retriever
from app.retrievers.wikipedia_retriever import get_wikipedia_retriever
from app.config.settings import settings

# Initialize LLM
llm = ChatOpenAI(model=settings.OPENAI_MODEL, temperature=0)

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Use the following context to answer the question.
If you don't know, just say you don't know. Don't make up an answer.

Context:
{context}

Question:
{question}
""")

output_parser = StrOutputParser()

def retrieve_context(question: str, vectorstore) -> tuple[Optional[str], List[Document]]:
    """Search in user files, then Arxiv, then Wikipedia."""
    # 1. User files (FAISS)
    docs = vectorstore.similarity_search(question, k=4)
    if docs:
        return "\n\n".join(doc.page_content for doc in docs), docs

    # 2. Arxiv
    arxiv_docs = get_arxiv_retriever().get_relevant_documents(question)
    if arxiv_docs:
        return "\n\n".join(doc.page_content for doc in arxiv_docs), arxiv_docs

    # 3. Wikipedia
    wiki_docs = get_wikipedia_retriever().get_relevant_documents(question)
    if wiki_docs:
        return "\n\n".join(doc.page_content for doc in wiki_docs), wiki_docs

    return None, []

def generate_answer(context: str, question: str) -> str:
    """Run LLM on given context + question."""
    chain = prompt | llm | output_parser
    return chain.invoke({"context": context, "question": question})

def qa_answer(question: str, vectorstore) -> dict:
    """Full RAG process: retrieve, generate, return with sources."""
    context, docs = retrieve_context(question, vectorstore)

    if context is None:
        return {
            "answer": "I’m sorry, I couldn’t find any relevant information in your files, Arxiv, or Wikipedia.",
            "sources": []
        }

    answer = generate_answer(context, question)
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    return {
        "answer": answer,
        "sources": sources,
    }

def build_qa_chain(vectorstore):
    """Wraps qa_answer() to make it callable in UI layer."""
    return lambda question: qa_answer(question, vectorstore)
