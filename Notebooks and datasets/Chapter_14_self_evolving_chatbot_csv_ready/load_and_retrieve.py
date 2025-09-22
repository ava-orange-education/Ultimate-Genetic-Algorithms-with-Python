import numpy as np
import faiss
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
import config

# === Configuration ===
STATE_NAME = "Wisconsin"  # <-- Change this to match your state
CSV_PATH = f"state_data/{STATE_NAME}.csv"
EMBEDDING_PATH = f"state_data/{STATE_NAME}_embeddings.npy"

# Load embeddings from .npy file
embeddings = np.load(EMBEDDING_PATH).astype("float32")

# Load property descriptions from CSV column
df = pd.read_csv(CSV_PATH)
if 'description' not in df.columns:
    raise ValueError("CSV does not contain 'description' column.")
property_texts = df['description'].fillna("No description available").tolist()

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === Functions ===
def retrieve_top_k(query: str, faiss_index, texts, k=3):
    embed_model = OpenAIEmbeddings(
        openai_api_key=config.AZURE_OPENAI_API_KEY,
        openai_api_base=config.AZURE_OPENAI_API_BASE,
        openai_api_version=config.AZURE_OPENAI_API_VERSION,
        deployment=config.AZURE_OPENAI_DEPLOYMENT
    )
    query_vec = embed_model.embed_query(query)
    D, I = faiss_index.search(np.array([query_vec], dtype="float32"), k)
    return [texts[i] for i in I[0]]

def generate_answer(query: str, context_docs: list):
    from langchain.chat_models import AzureChatOpenAI

    llm = AzureChatOpenAI(
        openai_api_key=config.AZURE_OPENAI_API_KEY,
        openai_api_base=config.AZURE_OPENAI_API_BASE,
        openai_api_version=config.AZURE_OPENAI_API_VERSION,
        deployment_name=config.AZURE_OPENAI_DEPLOYMENT
    )

    context = "\n".join(context_docs) if context_docs else "No relevant context found."
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    response = llm.predict(prompt)
    return response