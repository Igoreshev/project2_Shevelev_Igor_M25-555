SUPPORTED_TYPES = {"int", "str", "bool"}


def create_table(metadata: dict, table_name: str, columns: list) -> dict:

    #существует ли таблица
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_schema = {}

    #добавляем ID:int
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

