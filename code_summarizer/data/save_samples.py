import json
import os
from datetime import datetime

SAMPLES_FILE = os.path.join(os.path.dirname(__file__), "samples.json")


def save_sample(code: str, summary: str):
    """
    Saves a code + generated summary pair to samples.json.

    Args:
        code (str): The input Python code
        summary (str): The generated natural language summary
    """
    # Load existing samples
    if os.path.exists(SAMPLES_FILE):
        with open(SAMPLES_FILE, "r") as f:
            samples = json.load(f)
    else:
        samples = []

    # Append new sample
    samples.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "code": code,
        "summary": summary
    })

    # Save back to file
    with open(SAMPLES_FILE, "w") as f:
        json.dump(samples, f, indent=2)


def load_samples() -> list:
    """
    Loads all saved samples from samples.json.

    Returns:
        list: List of saved code+summary pairs
    """
    if not os.path.exists(SAMPLES_FILE):
        return []

    with open(SAMPLES_FILE, "r") as f:
        return json.load(f)
