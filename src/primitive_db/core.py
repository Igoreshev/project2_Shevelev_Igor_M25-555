from .utils import load_table_data, save_table_data



SUPPORTED_TYPES = {"int", "str", "bool"}


def create_table(metadata: dict, table_name: str, columns: list) -> dict:

    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_schema = {}

    table_schema["ID"] = "int"

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = column.split(":", 1)

        if column_type not in SUPPORTED_TYPES:
            print(f"Некорректное значение: {column_type}. Попробуйте снова.")
            return metadata

        table_schema[column_name] = column_type

    metadata[table_name] = table_schema
    return metadata


def drop_table(metadata: dict, table_name: str) -> dict:
    """
    удаляет таблицу из metadata
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    return metadata

def insert(metadata: dict, table_name: str, values: list) -> list:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return []

    schema = metadata[table_name]
    columns = [c for c in schema if c != "ID"]

    if len(values) != len(columns):
        print("Ошибка: Количество значений не соответствует количеству столбцов.")
        return []

    data = load_table_data(table_name)

    new_id = max([row["ID"] for row in data], default=0) + 1
    new_row = {"ID": new_id}

    for column, value in zip(columns, values):
        col_type = schema[column]

        try:
            if col_type == "int":
                value = int(value)
            elif col_type == "str":
                value = str(value)
            elif col_type == "bool":
                if str(value).lower() in ("true", "1"):
                    value = True
                elif str(value).lower() in ("false", "0"):
                    value = False
                else:
                    raise ValueError
        except ValueError:
            print(f"Ошибка: Некорректное значение для столбца {column}.")
            return []

        new_row[column] = value

    data.append(new_row)
    save_table_data(table_name, data)
    return data


def select(table_data: list, where_clause: dict | None = None) -> list:
    if where_clause is None:
        return table_data

    result = []
    for row in table_data:
        if all(row.get(col) == val for col, val in where_clause.items()):
            result.append(row)

    return result


def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    for row in table_data:
        if all(row.get(col) == val for col, val in where_clause.items()):
            for col, new_value in set_clause.items():
                if col != "ID":
                    row[col] = new_value
    return table_data


def delete(table_data: list, where_clause: dict) -> list:
    return [
        row for row in table_data
        if not all(row.get(col) == val for col, val in where_clause.items())
    ]
