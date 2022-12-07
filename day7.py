FILE_SYSTEM_SIZE = 70000000
UPDATE_SIZE_REQUIRED = 30000000


class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files_size = 0
        self.children = list()

    @property
    def root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.root

    @property
    def total_size(self):
        total_size = 0
        for child in self.walk():
            total_size += child.files_size
        return total_size

    def add_child(self, _dir):
        self.children.append(_dir)

    def walk(self):
        if self.children:
            for child in self.children:
                yield from child.walk()
            yield self
        else:
            yield self

    def __repr__(self):
        return f"{directory.name}: {directory.total_size}"


if __name__ == "__main__":
    with open("inputs.txt") as inputs:
    # with open("test.txt") as inputs:
        cwd = None
        for line in inputs.readlines():
            line = line.rstrip("\n")
            if line.startswith("$ cd"):
                line = line[len("$ cd "):]
                if line == "..":
                    cwd = cwd.parent
                else:
                    new_cwd = Directory(name=line, parent=cwd)
                    try:
                        cwd.add_child(new_cwd)
                    except AttributeError:
                        pass
                    cwd = new_cwd

            elif line[0].isnumeric():
                size = ""
                for sign in line:
                    if sign == " ":
                        break
                    size += sign
                cwd.files_size += int(size)
    # part1
    sum1 = 0
    for directory in cwd.root.walk():
        if directory.total_size <= 100000:
            sum1 += directory.total_size
    print(sum1)

    # part2
    space_still_required = UPDATE_SIZE_REQUIRED - (FILE_SYSTEM_SIZE - cwd.root.total_size)

    to_delete = cwd.root.total_size
    for directory in cwd.root.walk():
        if directory.total_size >= space_still_required:
            if directory.total_size < to_delete:
                to_delete = directory.total_size
    print(to_delete)


