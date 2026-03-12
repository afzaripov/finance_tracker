import json
import csv
from pathlib import Path

from transaction import Transaction


def export_to_json(filepath: str, data) -> None:
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def export_to_csv(transactions: list[Transaction], filepath: str) -> None:
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["date", "amount", "category", "description"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for transaction in transactions:
            writer.writerow(transaction.to_dict())


class ExportContext:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.extension = Path(filepath).suffix.lower()

    def __enter__(self):
        return self

    def write(self, data):
        if self.extension == ".json":
            export_to_json(self.filepath, data)

        elif self.extension == ".csv":
            export_to_csv(data, self.filepath)

        else:
            raise ValueError(f"Unsupported export format: {self.extension}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print(f"Экспорт завершён: {self.filepath}")
        else:
            print(f"Ошибка экспорта: {exc_val}")
        return False
