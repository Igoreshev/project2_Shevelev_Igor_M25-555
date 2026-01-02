
import shlex

from .utils import load_metadata, save_metadata
from .core import create_table, drop_table


DB_META_FILE = "db_meta.json"

def _print_help():
    print("""***Процесс работы с таблицей***
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ..
<command> list_tables
<command> drop_table <имя_таблицы>
<command> exit - выйти из программы
<command> help - справочная информация
""")


def run():
    print("Первая попытка запустить проект!\n")
    print("***")
    _print_help()

    while True:
        metadata = load_metadata(DB_META_FILE)

        user_input = input("Введите команду: ").strip()
        if not user_input:
            continue

        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")
            continue

        command = args[0]

        if command == "help":
            _print_help()

        elif command == "exit":
            print("Выход из программы.")
            break

        elif command == "create_table":
            if len(args) < 3:
                print("Некорректное значение. Попробуйте снова.")
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
                print(f'Таблица "{table_name}" успешно создана со столбцами: {cols}')

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[1]
            old_count = len(metadata)

            metadata = drop_table(metadata, table_name)
            save_metadata(DB_META_FILE, metadata)

            if len(metadata) < old_count:
                print(f'Таблица "{table_name}" успешно удалена.')

        elif command == "list_tables":
            if not metadata:
                print("Таблиц нет.")
            else:
                for table_name in metadata:
                    print(f"- {table_name}")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
    