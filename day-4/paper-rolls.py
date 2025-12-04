#! /usr/bin/env python3


EXAMPLE_INPUT = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def read_file(file_path) -> list[str]:
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def number_of_occupied_neighbors(
    paper_rolls: list[list[str]], row: int, col: int
) -> int:
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    occupied_count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(paper_rolls) and 0 <= c < len(paper_rolls[0]):
            if paper_rolls[r][c] == "@":
                occupied_count += 1
    return occupied_count


def find_accessible_paper_rolls(paper_rolls: list[list[str]]) -> list[(int, int)]:
    accessible_rolls = []
    for line_idx, line in enumerate(paper_rolls):
        for col_idx, cell in enumerate(line):
            if cell == "@":
                if number_of_occupied_neighbors(paper_rolls, line_idx, col_idx) < 4:
                    accessible_rolls.append((line_idx, col_idx))
    return accessible_rolls


def remove_paper_rolls(
    paper_rolls: list[list[str]], rolls_to_remove: list[(int, int)]
) -> None:
    for row, col in rolls_to_remove:
        paper_rolls[row][col] = "."


def operate_forklift(paper_rolls: list[list[str]]) -> int:
    number_of_removed_rolls = 0
    while True:
        rolls_to_remove = find_accessible_paper_rolls(paper_rolls)
        number_of_removed_rolls += len(rolls_to_remove)
        if not rolls_to_remove:
            break
        remove_paper_rolls(paper_rolls, rolls_to_remove)
    return number_of_removed_rolls


if __name__ == "__main__":
    print(len(find_accessible_paper_rolls(read_file("input.txt"))))
    print(operate_forklift(read_file("input.txt")))
