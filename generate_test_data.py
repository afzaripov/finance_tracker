import csv
import random
from datetime import datetime, timedelta


def generate_test_data(filepath: str = "test_data.csv"):
    data = []
    for i in range(300):
        record = []
        date = generate_date()
        category = generate_category()
        amount = generate_amount(category)
        description = generate_description(category)
        
        record.append(date)
        record.append(amount)
        record.append(category)
        record.append(description)

        data.append(record)

    with open(filepath, 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "amount", "category", "description"])
        writer.writerows(data)


def generate_date() -> str:
    random_day = random.randint(0,180)
    transaction_day = datetime.now() - timedelta(days=random_day) 
    return datetime.strftime(transaction_day, "%Y-%m-%d")

def generate_category() -> str:
    categories = ["Еда", "Зарплата", "Квартира", "Развлечения", "Автомобиль"]
    return random.choice(categories)

def generate_amount(category: str) -> float:
    if category == "Зарплата":
        return str(random.uniform(50000, 100000))
    elif category == "Еда":
        return str(random.uniform(-5000, -500))
    elif category == "Квартира":
        return str(random.uniform(-10000, -6000))
    elif category == "Развлечения":
        return str(random.uniform(-4000, -1000))
    elif category == "Автомобиль":
        return str(random.uniform(-3000, -1000))

def generate_description(category: str) -> str:
    food_expenses = ["Пятерочка", "Перекресток", "Магнит", "Красное и Белое"]
    rent_and_utilities = ["Аренда", "Водоснабжение", "Электричество"]
    entertainments = ["Кино", "Караоке", "Боулинг"]
    vehicle_expenses = ["Парковка", "Заправка", "Техническое обслуживание"]

    if category == "Зарплата":
        return "Заработная плата"
    elif category == "Еда":
        return random.choice(food_expenses)
    elif category == "Квартира":
        return random.choice(rent_and_utilities)
    elif category == "Развлечения":
        return random.choice(entertainments)
    elif category == "Автомобиль":
        return random.choice(vehicle_expenses)


if __name__ == "__main__":
    generate_test_data()