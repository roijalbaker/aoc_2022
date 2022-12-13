def parse_file(fn):
    pairs = []
    left = None
    right = None
    with open(fn, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                pairs.append((left, right))
                left, right = None, None
                continue
            if left is None:
                left = eval(line)
            elif right is None:
                right = eval(line)
            else:
                raise ValueError()
        pairs.append((left, right))
    return pairs


def compare(left, right):
    print(left, right)
    # print(left, right)
    # integer comparison
    if isinstance(left, int) and isinstance(right, int):
        return left <= right

    # list comparison
    if isinstance(left, list) and isinstance(right, list):
        i = 0
        for i, r in enumerate(right):
            if i == len(left):  # pair 4 example
                return True
            result = compare(left[i], r)
            if result is False:
                return result
            if result is True and i == len(right) - 1:
                return len(left) - 1 >= i

        return True

    # list casting
    new_left, new_right = None, None
    if isinstance(left, int):
        new_left = [left]
    if isinstance(right, int):
        new_right = [right]

    return compare(new_left or left, new_right or right)


if __name__ == "__main__":
    pairs = parse_file("day13_test1.txt")
    indices = []
    for i, pair in enumerate(pairs):
        result = compare(*pair)
        print(i+1, result)
        if result:
            indices.append(i+1)
    print(indices)
    print(sum(indices))
