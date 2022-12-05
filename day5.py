from queue import LifoQueue

def stacks_parser(row):
    return row[1::len("] [A")]


if __name__ == "__main__":
    rows = list()
    with open("day5/inputs.txt") as inputs:
        for line in inputs.readlines():
            if line[1].isdigit() or line[0] == "\n":
                break
            rows.append(stacks_parser(line))

    lifos = [LifoQueue() for stack in rows[0]]

    for row in reversed(rows):
        for element, lifo in zip(row, lifos):
            if element != " ":
                lifo.put(element)

    with open("day5/inputs.txt") as inputs:
        for line in inputs.readlines():
            if "move" in line:
                # print(line)
                line = line.lstrip("move ")
                # print(line)
                count = int(line[:line.find(" ")])
                line = line[line.find(" "):].lstrip("from ")
                # print(line)
                from_stack = int(line[0]) - 1
                to_stack = int(line[1:].lstrip(" to ").rstrip("\n")) - 1
                # if count > 10:
                #     print(count)
                #     print(from_stack)
                #     print(to_stack)
                #     break
                items = list()
                while count:
                    count -= 1
                    items.append(lifos[from_stack].get())
                for item in reversed(items):
                    lifos[to_stack].put(item)

    out = ""
    for lifo in lifos:
        out += lifo.get()
    print(out)


