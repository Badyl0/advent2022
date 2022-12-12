if __name__ == "__main__":
    register = 1
    cycle = 0
    # with open("test.txt") as inputs:
    with open("inputs.txt") as inputs:
        read_line = iter(inputs)
        line = next(read_line)
        while 1:
            if cycle > 39:
                cycle -= 40
            if cycle in [register - 1, register, register + 1]:
                print("#", end="")
            else:
                print(".", end="")
            if cycle in [39]:
                print()
            if line.startswith("noop"):
                line = next(read_line)
                cycle += 1
            elif line.startswith("addx "):
                line = int(line.rstrip("\n").lstrip("addx "))
                cycle += 1
                if cycle in [register - 1, register, register + 1]:
                    print("#", end="")
                else:
                    print(".", end="")
                if cycle in [39]:
                    print()
                cycle += 1
                register += line
                line = next(read_line)


