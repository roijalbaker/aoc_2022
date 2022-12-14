import re
import numpy as np


def line_to_path(line: str):
    path = r"(\d+,\d)"
    points = re.findall(path, line)
    points = [p.split(",") for p in points]
    points = [(int(a), int(b)) for a, b in points]
    return list(zip(points[:-1], points[1:]))


def parse_file(fn):
    paths = []
    with open(fn, "r") as f:
        for line in f.readlines():
            paths.extend(line_to_path(line))
    return paths


def rocks_to_map(rocks):
    y_max, x_max = np.array(rocks).max(axis=1).max(axis=0)
    blocked = np.array([[False] * (y_max+1)] * (x_max+1))
    for (start_x, start_y), (end_x, end_y) in rocks:
        if start_x == end_x:
            ys = range(start_y, end_y+1, 1) if end_y > start_y else range(end_y, start_y+1, 1)
            for y in ys:
                blocked[y, start_x] = True
        elif start_y == end_y:
            xs = range(start_x, end_x+1, 1) if end_x > start_x else range(end_x, start_x+1, 1)
            for x in xs:
                blocked[start_y, x] = True
        else:
            raise ValueError()
    return blocked


if __name__ == "__main__":
    rocks = parse_file("day14_test1.txt")
    print(rocks)
    rocks = rocks_to_map(rocks)
    print(rocks)
    np.savetxt("rocks.txt", rocks, fmt="%d")
    
    start = rocks.sum()

    print(rocks.sum()-start)
