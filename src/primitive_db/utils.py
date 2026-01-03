import json
import os

DATA_DIR = "data"

def load_metadata(filepath):
    'Загружает данные из JSON'
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_metadata(filepath: str, data: dict) -> None:
    'Сохраняем данные'
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_table_data(table_name: str) -> list:
    """
    Загружает данные таблицы из data/<table_name>.json.
    Если файл не существует — возвращает пустой список.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list) -> None:
    """
    Сохраняет данные таблицы в data/<table_name>.json.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def create_cacher():
    """
    Фабрика кэширующей функции.
    Кэш хранится в замыкании.
    """
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result
        return result

    return cache_result
