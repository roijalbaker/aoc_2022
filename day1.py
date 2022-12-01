def day1(filename: str):
    with open(filename) as file:
        elves = []
        elf = []
        for line in file.readlines():
            if line == "\n":
                elves.append(elf)
                elf = []
            else:
                elf.append(int(line[:-1]))

        print(
            max([sum(elf) for elf in elves])
        )


if __name__ == "__main__":
    day1("day1_input1.txt")
