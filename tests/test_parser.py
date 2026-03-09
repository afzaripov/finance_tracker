import pytest
import csv
from typing import Generator

from transaction import Transaction
from parser import read_transactions, filter_by_category, filter_by_month, filter_by_type


@pytest.fixture
def make_csv(tmp_path):
    def _make(data: list[list]) -> str:
        log_file = tmp_path / "test.csv"
        with open(log_file, 'w', encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "amount", "category", "description"])
            writer.writerows(data)
        return str(log_file)
    return _make


def test_read_transactions_returns_valid_entries(make_csv):
    path = make_csv([
        ["2025-12-29", "-1324.85", "Автомобиль", "Заправка"],
        ["2025-12-23", "45244.15", "Зарплата", "Аванс за февраль"]
    ])

    gen = read_transactions(path)
    assert isinstance(gen, Generator)

    entries = list(gen)

    assert len(entries) == 2

    assert isinstance(entries[0], Transaction)
    assert entries[0].category == "Автомобиль"
    assert entries[0].description == "Заправка"

    assert isinstance(entries[1], Transaction)
    assert entries[1].category == "Зарплата"
    assert "за" in entries[1].description


def test_read_transactions_with_invalid_record(make_csv):
    path = make_csv([
        ["2025-12-29", "-1324.85", "Автомобиль", "Заправка"],
        ["2025-12-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2024-12-29", "-1214.15", "Автомобиль", "Заправка"],
        ["aaaa", "45244.15", "Зарплата", "Аванс за февраль"]
    ])

    gen = read_transactions(path)
    assert isinstance(gen, Generator)
    
    entries = list(gen)

    assert len(entries) == 3

    assert isinstance(entries[0], Transaction)
    assert entries[0].category == "Автомобиль"
    assert entries[0].description == "Заправка"

    assert isinstance(entries[1], Transaction)
    assert entries[1].category == "Зарплата"
    assert "за" in entries[1].description


def test_read_transactions_invalid_path():
    with pytest.raises(FileNotFoundError, match="Файл log_file.csv не найден"):
        entries = list(read_transactions("log_file.csv"))


def test_filter_by_category_returns_correct_transaction(make_csv):
    path = make_csv([
        ["2025-12-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2025-12-29", "-1324.85", "Автомобиль", "Заправка"],
        ["2025-12-19", "-1451.50", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)
    filtered = list(filter_by_category(entries, "Автомобиль"))

    assert len(filtered) == 2

    assert filtered[0].category == "Автомобиль"
    assert filtered[0].amount == -1324.85
    assert filtered[0].description == "Заправка"


def test_filter_by_months_returns_correct_transaction(make_csv):
    path = make_csv([
        ["2025-11-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2026-01-19", "-1451.50", "Автомобиль", "Заправка"],
        ["2025-11-29", "-1324.85", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)
    filtered = list(filter_by_month(entries, 11, 2025))

    assert len(filtered) == 2

    assert filtered[1].category == "Автомобиль"
    assert filtered[1].amount == -1324.85
    assert filtered[1].description == "Заправка"


def test_filter_by_months_with_invalid_month_value(make_csv):
    path = make_csv([
        ["2025-11-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2026-01-19", "-1451.50", "Автомобиль", "Заправка"],
        ["2025-11-29", "-1324.85", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)

    with pytest.raises(ValueError, match="Переданное значение месяца: -1, тип данных: <class 'int'>. Должно быть число в диапазоне от 1 до 12 включительно"):
        filtered = list(filter_by_month(entries, -1, 2025))


def test_filter_by_months_with_invalid_month_type(make_csv):
    path = make_csv([
        ["2025-11-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2026-01-19", "-1451.50", "Автомобиль", "Заправка"],
        ["2025-11-29", "-1324.85", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)

    with pytest.raises(ValueError, match="Переданное значение месяца: 123, тип данных: <class 'str'>. Должно быть число в диапазоне от 1 до 12 включительно"):
        filtered = list(filter_by_month(entries, "123", 2025))


def test_filter_by_months_with_invalid_year_value(make_csv):
    path = make_csv([
        ["2025-11-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2026-01-19", "-1451.50", "Автомобиль", "Заправка"],
        ["2025-11-29", "-1324.85", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)

    with pytest.raises(ValueError, match="Переданное значение года: 2025, тип данных: <class 'str'>. Должно быть число в диапазоне от 2000 до текущего года"):
        filtered = list(filter_by_month(entries, 11, "2025"))


def test_filter_by_type_returns_correct_transaction(make_csv):
    path = make_csv([
        ["2025-11-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2026-01-19", "-1451.50", "Автомобиль", "Заправка"],
        ["2025-11-29", "-1324.85", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)
    filtered = list(filter_by_type(entries, "income"))

    assert len(filtered) == 1

    assert filtered[0].category == "Зарплата"
    assert filtered[0].amount == 45244.15
    assert filtered[0].description == "Аванс за февраль"


def test_filter_by_type_with_incorrect_type(make_csv):
    path = make_csv([
        ["2025-11-23", "45244.15", "Зарплата", "Аванс за февраль"],
        ["2026-01-19", "-1451.50", "Автомобиль", "Заправка"],
        ["2025-11-29", "-1324.85", "Автомобиль", "Заправка"]
    ])

    entries = read_transactions(path)

    with pytest.raises(ValueError, match="Некорректный тип транзакций - 'abcd', ожидался: 'expense/income'"):
        filtered = list(filter_by_type(entries, "abcd"))