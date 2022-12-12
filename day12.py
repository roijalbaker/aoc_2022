import networkx as nx


def to_ord(char):
    if char == "E":
        return ord("z") + 1
    if char == "S":
        return ord("a") - 1
    return ord(char)


def parse_file(fn):
    start = None
    end = None
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
                if diff in [1, 0]:
                    edges.append((right, node))
                if diff in [-1, 0]:
                    edges.append((node, right))
            if i < len(lines) - 1:
                down = f"{i+1}|{j}"
                char_down = lines[i+1][j]
                diff = to_ord(char) - to_ord(char_down)
                if diff in [1, 0]:
                    edges.append((down, node))
                if diff in [-1, 0]:
                    edges.append((node, down))

            if char == "E":
                end = node
            if char == "S":
                start = node

            G.add_edges_from(edges)
    return G, start, end


if __name__ == "__main__":
    G, start, end = parse_file("day12_input1.txt")
    path = nx.shortest_path(G, start, end)
    print(path)
    print(len(path) - 1)
