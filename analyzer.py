from transaction import Transaction
from datetime import datetime


def get_summary(transactions: list[Transaction]) -> dict:
    total_income = sum(t.amount for t in transactions if t.is_income())
    total_expense = sum(t.amount for t in transactions if t.is_expense())
    count_income = sum(1 for t in transactions if t.is_income())
    count_expense = sum(1 for t in transactions if t.is_expense())

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net": total_income + total_expense,
        "count": len(transactions),
        "count_income": count_income,
        "count_expense": count_expense,
    }


def get_by_category(transactions: list[Transaction]) -> dict:
    categories_amount = {}

    for t in transactions:
        if t.is_expense():
            categories_amount[t.category] = (
                categories_amount.get(t.category, 0) + t.amount
            )

    return categories_amount


def get_top_expenses(transactions: list[Transaction], n: int = 5):
    expenses = [t for t in transactions if t.is_expense()]
    return sorted(expenses, key=lambda t: abs(t.amount), reverse=True)[:n]


def get_monthly_stats(transactions: list[Transaction]) -> dict:
    monthly_stats = {}
    for transaction in transactions:
        date = transaction.date.strftime("%Y-%m")

        if date not in monthly_stats:
            monthly_stats[date] = {"income": 0.0, "expense": 0.0}

        if transaction.is_income():
            monthly_stats[date]["income"] += transaction.amount

        if transaction.is_expense():
            monthly_stats[date]["expense"] += transaction.amount

    return monthly_stats


def get_category_stats(transactions: list[Transaction]) -> dict:
    categories_amount = {}

    for t in transactions:
        if t.is_expense():
            if t.category not in categories_amount:
                categories_amount[t.category] = {"total": 0.0, "count": 0, "average": 0.0}
            
            categories_amount[t.category]["total"] += t.amount
            categories_amount[t.category]["count"] += 1
    
    category_stats = []

    for key, value in categories_amount.items():
        category_stats.append(
            {
                "category":key,
                "total": value["total"],
                "count": value["count"],
                "average" : value["total"] / value["count"]
            }
        )
    
    return sorted(category_stats, key=lambda t: abs(t["total"]), reverse=True)

