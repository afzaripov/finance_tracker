import json
import csv
import pytest

from exporter import export_to_json, export_to_csv, ExportContext
from transaction import Transaction


def test_export_to_json(tmp_path):
    filepath = tmp_path / "data.json"

    data = {"name": "Александр", "amount": 100}

    export_to_json(filepath, data)

    with open(filepath, encoding="utf-8") as f:
        result = json.load(f)

    assert result == data


def test_export_to_csv(tmp_path):
    filepath = tmp_path / "data.csv"

    transactions = [
        Transaction("2025-01-01", "100000", "Зарплата", "Премия"),
        Transaction("2025-01-02", "-5000", "Еда", "Ресторан 'Вивальди'"),
    ]

    export_to_csv(transactions, filepath)

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows[0]["category"] == "Зарплата"
    assert rows[1]["category"] == "Еда"
    assert rows[1]["amount"] == "-5000.0"


def test_export_context_json(tmp_path):
    filepath = tmp_path / "report.json"

    data = {"test": 123}

    with ExportContext(filepath) as ctx:
        ctx.write(data)

    with open(filepath, encoding="utf-8") as f:
        result = json.load(f)

    assert result == data


def test_export_context_csv(tmp_path):
    filepath = tmp_path / "report.csv"

    transactions = [
        Transaction("2025-01-01", "10", "misc", "test")
    ]

    with ExportContext(filepath) as ctx:
        ctx.write(transactions)

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows[0]["category"] == "misc"


def test_export_context_unsupported_format(tmp_path):
    filepath = tmp_path / "report.txt"

    with pytest.raises(ValueError):
        with ExportContext(filepath) as ctx:
            ctx.write({"a": 1})

def test_export_to_json_preserves_cyrillic(tmp_path):
    filepath = tmp_path / "cyrillic.json"

    data = {"name": "Александр", "city": "Пермь"}

    export_to_json(filepath, data)

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    assert "Александр" in content
    assert "Пермь" in content