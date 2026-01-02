import json

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

