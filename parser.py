from typing import Generator, Iterator
from datetime import datetime

from decorators import validate_file, timer
from transaction import Transaction


import csv


@timer
@validate_file
def read_transactions(filepath: str) -> Generator:
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                transaction = Transaction(
                    row["date"], row["amount"], row["category"], row["description"]
                )
                yield transaction
            except ValueError as e:
                print(f"Предупреждение: пропущена строка — {e}")


def filter_by_category(transactions: Iterator[Transaction], category: str) -> Generator:
    for transaction in transactions:
        if transaction.category == category:
            yield transaction


def filter_by_month(transactions: Iterator[Transaction], month: int, year:int = None) -> Generator:
    if not (0 < month <= 12) or not isinstance(month, int):
        raise ValueError(
            "Значение месяца должно быть числом в диапазоне от 1 до 12 включительно"
        )

    if year is None:
        year = datetime.now().year

    if not isinstance(year, int):
        raise ValueError("Значение года должно быть числом")

    for transaction in transactions:
        if transaction.date.month == month and transaction.date.year == year:
            yield transaction


def filter_by_type(transactions: Iterator[Transaction], tx_type: str) -> Generator:
    if not (tx_type == "expense" or tx_type == "income"):
        raise ValueError("Некорректный тип транзакций, ожидался: expense/income")

    for transaction in transactions:
        if tx_type == "income" and transaction.is_income():
            yield transaction
        elif tx_type == "expense" and transaction.is_expense():
            yield transaction
