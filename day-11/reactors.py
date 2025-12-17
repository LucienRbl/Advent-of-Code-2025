#! /usr/bin/env python3
from functools import cache

EXAMPLE_INPUT_1 = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

EXAMPLE_INPUT_2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def parse_devices_lines(lines: list[str]) -> dict:
    devices = {}
    for line in lines:
        parts = line.split(": ")
        device_id = parts[0]
        reachable_ids = parts[1].split(" ") if len(parts) > 1 else []
        devices[device_id] = reachable_ids
    return devices | {"out": []}


@cache
def count_paths(current_device: str, target_device: str) -> int:
    if current_device == target_device:
        return 1
    else:
        return sum(
            count_paths(next_device, target_device)
            for next_device in devices[current_device]
        )


if __name__ == "__main__":
    lines = read_file("input.txt")
    # lines = EXAMPLE_INPUT_1.strip().split("\n")
    # lines = EXAMPLE_INPUT_2.strip().split("\n")

    devices = parse_devices_lines(lines)

    nb_path_you_out = count_paths("you", "out")
    print("Number of path from you to out:", nb_path_you_out)

    nb_paths_svr_dac = count_paths("svr", "dac")
    nb_path_dac_fft = count_paths("dac", "fft")
    nb_path_fft_out = count_paths("fft", "out")

    nb_path_svr_fft = count_paths("svr", "fft")
    nb_path_fft_dac = count_paths("fft", "dac")
    nb_path_dac_out = count_paths("dac", "out")

    nb_paths = (
        nb_paths_svr_dac * nb_path_dac_fft * nb_path_fft_out
        + nb_path_svr_fft * nb_path_fft_dac * nb_path_dac_out
    )
    print("Number of paths from svr to out passing by dac and fft:", nb_paths)
