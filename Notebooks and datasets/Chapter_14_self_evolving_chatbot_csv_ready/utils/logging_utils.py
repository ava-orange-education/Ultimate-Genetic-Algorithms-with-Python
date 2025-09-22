import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/performance_log.json")

def log_performance(query: str, response: str, score: float, mode: str) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "mode": mode,
        "query": query,
        "response": response,
        "score": score
    }
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except json.JSONDecodeError:
            log_data = []
    else:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        log_data = []

    log_data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)