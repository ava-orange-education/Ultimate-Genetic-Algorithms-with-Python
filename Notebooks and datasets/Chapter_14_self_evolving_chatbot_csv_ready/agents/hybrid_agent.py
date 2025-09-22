from langchain.agents import AgentType, initialize_agent
from langchain.vectorstores import FAISS

class HybridAgent:
    def __init__(self, llm, tools, vector_store: FAISS, top_k: int = 3):
        self.vector_store = vector_store
        self.top_k = top_k
        self.agent = initialize_agent(
            tools, llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=False
        )

    def answer(self, query: str) -> str:
        docs = self.vector_store.similarity_search(query, k=self.top_k)
        context = "\n".join([doc.page_content for doc in docs]) if docs else ""
        augmented_query = f"Context:\n{context}\n\nQuestion: {query}" if context else query
        return self.agent.run(augmented_query)