from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
import json
import os
from typing import List

# Initialize MCP server
mcp = FastMCP("SEMAS Tool Discovery Server")

# Predefined starter tools
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@mcp.tool()
def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two 2D coordinates."""
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

# Load low score queries from logs and try to discover patterns for new tools
DISCOVERY_LOG = "logs/performance_log.json"
NEW_TOOLS_FILE = "tools/auto_discovered_tools.py"

@mcp.tool()
def analyze_low_score_queries(threshold: float = 0.4, max_tools: int = 5) -> List[str]:
    """
    Analyze low-score queries from logs and suggest possible new tool ideas.
    This function is an intermediate step before auto-generating tool code.
    """
    if not os.path.exists(DISCOVERY_LOG):
        return ["No log file found"]

    with open(DISCOVERY_LOG, "r") as f:
        logs = json.load(f)

    suggestions = []
    for entry in logs:
        if entry["score"] < threshold:
            query = entry["query"].lower()
            if "bmi" in query:
                suggestions.append("Add BMI Calculator Tool")
            elif "area" in query:
                suggestions.append("Add Area Calculator Tool")
            elif "difference" in query or "subtract" in query:
                suggestions.append("Add Subtraction Tool")
            elif "average" in query:
                suggestions.append("Add Average Calculator Tool")
            elif "convert" in query:
                suggestions.append("Add Unit Converter Tool")

    return list(set(suggestions))[:max_tools]

@mcp.tool()
def generate_new_tools(suggestions: List[str]) -> str:
    """
    Generate new tool function code snippets based on suggestions and save to tool file.
    """
    generated = ""
    with open(NEW_TOOLS_FILE, "a") as f:
        for idea in suggestions:
            if "BMI" in idea:
                code = "@mcp.tool()\ndef calculate_bmi(weight_kg: float, height_m: float) -> float:\n    \"\"\"Calculate Body Mass Index (BMI).\"\"\"\n    return weight_kg / (height_m ** 2)\n"
            elif "Subtraction" in idea:
                code = "@mcp.tool()\ndef subtract(a: float, b: float) -> float:\n    \"\"\"Subtract b from a.\"\"\"\n    return a - b\n"
            elif "Average" in idea:
                code = "@mcp.tool()\ndef average(values: list[float]) -> float:\n    \"\"\"Calculate average of a list of numbers.\"\"\"\n    return sum(values) / len(values)\n"
            elif "Area" in idea:
                code = "@mcp.tool()\ndef area_rectangle(length: float, width: float) -> float:\n    \"\"\"Calculate area of a rectangle.\"\"\"\n    return length * width\n"
            elif "Unit Converter" in idea:
                code = "@mcp.tool()\ndef convert_km_to_miles(km: float) -> float:\n    \"\"\"Convert kilometers to miles.\"\"\"\n    return km * 0.621371\n"
            else:
                continue

            f.write(code + "\n\n")
            generated += f"Tool generated: {idea}\n"

    return generated or "No tool was generated."

if __name__ == "__main__":
    mcp.run()