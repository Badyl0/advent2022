example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def offset(letter):
    if ord(letter) > 96:
        return 96
    if ord(letter) < 91:
        return 38
    return None


def part1():
    with open("input.txt") as inputs:
        rucksacks = inputs.read().split("\n")
    sum1 = 0
    for rucksack in rucksacks:
        compartment1 = rucksack[:int(len(rucksack) / 2)]
        compartment2 = rucksack[int(len(rucksack) / 2):]
        item = [item for item in compartment1 if item in compartment2][0]
        value = item_value(item)
        sum1 += value
    print(sum1)


def item_value(item):
    value = ord(item) - offset(item)
    return value


class ElfGroupIterator:
    def __init__(self, rucksacks):
        self.rucksacks_iterator = iter(rucksacks)

    def __iter__(self):
        return self

    def __next__(self):
        return [next(self.rucksacks_iterator),
                next(self.rucksacks_iterator),
                next(self.rucksacks_iterator)]


def search_badge(elf_group):
    for item in elf_group[0]:
        if item in elf_group[1]:
            if item in elf_group[2]:
                return item


def part2():
    with open("input.txt") as inputs:
        elf_groups = ElfGroupIterator(inputs.read().split("\n"))
    sum1 = 0
    for elf_group in elf_groups:
        item = search_badge(elf_group)
        sum1 += item_value(item)
    print(sum1)


if __name__ == "__main__":
    # part1()
    part2()
