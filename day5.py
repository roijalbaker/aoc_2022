import re
import numpy as np


def parse_file(fn):
    stack = []
    instructions = []
    with open(fn, "r") as f:
        for line in f.readlines():
            if "[" in line:
                stack.append([line[i+1] for i in range(0, len(line)-1, 4)])

    with open(fn, "r") as f:
        search = r"move (\d*) from (\d*) to (\d*)"
        instructions = re.findall(search, f.read())
        instructions = [[int(el) for el in inst] for inst in instructions]

    return stack, instructions


if __name__ == "__main__":
    stack, instructions = parse_file("day5_test1.txt")

    stack = np.array(stack)
    print(stack)

    empty_line = np.array([[' ']*stack.shape[0]])
    print(empty_line)

    for number, st_from, st_to in instructions:
        print(number, st_from, st_to)
        temp = []
        for _ in range(number):
            index, el = next(((i, el) for (i, el) in enumerate(stack[:, st_from-1]) if el != ' '))
            print(el)
            temp.append(el)
            stack[index, st_from-1] = ' '

        for el in temp:
            index = next((i for i, el in enumerate(stack[:, st_to-1]) if el != ' '), None)
            if index == 0:
                stack = np.concatenate((empty_line, stack), axis=0)
                index = 1
            elif index is None:
                index = stack.shape[1]+1
            print(index)
            stack[index-1, st_to-1] = el
    
        print(stack)
