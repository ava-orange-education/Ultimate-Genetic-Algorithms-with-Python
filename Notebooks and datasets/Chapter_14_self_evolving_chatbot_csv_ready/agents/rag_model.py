from load_and_retrieve import retrieve_top_k, generate_answer

class RagModel:
    def __init__(self, index, property_texts, top_k=3):
        self.index = index
        self.property_texts = property_texts
        self.top_k = top_k

    def answer(self, query: str) -> str:
        top_docs = retrieve_top_k(query, self.index, self.property_texts, k=self.top_k)
        return generate_answer(query, top_docs)