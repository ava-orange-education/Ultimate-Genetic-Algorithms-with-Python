import re

def score_response(query: str, response: str) -> float:
    try:
        expr = re.sub(r'[^0-9+\-*/(). ]', '', query)
        if expr.strip():
            expected = eval(expr)
            expected_val = float(expected)
            answer_val = float(response)
            return 1.0 if abs(expected_val - answer_val) < 1e-6 else 0.0
        return 0.0
    except Exception:
        return 0.0