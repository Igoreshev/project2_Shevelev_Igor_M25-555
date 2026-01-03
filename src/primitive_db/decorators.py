from functools import wraps
import time

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except FileNotFoundError:
            print(
                "Ошибка: файл данных не найден. "
                "Возможно, таблица еще не создана."
            )

        except KeyError as exc:
            print(f"Ошибка: таблица или столбец не найден: {exc}")

        except ValueError as exc:
            print(f"Ошибка валидации данных: {exc}")

        except Exception as exc:
            print(f"Непредвиденная ошибка: {exc}")

        return None

    return wrapper

def confirm_action(action_name: str):
    """
    Декоратор с аргументом.
    Запрашивает подтверждение опасной операции.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()

            if answer != "y":
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator

def log_time(func):
    """
    Декоратор для замера времени выполнения функции.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()

        duration = end - start
        print(
            f'Функция {func.__name__} выполнилась за {duration:.3f} секунд.'
        )

        return result

    return wrapper