def parse_file(fn):
    with open(fn, "r") as f:
        return [l.strip() for l in f.readlines()]

def value(char):
    a = int.from_bytes(bytes("a", "utf8"), "big")
    A = int.from_bytes(bytes("A", "utf8"), "big")
    c = int.from_bytes(bytes(char, "utf8"), "big")

    if c < a:
        return c - A + 27
    
    return c - a + 1


if __name__ == "__main__":
    rugsacks = parse_file("day3_input1.txt")

    contents = [[sack[:int(len(sack)/2)], sack[-int(len(sack)/2):]] for sack in rugsacks]
    in_common = [list(set(sack[0]).intersection(set(sack[1])))[0] for sack in contents]
    print(sum([value(x) for x in in_common]))

    groups = [rugsacks[i:i+3] for i in range(0, len(rugsacks), 3)]
    badges = [list(set(sack[0]).intersection(set(sack[1])).intersection(set(sack[2])))[0] for sack in groups]
    print(sum([value(x) for x in badges]))
