def calc_score(trees_row):
    if len(trees_row)==0:
        print("hrer")
    if trees_row.count(trees_row[0]) > 1 or max(trees_row) != trees_row[0]:
        sum2 = 0
        for tree in trees_row[1:]:
            if tree < trees_row[0]:
                sum2 += 1
            if tree >= trees_row[0]:
                sum2 += 1
                return sum2
    if max(trees_row) == trees_row[0]:
        return len(trees_row) - 1
    return 1


if __name__ == "__main__":
    # with open("test.txt") as inputs:
    with open("inputs.txt") as inputs:
        trees = list()
        for line in inputs.readlines():
            trees.append(list(line.rstrip("\n")))

    # part1
    sum1 = 0
    # part2
    highest = 0
    for i, row in enumerate(trees):
        if i == 0 or i == len(trees)-1:
            continue
        for j, tree in enumerate(row):
            score = 1
            if j == 0 or j == len(row)-1:
                continue
            if max(row[:j+1]) == tree and row[:j+1].count(tree) == 1:
                sum1 += 1
            elif max(row[j:]) == tree and row[j:].count(tree) == 1:
                sum1 += 1
            elif max([tree[j] for tree in trees[:i+1]]) == tree and [tree[j] for tree in trees[:i+1]].count(tree) == 1:
                sum1 += 1
            elif max([tree[j] for tree in trees[i:]]) == tree and [tree[j] for tree in trees[i:]].count(tree) == 1:
                sum1 += 1
            # part2
            score *= calc_score(row[j::-1])
            score *= calc_score(row[j:])
            score *= calc_score([tree[j] for tree in trees[i::-1]])
            score *= calc_score([tree[j] for tree in trees[i:]])
            highest = max(highest, score)


    sum1 += (len(trees[0]) * 2) + (len(trees) * 2) - 4
    print(sum1)

    #part2
    print(highest)


