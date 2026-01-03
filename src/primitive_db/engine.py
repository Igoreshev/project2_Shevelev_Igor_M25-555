import shlex
from prettytable import PrettyTable

from .utils import (
    load_metadata,
    save_metadata,
    load_table_data,
    save_table_data,
)
from .core import (
    create_table,
    drop_table,
    insert,
    select,
    update,
    delete,
)
from .parser import parse_condition, parse_set_clause, parse_value


DB_META_FILE = "db_meta.json"


def _print_help():
    print("""***Команды базы данных***

Таблицы:
<command> create_table <имя> <столбец:тип> ...
<command> drop_table <имя>
<command> list_tables

Данные:
<command> insert into <таблица> values (<v1>, <v2>, ...)
<command> select from <таблица>
<command> select from <таблица> where <столбец> = <значение>
<command> update <таблица> set <столбец> = <значение> where <столбец> = <значение>
<command> delete from <таблица> where <столбец> = <значение>
<command> info <таблица>

Служебные:
<command> help
<command> exit
""")


def run():
    print("Первая попытка запустить проект!\n")
    _print_help()

    while True:
        metadata = load_metadata(DB_META_FILE)

        user_input = input("Введите команду: ").strip()
        if not user_input:
            continue

        if user_input == "exit":
            print("Выход из программы.")
            break

        if user_input == "help":
            _print_help()
            continue

        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")
            continue

        command = args[0]

        # ---------- CREATE TABLE ----------
        if command == "create_table":
            if len(args) < 3:
                print("Некорректное значение.")
                continue

            table_name = args[1]
            columns = args[2:]

            metadata = create_table(metadata, table_name, columns)
            save_metadata(DB_META_FILE, metadata)

            if table_name in metadata:
                cols = ", ".join(
                    f"{name}:{dtype}"
                    for name, dtype in metadata[table_name].items()
                )
                print(f'Таблица "{table_name}" успешно создана: {cols}')

        # ---------- DROP TABLE ----------
        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение.")
                continue

            table_name = args[1]
            old_count = len(metadata)

            metadata = drop_table(metadata, table_name)
            save_metadata(DB_META_FILE, metadata)

            if len(metadata) < old_count:
                print(f'Таблица "{table_name}" успешно удалена.')

        # ---------- LIST TABLES ----------
        elif command == "list_tables":
            if not metadata:
                print("Таблиц нет.")
            else:
                for table_name in metadata:
                    print(f"- {table_name}")

        # ---------- INSERT ----------
        elif args[:2] == ["insert", "into"] and "values" in args:
            table_name = args[2]

            values_part = user_input[user_input.find("values") + 6:]
            values_part = values_part.strip().lstrip("(").rstrip(")")
            raw_values = [v.strip() for v in values_part.split(",")]
            values = [parse_value(v) for v in raw_values]

            data = insert(metadata, table_name, values)
            if data:
                print(f'Запись успешно добавлена в таблицу "{table_name}".')

        # ---------- SELECT ----------
        elif args[:2] == ["select", "from"]:
            table_name = args[2]
            table_data = load_table_data(table_name)

            if "where" in args:
                where_index = args.index("where")
                condition = " ".join(args[where_index + 1:])
                where_clause = parse_condition(condition)
                result = select(table_data, where_clause)
            else:
                result = select(table_data)

            if not result:
                print("Нет данных.")
                continue

            table = PrettyTable()
            table.field_names = result[0].keys()
            for row in result:
                table.add_row(row.values())

            print(table)

        # ---------- UPDATE ----------
        elif command == "update" and "set" in args and "where" in args:
            table_name = args[1]
            table_data = load_table_data(table_name)

            set_index = args.index("set")
            where_index = args.index("where")

            set_clause = parse_set_clause(
                " ".join(args[set_index + 1:where_index])
            )
            where_clause = parse_condition(
                " ".join(args[where_index + 1:])
            )

            updated_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, updated_data)

            print(f'Таблица "{table_name}" успешно обновлена.')

        # ---------- DELETE ----------
        elif args[:2] == ["delete", "from"] and "where" in args:
            table_name = args[2]
            table_data = load_table_data(table_name)

            where_index = args.index("where")
            where_clause = parse_condition(
                " ".join(args[where_index + 1:])
            )

            updated_data = delete(table_data, where_clause)
            save_table_data(table_name, updated_data)

            print(f'Записи из таблицы "{table_name}" успешно удалены.')

        # ---------- INFO ----------
        elif command == "info":
            if len(args) != 2:
                print("Некорректное значение.")
                continue

            table_name = args[1]
            if table_name not in metadata:
                print(f'Таблица "{table_name}" не существует.')
                continue

            print(f"Таблица: {table_name}")
            print("Столбцы:")
            for col, dtype in metadata[table_name].items():
                print(f"- {col}:{dtype}")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")

