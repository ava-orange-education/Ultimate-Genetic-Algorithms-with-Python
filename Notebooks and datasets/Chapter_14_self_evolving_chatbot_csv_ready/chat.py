import argparse
from agents.starter_agent import get_starter_agent
from agents.rag_model import RagModel
from agents.hybrid_agent import HybridAgent
from utils.logging_utils import log_performance
from scoring.evaluator import score_response
from load_and_retrieve import index, property_texts
from tools.arithmetic_tools import get_arithmetic_tools
from langchain.llms import OpenAI
import config

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["RAG", "AGENT", "HYBRID"], default="RAG")
args = parser.parse_args()
mode = args.mode.upper()

if mode == "RAG":
    rag_model = RagModel(index=index, property_texts=property_texts)
    print("Mode: RAG")

elif mode == "AGENT":
    agent = get_starter_agent(verbose=True)
    print("Mode: AGENT")

elif mode == "HYBRID":
    llm = OpenAI(temperature=0, openai_api_key=config.AZURE_OPENAI_API_KEY)
    tools = get_arithmetic_tools()
    hybrid_agent = HybridAgent(llm=llm, tools=tools, vector_store=index)
    print("Mode: HYBRID")

else:
    raise ValueError("Invalid mode")

while True:
    query = input("\nYou: ")
    if query.strip().lower() in ["exit", "quit"]:
        break

    if mode == "RAG":
        response = rag_model.answer(query)
    elif mode == "AGENT":
        response = agent.run(query)
    elif mode == "HYBRID":
        response = hybrid_agent.answer(query)
    else:
        response = "Invalid mode"

    score = score_response(query, response)
    log_performance(query, response, score, mode)
    print(f"Agent: {response} (Score: {score})")