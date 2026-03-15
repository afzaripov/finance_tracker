import argparse
from pprint import pprint

from decorators import timer

from parser import read_transactions, filter_by_category, filter_by_month, filter_by_type
from analyzer import get_summary, get_top_expenses
from exporter import ExportContext

@timer
def main():
    parser = argparse.ArgumentParser(description="Finance Tracker")

    parser.add_argument("--file", "-f", required=True, help="Путь к CSV файлу")
    parser.add_argument("--stats", action="store_true", help="Показать статистику")
    parser.add_argument("--category", "-c", help="Фильтр по категории")
    parser.add_argument("--month", "-m", type=str, help="Фильтр по месяцу (формат: `2025-01`)")
    parser.add_argument("--type", "-t", help="Тип: `income` или `expense`")
    parser.add_argument("--top", type=int, help="Топ-N крупнейших расходов")
    parser.add_argument(
        "--export", "-e", help="Путь к файлу для экспорта (`.json` или `.csv`)"
    )

    args = parser.parse_args()

    gen = read_transactions(args.file)
    if args.category:
        gen = filter_by_category(gen, args.category)
    
    if args.month:
        date = args.month.split(sep="-")
        gen = filter_by_month(gen, int(date[1]), int(date[0]))

    if args.type:
        gen = filter_by_type(gen, args.type)
    
    transactions = list(gen)

    if args.stats:
        pprint(get_summary(transactions))
    
    if args.top:
        pprint(get_top_expenses(transactions, args.top))
    
    if args.export:
        with ExportContext(args.export) as ex_context:
            ex_context.write([t.to_dict() for t in transactions])
    
    if not args.stats and not args.top:
        for t in transactions:
            pprint(t)