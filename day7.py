from dataclasses import dataclass
from typing import List, Any
from typing_extensions import Self

@dataclass
class File:
    name: str
    _size: int

    def size(self, min_size=0):
        return self._size


@dataclass
class Dir:
    name: str
    parent: Any

    def __post_init__(self):
        self.dirs: List[Self] = []
        self.files: List[File] = []

    def append(self, obj):
        if isinstance(obj, Dir):
            self.dirs.append(obj)
        else:
            self.files.append(obj)

    def to(self, name) -> Self:
        if name == "..":
            return self.parent
        return next(dir for dir in self.dirs if dir.name == name)

    def size(self, max_size=float("inf")):
        size_dirs = sum([dir.size(max_size) for dir in self.dirs])
        size_files = sum([file.size(0) for file in self.files])

        size = size_dirs + size_files
        if size_files <= max_size:
            return size + size_dirs
        else:
            return size_dirs

    def __str__(self):
        return "\n".join(self.description(0))

    def description(self, i=0, max_size=float("inf")):
        descr = []
        descr.append('\t'*i + f"-{self.name} ({self.size(max_size)})")
        for dir in self.dirs:
            descr.extend(dir.description(i+1))
        for file in self.files:
            descr.append('\t'*(i + 1) + f"*{file.name} ({file.size(0)})")
        return descr


if __name__ == "__main__":
    main_dir = Dir("/", None)
    dir = main_dir
    with open("day7_test1.txt") as f:
        for line in f.readlines()[1:]:
            line = line.strip()

            if line == "$ ls":
                pass

            elif line.startswith("$ cd "):
                dir = dir.to(line.split(" ")[2])

            elif line.startswith("dir "):
                dir.append(Dir(line.split(" ")[1], parent=dir))

            else:
                size, name = line.split(" ")
                dir.append(File(name, int(size)))

    print(main_dir.size())
    print(main_dir.size(100_000))
