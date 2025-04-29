from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain import hub

from app.utils.data_loader import load_and_embed_files
from app.retrievers.arxiv_retriever import get_arxiv_retriever
from app.retrievers.wikipedia_retriever import get_wikipedia_retriever
from app.config.settings import settings


def create_agent_from_pdf(pdf_path: str) -> AgentExecutor:
    """Build an agent that can search a PDF, Arxiv, and Wikipedia using tools."""

    # 1. Load the PDF and embed it using your shared loader + Pinecone utils
    vectorstore = load_and_embed_files([pdf_path])
    retriever = vectorstore.as_retriever()

    # 2. Create a retriever tool for the PDF
    pdf_tool = create_retriever_tool(
        retriever=retriever,
        name="pdf_search",
        description="Search for information in the uploaded PDF document."
    )

    # 3. Add your custom Arxiv and Wikipedia retrievers
    arxiv_tool = create_retriever_tool(
        retriever=get_arxiv_retriever(),
        name="arxiv_search",
        description="Search for academic research and papers from Arxiv."
    )

    wiki_tool = create_retriever_tool(
        retriever=get_wikipedia_retriever(),
        name="wikipedia_search",
        description="Search for general knowledge and facts from Wikipedia."
    )

    tools = [pdf_tool, arxiv_tool, wiki_tool]

    # 4. Use standard agent prompt + LLM config
    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI(model=settings.OPENAI_MODEL, temperature=0.2)

    # 5. Create the agent
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    # 6. Return agent executor (with intermediate step logging enabled)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
