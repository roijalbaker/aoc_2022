class Head:
    def __init__(self) -> None:
        self.position = [0, 0]
        self.visited = [self.position.copy()]

    def move(self, dir):
        if dir == "R":
            self.position[0] += 1
        if dir == "U":
            self.position[1] += 1
        if dir == "L":
            self.position[0] -= 1
        if dir == "D":
            self.position[1] -= 1
        self.visited.append(self.position.copy())


class Tail(Head):
    def move(self, head, previous_head):
        diag = self.position[0] != head[0] and self.position[1] != head[1]
        if diag and ((abs(self.position[0] - head[0] > 1)) or (abs(self.position[1] - head[1]) > 1)):
            self.position = previous_head
        elif self.position[0] < head[0] - 1:
            self.position[0] += 1
        elif self.position[0] > head[0] + 1:
            self.position[0] -= 1
        elif self.position[1] < head[1] - 1:
            self.position[1] += 1
        elif self.position[1] > head[1] + 1:
            self.position[1] -= 1
        self.visited.append(self.position.copy())


if __name__ == "__main__":
    head = Head()
    tail = Tail()
    with open("day9_test1.txt") as f:
        for line in f.readlines():
            dir, num = line.strip().split(" ")
            for _ in range(int(num)):
                head.move(dir)
                tail.move(head.visited[-1], head.visited[-2])
                print(dir, num, head.position, tail.position)
    start = next(i for i, pos in enumerate(tail.visited) if pos != [0, 0])
    print(len(set([f"{x}-{y}" for x, y in tail.visited[start:]])))
