#! /usr/bin/env python3


def read_file(file_path) -> list[tuple[int, int]]:
    with open(file_path, "r") as file:
        line = file.readline()
        ranges = line.strip().split(",")
        return [(int(r.split("-")[0]), int(r.split("-")[1])) for r in ranges]


def find_invalid_ids(ranges: list[tuple[int, int]]) -> list[int]:
    invalid_ids = []
    for rang in ranges:
        start, end = rang
        for id in range(start, end + 1):
            if is_invalid_id(id):
                invalid_ids.append(id)
    return invalid_ids


def sum_invalid_ids(invalid_ids: list[int]) -> int:
    return sum(invalid_ids)


def is_invalid_id(id: int) -> bool:
    def has_repetition(id: str, pattern_len: int) -> bool:
        pattern = id[:pattern_len]
        for i in range(pattern_len, len(id), pattern_len):
            if id[i : i + pattern_len] != pattern:
                return False
        return True

    id_str = str(id)
    for pattern_len in range(1, len(id_str) // 2 + 1):
        if has_repetition(id_str, pattern_len):
            return True
    return False


if __name__ == "__main__":
    print(sum_invalid_ids(find_invalid_ids(read_file("input.txt"))))
