import networkx as nx


def to_ord(char):
    if char == "E":
        return ord("z")
    if char == "S":
        return ord("a")
    return ord(char)


def parse_file(fn):
    start = []
    end = None
    s = None
    G = nx.DiGraph()
    with open(fn, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            edges = []
            node = f"{i}|{j}"
            if j < len(line) - 1:
                right = f"{i}|{j+1}"
                char_right = lines[i][j+1]
                diff = to_ord(char) - to_ord(char_right)
                if diff <= 1:
                    edges.append((right, node))
                if diff in [-1, 0]:
                    edges.append((node, right))
            if i < len(lines) - 1:
                down = f"{i+1}|{j}"
                char_down = lines[i+1][j]
                diff = to_ord(char) - to_ord(char_down)
                if diff <= 1:
                    edges.append((down, node))
                if diff in [-1, 0]:
                    edges.append((node, down))

            if char == "E":
                end = node
            if char == "S":
                s = node
            if char in ["S", "a"]:
                start.append(node)
            G.add_edges_from(edges)
    return G, s, start, end


def export(fn, path):
    with open(fn, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    with open("path.txt", "w") as f:
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                node = f"{i}|{j}"
                f.write(char if node in path else ".")
            f.write("\n")


if __name__ == "__main__":
    fn = "day12_input1.txt"
    G, start, starts, end = parse_file(fn)
    print(len(nx.shortest_path(G, start, end)) - 1)
    paths = []
    for start in starts:
        try:
            path = nx.shortest_path(G, start, end)
            paths.append(len(path) - 1)
        except:
            pass
    print(min(paths))
