from .utils import load_table_data, save_table_data, create_cacher
from .decorators import handle_db_errors, confirm_action, log_time


SUPPORTED_TYPES = {"int", "str", "bool"}

@handle_db_errors
def create_table(metadata: dict, table_name: str, columns: list) -> dict:

    if table_name in metadata:
        raise KeyError(f'Таблица "{table_name}" уже существует.')

    table_schema = {}

    table_schema["ID"] = "int"

    for column in columns:
        if ":" not in column:
            raise ValueError(f"Некорректное значение: {column}")

        column_name, column_type = column.split(":", 1)

        if column_type not in SUPPORTED_TYPES:
            raise ValueError(f"Некорректный тип данных: {column_type}")

        table_schema[column_name] = column_type

    metadata[table_name] = table_schema
    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata: dict, table_name: str) -> dict:
    """
    удаляет таблицу из metadata
    """

    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует.')


    del metadata[table_name]
    return metadata

@log_time
@handle_db_errors
def insert(metadata: dict, table_name: str, values: list) -> list:
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует.')

    schema = metadata[table_name]
    columns = [c for c in schema if c != "ID"]

    if len(values) != len(columns):
        raise ValueError(
        "Количество значений не соответствует количеству столбцов."
    )

    data = load_table_data(table_name)

    new_id = max([row["ID"] for row in data], default=0) + 1
    new_row = {"ID": new_id}

    for column, value in zip(columns, values):
        col_type = schema[column]

        
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
                raise ValueError(f"Некорректное логическое значение: {value}")

        new_row[column] = value

    data.append(new_row)
    save_table_data(table_name, data)
    return data

select_cache = create_cacher()
@log_time
@handle_db_errors
def select(table_data: list, where_clause: dict | None = None) -> list:
    cache_key = str(where_clause)

    def calculate():
        if where_clause is None:
            return table_data

        return [
            row for row in table_data
            if all(row.get(col) == val for col, val in where_clause.items())
        ]

    return select_cache(cache_key, calculate)



@handle_db_errors
def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    for row in table_data:
        if all(row.get(col) == val for col, val in where_clause.items()):
            for col, new_value in set_clause.items():
                if col != "ID":
                    row[col] = new_value
    return table_data


@confirm_action("удаление записи")
@handle_db_errors
def delete(table_data: list, where_clause: dict) -> list:
    return [
        row for row in table_data
        if not all(row.get(col) == val for col, val in where_clause.items())
    ]
