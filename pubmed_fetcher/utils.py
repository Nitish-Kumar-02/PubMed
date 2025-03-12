import csv
from typing import List, Dict, Any

def save_to_csv(papers: List[Dict[str, Any]], filename: str):
    """Save the paper details to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
    print(f"Saved results to {filename}")
