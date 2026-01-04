def parse_value(raw_value: str):
    raw_value = raw_value.strip()


    if raw_value.lower() == "true":
        return True
    if raw_value.lower() == "false":
        return False

   
    if raw_value.isdigit():
        return int(raw_value)


    if raw_value.startswith('"') and raw_value.endswith('"'):
        return raw_value[1:-1]

    return raw_value



def parse_condition(condition: str) -> dict:

    if "=" not in condition:
        raise ValueError("Условие должно содержать '='")

    column, raw_value = condition.split("=", 1)
    column = column.strip()

    value = parse_value(raw_value)

    return {column: value}


def parse_set_clause(set_clause: str) -> dict:

    return parse_condition(set_clause)
