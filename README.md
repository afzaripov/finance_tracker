# CSV Finance Tracker

CLI-утилита для анализа банковских выписок в формате CSV.

Читает транзакции, фильтрует по категории/месяцу/типу, считает статистику и экспортирует результаты в JSON или CSV. Работает с большими файлами через генераторы — без загрузки всего файла в память.


## Структура проекта

```
finance_tracker/
├── transaction.py          # Модель данных — класс Transaction
├── parser.py               # Чтение и парсинг CSV через генераторы
├── analyzer.py             # Статистика и группировка
├── exporter.py             # Экспорт результатов (JSON, CSV, контекстный менеджер)
├── decorators.py           # @timer, @validate_file, @log_call
├── cli.py                  # argparse + оркестрация модулей
├── main.py                 # Точка входа
├── generate_test_data.py   # Генерация тестового CSV (300+ транзакций)
└── tests/
    ├── test_transaction.py
    ├── test_parser.py
    ├── test_analyzer.py
    └── test_exporter.py
```

## Быстрый старт

### 1. Сгенерировать тестовые данные

```bash
python generate_test_data.py
# Создаёт файл test_transactions.csv с 300+ транзакциями за 6 месяцев
```

### 2. Посмотреть общую статистику

```bash
python main.py --file test_transactions.csv --stats
```

### 3. Топ крупнейших расходов

```bash
python main.py --file test_transactions.csv --top 5
```

### 4. Фильтрация

```bash

python main.py --file test_transactions.csv --category "Еда"

# Транзакции за январь 2025
python main.py --file test_transactions.csv --month 2025-01

# Только доходы
python main.py --file test_transactions.csv --type income

# Комбинация: расходы за январь, экспорт в JSON
python main.py --file test_transactions.csv --type expense --month 2025-01 --export jan_expenses.json
```

### 5. Экспорт

```bash
# В JSON
python main.py --file test_transactions.csv --stats --export report.json

# В CSV
python main.py --file test_transactions.csv --category "Транспорт" --export transport.csv
```

## Аргументы CLI

| Аргумент     | Короткий | Тип  | Описание                                    |
|--------------|----------|------|---------------------------------------------|
| `--file`     | `-f`     | str  | **Обязательный.** Путь к CSV файлу          |
| `--stats`    |          | flag | Показать общую статистику                   |
| `--category` | `-c`     | str  | Фильтр по категории                        |
| `--month`    | `-m`     | str  | Фильтр по месяцу (формат: `2025-01`)       |
| `--type`     | `-t`     | str  | Тип: `income` или `expense`                |
| `--top`      |          | int  | Топ-N крупнейших расходов                   |
| `--export`   | `-e`     | str  | Экспорт в файл (`.json` или `.csv`)        |

## Формат входного CSV

```csv
date,amount,category,description
2025-01-15,-1500.50,Еда,Пятёрочка
2025-01-16,-800.00,Транспорт,Яндекс.Такси
2025-01-17,85000.00,Зарплата,Аванс
```

- `date` — дата в формате `YYYY-MM-DD`
- `amount` — сумма: отрицательная = расход, положительная = доход
- `category` — произвольная строка
- `description` — описание транзакции

Строки с некорректными данными пропускаются с предупреждением — программа не падает.
