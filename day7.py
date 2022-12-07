from dataclasses import dataclass
from typing import List
from typing_extensions import Self


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str
    parent: Self

    def __post_init__(self):
        self.dirs: List[Self] = []
        self.files: List[File] = []
        self._size: int = None

    def append(self, obj):
        if isinstance(obj, Dir):
            self.dirs.append(obj)
        else:
            self.files.append(obj)
        self._size = None

    def to(self, name) -> Self:
        if name == "..":
            return self.parent
        return next(dir for dir in self.dirs if dir.name == name)

    @property
    def size(self):
        if self._size is None:
            self._size = sum([dir.size for dir in self.dirs])
            self._size += sum([file.size for file in self.files])

        return self._size

    def __str__(self):
        return "\n".join(self.description(0))

    def description(self, indent=0):
        descr = []
        descr.append('\t'*indent + f"-{self.name} ({self.size})")
        for dir in self.dirs:
            descr.extend(dir.description(indent+1))
        for file in self.files:
            descr.append('\t'*(indent + 1) + f"*{file.name} ({file.size})")
        return descr


if __name__ == "__main__":
    main_dir = Dir("/", None)
    dir = main_dir

    # keep separate list with all directories
    all_dirs: List[Dir] = []

    with open("day7_input1.txt") as f:
        for line in f.readlines()[1:]:
            line = line.strip()

            if line == "$ ls":
                pass

            elif line.startswith("$ cd "):
                dir = dir.to(line.split(" ")[2])

            elif line.startswith("dir "):
                dir.append(Dir(line.split(" ")[1], parent=dir))
                all_dirs.append(dir.dirs[-1])

            else:
                size, name = line.split(" ")
                dir.append(File(name, int(size)))

    sizes = [dir.size for dir in all_dirs]
    print("a", sum([s for s in sizes if s <= 100_000]))

    # Part b
    total_space = 70_000_000
    needed = 30_000_000
    to_find = needed - (total_space - main_dir.size)

    all_dirs.sort(key=lambda dir: dir.size)
    print("b", next(dir for dir in all_dirs if dir.size >= to_find).size)
