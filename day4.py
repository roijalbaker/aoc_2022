def parse_file(fn):
    with open(fn, "r") as f:
        return [l.strip().split(",") for l in f.readlines()]


def to_ids(string):
    first, last = string.split("-")
    return set(range(int(first), int(last)+1))


def intersect(left, right):
    left_set = to_ids(left)
    right_set = to_ids(right)
    return left_set.issubset(right_set) or right_set.issubset(left_set)


if __name__ == "__main__":
    assignments = parse_file("day4_input1.txt")

    print(sum([intersect(*assignment) for assignment in assignments]))
