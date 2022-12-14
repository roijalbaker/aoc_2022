import re
import numpy as np


def line_to_path(line: str):
    path = r"(\d+,\d+)"
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


def rocks_to_map(rocks, b=False):
    x_max, y_max = np.array(rocks).max(axis=1).max(axis=0)
    blocked = np.array([[False] * (x_max+1000)] * (y_max+1))
    for (start_x, start_y), (end_x, end_y) in rocks:
        if (x := start_x) == end_x:
            ys = range(start_y, end_y+1, 1) if end_y > start_y else range(end_y, start_y+1, 1)
            for y in ys:
                blocked[y, x] = True
        elif (y := start_y) == end_y:
            xs = range(start_x, end_x+1, 1) if end_x > start_x else range(end_x, start_x+1, 1)
            for x in xs:
                blocked[y, x] = True
        else:
            raise ValueError()
    if b:
        blocked = np.concatenate((blocked, np.array([[False] * (x_max+1000)]), np.array([[True] * (x_max+1000)])), axis=0)
    return blocked


if __name__ == "__main__":
    rocks = parse_file("day14_input.txt")
    rocks = rocks_to_map(rocks, True)
    np.savetxt("rocks.txt", rocks, fmt="%d")

    start = rocks.sum()

    landed = True
    while landed:
        x = 500
        if rocks[0, 500]:  # part b
            break
        for y in range(rocks.shape[0]):

            if y+1 == rocks.shape[0]:
                landed = False
                break
            if rocks[y+1, x]:
                if rocks[y+1, x-1]:
                    if rocks[y+1, x+1]:
                        rocks[y, x] = True
                        break
                    else:
                        x += 1
                else:
                    x -= 1

    np.savetxt("end.txt", rocks, fmt="%d")
    print(rocks.sum()-start)
