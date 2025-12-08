#! /usr/bin/env python3

EXAMPLE_INPUT = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


def read_file(file_path):
    with open(file_path, "r") as file:
        return [line.rstrip("\n") for line in file.readlines()]


def print_diagram(diagram: list[str]) -> None:
    for line in diagram:
        print("".join(line))


def move_beams_one_step(
    diagram: list[str], step: int, beams_n: list[int]
) -> tuple[list[str], int, list[int]]:
    height = len(diagram)
    width = len(diagram[0])
    new_diagram = [list(row) for row in diagram]

    beams_n_next = [0] * width

    nb_of_split_beams = 0
    if step >= height:
        return new_diagram, nb_of_split_beams, beams_n_next
    y = step

    for x in range(width):
        if diagram[y][x] == "S":
            if y + 1 < height:
                new_diagram[y + 1][x] = "|"
                beams_n_next[x] = 1  # beam from S

        elif diagram[y][x] == "|" and beams_n[x] > 0:
            if y + 1 < height and diagram[y + 1][x] == "^":
                nb_of_split_beams += 1

                # left beam
                if x - 1 >= 0:
                    beams_n_next[x - 1] += beams_n[x]
                    new_diagram[y + 1][x - 1] = "|"

                # right beam
                if x + 1 < width:
                    beams_n_next[x + 1] += beams_n[x]
                    new_diagram[y + 1][x + 1] = "|"

            else:
                if y + 1 < height:
                    new_diagram[y + 1][x] = "|"
                    beams_n_next[x] += beams_n[x]

    return new_diagram, nb_of_split_beams, beams_n_next


def compute_diagram(diagram: list[str]) -> tuple[list[str], int, list[int]]:
    new_diagram = diagram
    nb_of_split_beams = 0
    step = 0
    height = len(diagram)
    width = len(diagram[0]) if height > 0 else 0
    beams_n = [0 for _ in range(width)]
    for step in range(height - 1): # last line cannot create new beams
        updated_diagram, nb_of_split_beams_step, beams_n_1 = move_beams_one_step(
            new_diagram, step, beams_n
        )
        new_diagram = updated_diagram
        nb_of_split_beams += nb_of_split_beams_step
        beams_n = beams_n_1
    return new_diagram, nb_of_split_beams, beams_n


if __name__ == "__main__":
    lines = read_file("input.txt")
    new_diagram, nb_of_split_beams, nb_of_beams_by_coord = compute_diagram(
        lines
    )
    print(f"Number of split beams: {nb_of_split_beams}")
    print(f"Number of potential beams paths: {sum(nb_of_beams_by_coord)}")
