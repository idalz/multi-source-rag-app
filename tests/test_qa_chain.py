from app.chains.qa_chain import generate_answer
import app.chains.qa_chain as chain_module
from langchain_core.documents import Document
from langchain_core.documents import Document

# Tests LLM prompt execution
def test_generate_answer_basic():
    context = "Python is a programming language created by Guido van Rossum."
    question = "Who created Python?"

    answer = generate_answer(context, question)

    assert isinstance(answer, str)
    assert "Guido" in answer or "van Rossum" in answer


# Simulate FAISS failing to retrieve
class FakeVectorStore:
    def similarity_search(self, query, k=4):
        return []

class FakeRetriever:
    def invoke(self, question):
        return [Document(page_content="Fallback answer.", metadata={"source": "arxiv"})]

def test_retrieve_context_fallback(monkeypatch):
    # Monkeypatch inside the qa_chain module (where the functions are actually used)
    monkeypatch.setattr(chain_module, "get_arxiv_retriever", lambda: FakeRetriever())
    monkeypatch.setattr(chain_module, "get_wikipedia_retriever", lambda: FakeRetriever())

    question = "What is LangChain?"
    context, docs = chain_module.retrieve_context(question, vectorstore=FakeVectorStore())

    assert context is not None
    assert "Fallback answer." in context
    sources = [doc.metadata.get("source") for doc in docs]
    assert "arxiv" in sources or "wikipedia" in sources
