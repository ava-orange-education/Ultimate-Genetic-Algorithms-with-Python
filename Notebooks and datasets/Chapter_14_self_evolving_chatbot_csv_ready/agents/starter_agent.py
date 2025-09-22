from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from tools.arithmetic_tools import get_arithmetic_tools
import config

def get_starter_agent(verbose=True):
    llm = OpenAI(temperature=0, openai_api_key=config.AZURE_OPENAI_API_KEY)
    tools = get_arithmetic_tools()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose
    )
    return agent