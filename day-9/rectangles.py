#! /usr/bin/env python3

EXAMPLE_INPUT = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""



def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return [tuple(map(int, line.strip().split(","))) for line in lines]


def area_of_rectangle(corner1: tuple[int, int], corner2: tuple[int, int]) -> int:
    length = abs(corner2[0] - corner1[0]) + 1
    width = abs(corner2[1] - corner1[1]) + 1

    return length * width


def find_largest_rectangle_with_2_red_corners(red_tiles: list[tuple[int, int]]) -> int:
    max_area = 0
    n = len(red_tiles)

    for i in range(n):
        for j in range(i + 1, n):
            corner1 = red_tiles[i]
            corner2 = red_tiles[j]

            area = area_of_rectangle(corner1, corner2)
            if area >= max_area:
                max_area = area

    return max_area


def find_largest_rectangle_with_2_red_corners_and_green_tiles(
    red_tiles: list[tuple[int, int]],
) -> tuple[int, list[tuple[int, int]]]:
    green_edges = get_green_edges(red_tiles)
    max_area = 0
    n = len(red_tiles)
    
    for i in range(n):
        for j in range(i + 1, n):
            corner1 = red_tiles[i]
            corner2 = red_tiles[j]
            area = area_of_rectangle(corner1, corner2)
            if area < max_area:
                continue
            if not intersect_with_edges(corner1, corner2, green_edges):
                max_area = area
                    
    return max_area


def get_green_edges(red_tiles: list[tuple[int, int]]) -> list[tuple[tuple[int, int]]]:
    n = len(red_tiles)
    edges = []

    for i in range(n):
        _from = red_tiles[i]
        _to = red_tiles[(i + 1) % n]
        edges.append((_from, _to))


    return edges

def intersect_with_edges(tile1: tuple[int, int], tile2: tuple[int, int], edges: list[tuple[tuple[int, int]]]) -> bool:
    min_x, max_x = sorted([tile1[0], tile2[0]])
    min_y, max_y = sorted([tile1[1], tile2[1]])
    for edge in edges:
        edge_from, edge_to = edge
        min_edge_x, max_edge_x = sorted([edge_from[0], edge_to[0]])
        min_edge_y, max_edge_y = sorted([edge_from[1], edge_to[1]])
        if min_x < max_edge_x and max_x > min_edge_x and min_y < max_edge_y and max_y > min_edge_y:
            return True
    return False


if __name__ == "__main__":
    # Use real input
    tiles = read_file("input.txt")
    
    # Use example input
    # tiles = [
    #     tuple(map(int, line.strip().split(",")))
    #     for line in EXAMPLE_INPUT.strip().split("\n")
    # ]
    
    print(f"Processing {len(tiles)} tiles...")
    
    max_area_2_red_corners = find_largest_rectangle_with_2_red_corners(tiles)
    print("Largest rectangle area with 2 red corners:", max_area_2_red_corners)

    max_area_2_red_corners_green_edges = (
        find_largest_rectangle_with_2_red_corners_and_green_tiles(tiles)
    )
    print(
        "Largest rectangle area with 2 red corners and green tiles on edges:",
        max_area_2_red_corners_green_edges,
    )
    