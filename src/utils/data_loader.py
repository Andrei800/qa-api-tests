import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_csv(filename: str) -> list[dict]:
    """Загрузка CSV-файла как список словарей"""
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_json(filename: str) -> list[dict]:
    """Загрузка JSON-файла как список словарей"""
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        return data