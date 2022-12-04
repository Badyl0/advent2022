def part1():
    with open("inputs.txt") as inputs:
        sum1 = 0
        for line in inputs.readlines():
            a, b = line.split(",")
            a = a.split("-")
            b = b.strip("\n").split("-")
            a_list = list(range(int(a[0]), int(a[1]) + 1))
            b_list = list(range(int(b[0]), int(b[1]) + 1))
            if overlaps(a_list, b_list):
                sum1 += 1
            elif overlaps(b_list, a_list):
                sum1 += 1
        print(sum1)


def contains(list1, list2):
    return all(item if item in list2 else None for item in list1)


def overlaps(list1, list2):
    return any(item if item in list2 else None for item in list1)


if __name__ == "__main__":
    part1()