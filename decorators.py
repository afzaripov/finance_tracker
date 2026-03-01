from functools import wraps
from pathlib import Path
import time
from datetime import datetime

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} выполнилась за {end-start:.3f} сек')
        return result
    return wrapper


def validate_file(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pathfile = Path(args[0])

        if not pathfile.exists():
            raise FileNotFoundError(f"Файл {pathfile} не найден")
        
        if pathfile.suffix != ".csv":
            raise ValueError(f"Ожидается .csv файл, получен: {pathfile.suffix}")
        
        return func(*args, **kwargs)
    return wrapper


def log_call(log_path: str = "tracker.log"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with open(log_path, "a", encoding="utf-8") as file:
                data = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {func.__name__} | args: {args} | kwargs: {kwargs}\n"
                file.write(data)
            return func(*args, **kwargs)
        return wrapper
    return decorator

