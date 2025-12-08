#! /usr/bin/env python3

EXAMPLE_INPUT = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


def read_file(file_path):
    with open(file_path, "r") as file:
        return [line for line in file.readlines()]


def format_lines(lines: list[str]) -> list[str]:
    result = []
    for line in lines[:-1]:
        values = [int(x) for x in line.split(" ") if x.isdigit()]
        result.append(values)
    operator_line = lines[-1]
    operators = [x for x in operator_line.split(" ") if x in ("+", "*")]
    result.append(operators)
    return result


def compute_column(formated_lines: list[str], column_id: int) -> int:
    operators = formated_lines[-1][column_id]
    values = [int(line[column_id]) for line in formated_lines[:-1]]
    computed_values = []
    if operators == "+":
        computed_values = sum(values)
    elif operators == "*":
        product = 1
        for v in values:
            product *= v
        computed_values = product
    else:
        raise ValueError(f"Unknown operator: {operators}")
    return computed_values


def compute_all_columns(formatted_lines: list[str]) -> list[int]:
    result = []
    num_columns = len(formatted_lines[0])
    for col_id in range(num_columns):
        computed_value = compute_column(formatted_lines, col_id)
        result.append(computed_value)
    return result


def format_cephalopod(lines: list[str]) -> list[str]:
    formatted_columns = []
    number = ""
    max_len_line = max(len(line) for line in lines)
    for idx in range(max_len_line):
        number = ""
        for line in lines[:-1]:
            if idx < len(line) and line[idx].isdigit():
                number += line[idx]
        formatted_columns.append(number)
    result = []
    operators_line = [op for op in lines[-1].split(" ") if op in ("+", "*")]
    current_line = []
    for number in formatted_columns:
        if number.isdigit():
            current_line.append(number)
        else:
            operator = operators_line.pop(0)
            current_line.append(operator)
            result.append(current_line)
            current_line = []
    if current_line:
        operator = operators_line.pop(0)
        current_line.append(operator)
        result.append(current_line)
    return result


def compute_column_cephalopod(formatted_lines: list[str], column_id: int) -> int:
    operator = formatted_lines[column_id][-1]
    values = [int(val) for val in formatted_lines[column_id][:-1]]
    computed_values = []
    if operator == "+":
        computed_values = sum(values)
    elif operator == "*":
        product = 1
        for v in values:
            product *= v
        computed_values = product
    else:
        raise ValueError(f"Unknown operator: {operator}")
    return computed_values


def compute_all_columns_cephalopod(formatted_lines: list[str]) -> list[int]:
    result = []
    num_columns = len(formatted_lines)
    for col_id in range(num_columns):
        computed_value = compute_column_cephalopod(formatted_lines, col_id)
        result.append(computed_value)
    return result


if __name__ == "__main__":
    lines = read_file("input.txt")
    print(sum(compute_all_columns(format_lines(lines))))
    print(sum(compute_all_columns_cephalopod(format_cephalopod(lines))))
