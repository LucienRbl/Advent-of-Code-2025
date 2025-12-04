#! /usr/bin/env python3


def read_file(file_path) -> list[str]:
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def find_max_joltage_with_n_batteries(batteries: str, n: int) -> int:
    s = batteries
    length = len(s)
    if n >= length:
        return int(s)

    result_digits: list[str] = []
    start = 0
    for i in range(n):
        last_index = length - (n - i)
        candidate_slice = s[start : last_index + 1]
        max_digit = max(candidate_slice)
        idx = s.index(max_digit, start, last_index + 1)
        result_digits.append(max_digit)
        start = idx + 1

    return int("".join(result_digits))


def sum_max_joltage_n_batteries(battery_lines: list[str], n: int) -> int:
    total = 0
    for battery_line in battery_lines:
        total += find_max_joltage_with_n_batteries(battery_line, n)
    return total


if __name__ == "__main__":
    print(sum_max_joltage_n_batteries(read_file("input.txt"), 2))
    print(sum_max_joltage_n_batteries(read_file("input.txt"), 12))
