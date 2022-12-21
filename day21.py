from typing import Dict


class Monkey:
    def __init__(self, name: str, value: str):
        self.name = name.strip()
        self.init_value = value.strip()
        self._value = None

    def value(self, monkeys: Dict[str, "Monkey"]):
        if self._value is None:
            try:
                self._value = int(self.init_value.strip())
            except Exception:
                left, *_, right = self.init_value.split(" ")
                left = monkeys[left]
                right = monkeys[right]
                calculate = (
                    self.init_value
                    .replace(left.name, f"{left.value(monkeys)}")
                    .replace(right.name, f"{right.value(monkeys)}")
                )
                self._value = eval(calculate)

        return self._value


def parse_file(fn) -> Dict[str, Monkey]:
    monkeys = {}
    with open(fn, "r") as f:
        for line in f.readlines():
            monkey = Monkey(*line.split(":"))
            monkeys.update({monkey.name: monkey})
    return monkeys


if __name__ == "__main__":
    monkeys = parse_file("day21_test1.txt")
    print(monkeys["root"].value(monkeys))
