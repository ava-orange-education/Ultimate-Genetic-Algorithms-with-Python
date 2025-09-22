from math import sqrt
from langchain.agents import Tool, load_tools
from langchain.llms import OpenAI
import config

def add_numbers(input: str) -> str:
    try:
        parts = input.replace(',', ' ').split()
        nums = [float(x) for x in parts if x.replace('.', '', 1).lstrip('-').isdigit()]
        if len(nums) < 2:
            return "Error: provide two numbers."
        return str(nums[0] + nums[1])
    except Exception as e:
        return f"Error: {e}"

def calculate_distance(input: str) -> str:
    try:
        parts = input.replace(',', ' ').split()
        nums = [float(x) for x in parts if x.replace('.', '', 1).lstrip('-').isdigit()]
        if len(nums) < 4:
            return "Error: provide four numbers (x1 y1 x2 y2)."
        x1, y1, x2, y2 = nums[:4]
        dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return str(dist)
    except Exception as e:
        return f"Error: {e}"

def get_arithmetic_tools():
    llm = OpenAI(temperature=0, openai_api_key=config.AZURE_OPENAI_API_KEY)
    addition_tool = Tool(
        name="addition",
        func=add_numbers,
        description="Add two numbers. Input: 'a b' or 'a, b'."
    )
    distance_tool = Tool(
        name="distance",
        func=calculate_distance,
        description="Compute the Euclidean distance between two points. Input: 'x1 y1 x2 y2'."
    )
    built_in_tools = load_tools(["llm-math"], llm=llm)
    return [addition_tool, distance_tool] + built_in_tools