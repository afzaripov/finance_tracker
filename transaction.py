from datetime import datetime


class Transaction:
    def __init__(self, date: str, amount: str, category: str, description: str):
        try:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError("Expected date in format 'YYYY-MM-DD'") from e

        try:
            self.amount = float(amount)
        except ValueError as e:
            raise ValueError("Expected amount as a number") from e

        if self.amount == 0:
            raise ValueError("Amount cant be 0")
        self.category = category
        self.description = description

    def is_expense(self) -> bool:
        """
        Возвращает `True` если транзакция является расходом
        """
        return self.amount < 0

    def is_income(self) -> bool:
        """
        Возвращает `True` если транзакция является доходом
        """
        return self.amount > 0
    

    def to_dict(self)->dict:
        """
        Преобразует объект в словарь для экспорта
        """
        return {
            "date" : self.date.strftime("%Y-%m-%d"),
            "amount" : self.amount,
            "category" : self.category,
            "description" : self.description
        }

    def __str__(self):
        return f"{self.date.strftime("%Y-%m-%d")} | {self.category} | {self.amount} | {self.description}"
    
    def __repr__(self):
        return f"Transaction(date={self.date.strftime("%Y-%m-%d")}, amount={self.amount}, category={self.category})"