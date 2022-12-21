from typing import Dict
from sympy import parse_expr, solve


class Monkey:
    def __init__(self, name: str, value: str, part: str = "a"):
        self.name = name.strip()
        self.init_value = value.strip()
        self._value = None
        self.part = part

    def value(self, monkeys: Dict[str, "Monkey"]):   
        if self._value is None:
            try:
                if self.part == "b" and self.name == "humn":
                    self._value = "x"
                else:
                    self._value = int(self.init_value.strip())
            except Exception:
                left, *_, right = self.init_value.split(" ")
                left = monkeys[left]
                right = monkeys[right]
                calculate = (
                    (self.init_value.replace("+", "-") if self.part == "b" and self.name=="root" else self.init_value)
                    .replace(left.name, f"{left.value(monkeys)}")
                    .replace(right.name, f"{right.value(monkeys)}")
                )
                if "x" in calculate:
                    self._value = f"({calculate})"
                else:
                    self._value = int(eval(calculate))

        return self._value


def parse_file(fn, part: str = "a") -> Dict[str, Monkey]:
    monkeys = {}
    with open(fn, "r") as f:
        for line in f.readlines():
            monkey = Monkey(*line.split(":"), part=part)
            monkeys.update({monkey.name: monkey})
    return monkeys


if __name__ == "__main__":
    monkeys = parse_file("day21_input1.txt", "a")
    print(monkeys["root"].value(monkeys))

    monkeys = parse_file("day21_input1.txt", "b")
    sympy_eq = parse_expr(monkeys["root"].value(monkeys)[1:-1])
    print(solve(sympy_eq)[0])
