#! /usr/bin/env python3


def read_file(file_path) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    item_ids = []
    with open(file_path, "r") as file:
        line = file.readline()
        while line != "\n":
            line = line.strip()
            ranges.append(tuple(int(x) for x in line.split("-")))
            line = file.readline()
        for line in file.readlines():
            item_ids.append(int(line.strip()))
    return ranges, item_ids


def find_fresh_items(ranges: list[tuple[int, int]], item_ids: list[int]) -> list[int]:
    fresh_items = []
    for item in item_ids:
        is_fresh = False
        for rang in ranges:
            start, end = rang
            if start <= item <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_items.append(item)
    return fresh_items


def find_number_of_potential_fresh_items(ranges: list[tuple[int, int]]) -> int:
    intervals = sorted(ranges, key=lambda x: x[0], reverse=True)
    merged_intervals = []
    while intervals:
        current_start, current_end = intervals.pop()
        while intervals and intervals[-1][0] <= current_end + 1:
            next_start, next_end = intervals.pop()
            current_end = max(current_end, next_end)
        merged_intervals.append((current_start, current_end))
    total_count = 0
    for start, end in merged_intervals:
        total_count += end - start + 1
    return total_count


if __name__ == "__main__":
    ranges, item_ids = read_file("input.txt")
    print(len(find_fresh_items(ranges, item_ids)))
    print(find_number_of_potential_fresh_items(ranges))
