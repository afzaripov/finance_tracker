import pytest


from transaction import Transaction
from analyzer import (
    get_summary,
    get_by_category,
    get_top_expenses,
    get_category_stats,
    get_monthly_stats,
)


def test_get_summary_returns_correct_dict():
    transactions = [
        Transaction("2012-1-1", "-1000", "Еда", ""),
        Transaction("2012-1-1", "-2000", "Еда", ""),
        Transaction("2012-1-1", "20000", "Зарплата", ""),
    ]

    expected_result = {
        "total_income": 20000.00,
        "total_expense": -3000.00,
        "net": 17000.00,
        "count": 3,
        "count_income": 1,
        "count_expense": 2,
    }

    result = get_summary(transactions)

    assert isinstance(result, dict)
    assert result == expected_result
    assert result["net"] == expected_result["net"]


def test_get_by_category_returns_only_valid_expenses():
    transactions = [
        Transaction("2012-1-1", "-1000", "Еда", ""),
        Transaction("2012-1-1", "-2000", "Еда", ""),
        Transaction("2012-1-1", "20000", "Зарплата", ""),
        Transaction("2012-1-1", "-5000", "Развлечения", "Караоке"),
        Transaction("2012-1-1", "20000", "Зарплата", ""),
    ]

    expected_result = {
        "Еда": -3000.00,
        "Развлечения": -5000.00,
    }

    result = get_by_category(transactions)

    assert isinstance(result, dict)
    assert len(result) == 2
    assert result == expected_result
    assert result["Еда"] == expected_result["Еда"]


def test_get_top_expenses_return_correct_dict():
    transactions = [
        Transaction("2012-1-1", "-1000", "Еда", ""),
        Transaction("2012-1-1", "-2000", "Еда", ""),
        Transaction("2012-1-1", "20000", "Зарплата", ""),
        Transaction("2012-1-1", "-5000", "Развлечения", "Караоке"),
        Transaction("2012-1-1", "20000", "Зарплата", ""),
    ]

    expected_result = [
        Transaction("2012-1-1", "-5000", "Развлечения", "Караоке"),
        Transaction("2012-1-1", "-2000", "Еда", ""),
        Transaction("2012-1-1", "-1000", "Еда", ""),
    ]

    result = get_top_expenses(transactions, 5)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result == expected_result


def test_monthly_stats_groups_by_month():
    transactions = [
        Transaction("2012-1-1", "-1000", "Еда", ""),
        Transaction("2012-2-1", "-2000", "Еда", ""),
        Transaction("2012-2-1", "20000", "Зарплата", ""),
        Transaction("2012-3-1", "-5000", "Развлечения", "Караоке"),
        Transaction("2012-1-1", "-4000", "Развлечения", ""),
        Transaction("2012-3-1", "40000", "Зарплата", ""),
    ]

    expected_result = {
        "2012-01": {"income": 0.0, "expense": -5000.0},
        "2012-02": {"income": 20000.0, "expense": -2000.0},
        "2012-03": {"income": 40000.0, "expense": -5000.0},
    }

    result = get_monthly_stats(transactions)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result == expected_result


def test_category_stats_returns_valid_expenses():
    transactions = [
        Transaction("2012-1-1", "-1000", "Еда", ""),
        Transaction("2012-2-1", "-2000", "Еда", ""),
        Transaction("2012-2-1", "20000", "Зарплата", ""),
        Transaction("2012-3-1", "-5000", "Развлечения", "Караоке"),
        Transaction("2012-1-1", "-4000", "Развлечения", ""),
        Transaction("2012-3-1", "40000", "Зарплата", ""),
    ]

    expected_result = [
        {"category": "Развлечения", "total": -9000.00, "count": 2, "average": -4500.00},
        {"category": "Еда", "total": -3000.00, "count": 2, "average": -1500.00},
    ]

    result = get_category_stats(transactions)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result == expected_result
    assert result[0]["total"] == -9000.00