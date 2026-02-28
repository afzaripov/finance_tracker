import pytest
from datetime import datetime
from transaction import Transaction


def test_create_transaction_with_valid_data():
    t = Transaction("2025-12-23", "2000", "Еда", "Хлеб")
    assert isinstance(t, Transaction)
    assert isinstance(t.date, datetime)
    assert isinstance(t.amount, float)


def test_create_transaction_with_invalid_date():
    with pytest.raises(ValueError, match="Expected date in format 'YYYY-MM-DD'"):
        t = Transaction("2025-as-23", "2000", "Еда", "Хлеб")


def test_create_transaction_with_invalid_amout():
    with pytest.raises(ValueError, match="Expected amount as a number"):
        t = Transaction("2025-12-23", "qwer", "Еда", "Хлеб")


def test_create_transaction_with_zero_amout():
    with pytest.raises(ValueError, match="Amount cant be 0"):
        t = Transaction("2025-12-23", "0", "Еда", "Хлеб")

def test_transaction_is_expense():
    t1 = Transaction("2025-12-23", "2000", "Еда", "Хлеб")
    t2 = Transaction("2025-12-23", "-2000", "Еда", "Хлеб")
    assert not t1.is_expense()
    assert t2.is_expense()


def test_transaction_is_income():
    t1 = Transaction("2025-12-23", "-2000", "Еда", "Хлеб")
    t2 = Transaction("2025-12-23", "2000", "Еда", "Хлеб")
    assert not t1.is_income()
    assert t2.is_income()


def test_transaction_to_dict():
    t1 = Transaction("2025-12-23", "2000", "Еда", "Хлеб")
    expected = {
        "date": "2025-12-23",
        "amount": 2000,
        "category": "Еда",
        "description": "Хлеб",
    }
    assert isinstance(t1.to_dict(), dict)
    assert isinstance(t1.to_dict()["date"], str)
    assert t1.to_dict() == expected
