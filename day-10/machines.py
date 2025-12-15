#! /usr/bin/env python3
from functools import lru_cache
import re
from collections import deque
from itertools import combinations


EXAMPLE_INPUT = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def parse_machine_line(line: str) -> dict:
    parts = re.match(r"\[(.*?)\]\s+(.*?)\s+(\{.*?\})", line)
    if parts:
        lights_str = parts.group(1)
        lights = [1 if c == "#" else 0 for c in lights_str]
        buttons_str = parts.group(2)
        buttons = [
            tuple(map(int, b.strip("()").split(","))) for b in buttons_str.split()
        ]
        joltages_str = parts.group(3)
        joltages = list(map(int, joltages_str.strip("{}").split(",")))
        return {"lights": lights, "buttons": buttons, "joltages": joltages}
    return {}


def list_to_binary(lst: list[int]) -> int:
    return sum(bit << idx for idx, bit in enumerate(lst))


def binary_to_list(value: int, length: int) -> list[int]:
    return [(value >> bit) & 1 for bit in range(length)]


def build_graph_light(machine: dict) -> dict:
    graph = {}
    nb_lights = len(machine["lights"])
    nb_states = 2**nb_lights
    for i in range(nb_states):
        state_i = binary_to_list(i, nb_lights)
        graph[i] = []
        for j, button in enumerate(machine["buttons"]):
            new_state = state_i.copy()
            for light_index in button:
                new_state[light_index] ^= 1
            new_state_int = list_to_binary(new_state)
            graph[i].append(new_state_int)
    return graph


def find_shortest_path_light(machine: dict) -> list[int]:
    start = 0   
    graph = build_graph_light(machine)
    target = list_to_binary(machine["lights"])
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == target:
            return path
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return []


def get_patterns(buttons: list[tuple[int, ...]], target: tuple[int, ...]) -> dict[tuple[int, ...], int]:
    patterns = {}
    coeffs = [tuple(int(i in r) for i in range(len(target))) for r in buttons]
    num_buttons = len(coeffs)
    num_variables = len(coeffs[0])
    for pattern_len in range(num_buttons + 1):
        for buttons in combinations(range(num_buttons), pattern_len):
            pattern = tuple(
                map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons)))
            )
            if pattern not in patterns:
                patterns[pattern] = pattern_len
    return patterns


def find_shortest_path_joltage_size(machine: dict) -> list[int]:
    joltages = machine["joltages"]
    buttons = machine["buttons"]

    patterns_cost = get_patterns(buttons, tuple(joltages))

    @lru_cache(maxsize=None)
    def solve(target: tuple[int, ...]) -> int:
        if all(t == 0 for t in target):
            return 0
        result = float("inf")
        for pattern, cost in patterns_cost.items():
            if all(t1 <= t2 and t1 % 2 == t2 % 2 for t1, t2 in zip(pattern, target)):
                new_target = tuple((t2 - t1) // 2 for t1, t2 in zip(pattern, target))
                result = min(result, cost + 2 * solve(new_target))
        return result

    target = tuple(joltages)
    return solve(target)

if __name__ == "__main__":
    # Use real input
    machine_lines = read_file("input.txt")

    # Use example input
    # machine_lines = [line.strip() for line in EXAMPLE_INPUT.strip().split("\n")]

    print(f"Processing {len(machine_lines)} machine lines...")

    total_min_move_light = 0
    total_min_move_joltage = 0

    for line in machine_lines:
        machine = parse_machine_line(line)

        
        path_light = find_shortest_path_light(machine)
        min_moves_light = len(path_light) - 1
        print("Minimum moves (light):", min_moves_light)
        total_min_move_light += min_moves_light
        
        path_len = find_shortest_path_joltage_size(machine)
        print("Minimum moves (joltage):", path_len)
        total_min_move_joltage += path_len

    print("Total minimum moves for all machines:", total_min_move_light)
    print("Total minimum moves for all machines (joltage):", total_min_move_joltage)
