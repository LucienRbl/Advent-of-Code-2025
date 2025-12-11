#! /usr/bin/env python3

EXAMPLE_INPUT = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return [tuple(map(int, line.strip().split(","))) for line in lines]


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.num_sets = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) 
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False 

        self.parent[root_y] = root_x
        
        self.num_sets -= 1
        return True


def distance(point1: tuple[int, int, int], point2: tuple[int, int, int]) -> int:
    return (
        (point1[0] - point2[0]) ** 2
        + (point1[1] - point2[1]) ** 2
        + (point1[2] - point2[2]) ** 2
    )


def size_of_largest_circuit(
    circuits_mapping: dict[int, list[tuple[int, int, int]]],
    number_of_circuits: int = 3,
) -> int:
    sorted_circuits = sorted(
        circuits_mapping.items(), key=lambda x: len(x[1]), reverse=True
    )
    largest_circuits = sorted_circuits[:number_of_circuits]
    size = 1
    for circuit in largest_circuits:
        size *= len(circuit[1])
    return size


def arrange_boxes_optimized(boxes, nb_of_pairs=-1):
    n = len(boxes)

    # Pre-compute all distances once
    print(f"Computing distances for {n} boxes...")
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            edges.append((dist, i, j, boxes[i], boxes[j]))

    edges.sort()

    uf = UnionFind(n)
    last_connected_boxes = ((), ())
    connections_made = 0

    if nb_of_pairs == -1:
        print("Merging all circuits until one remains...")
    else:
        print(f"Merging circuits until {nb_of_pairs} connections are made...")

    for dist, i, j, box_i, box_j in edges:
        connections_made += 1

        if uf.union(i, j):
            last_connected_boxes = (box_i, box_j)

            if connections_made >= nb_of_pairs and nb_of_pairs != -1:
                break

            if uf.num_sets == 1:
                break

    # Group boxes by circuit
    circuits_dict = {}
    for idx, box in enumerate(boxes):
        root = uf.find(idx)
        circuits_dict.setdefault(root, []).append(box)

    return circuits_dict, last_connected_boxes


if __name__ == "__main__":
    example_array = [
        tuple(map(int, line.strip().split(",")))
        for line in EXAMPLE_INPUT.strip().split("\n")
    ]
    input_array = read_file("input.txt")
    
    
    circuits_mapping, _ = arrange_boxes_optimized(input_array, 1000)
    print(f"Number of circuits: {len(circuits_mapping)}")
    print(
        f"Size of largest 3 circuits multiplied: {size_of_largest_circuit(circuits_mapping, 3)}"
    )
        
    print("\nArranging all boxes into a single circuit...")    
        
    circuits_mapping, last_connected_boxes = arrange_boxes_optimized(input_array)
    print(f"Last connected boxes: {last_connected_boxes}")
    print(f"X coordinates of last connected boxes multiplied: {last_connected_boxes[0][0] * last_connected_boxes[1][0]}")
