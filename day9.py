from adventofcode.libs.observer import Observer, Observable


class End:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.my_positions = [(0, 0)]

    def move_up(self):
        self.pos_y += 1

    def move_down(self):
        self.pos_y -= 1

    def move_right(self):
        self.pos_x += 1

    def move_left(self):
        self.pos_x -= 1


class Tail(End, Observer):
    def update(self, **state):
        dist = calc_distance(self, **state)
        if max(dist) > 1:
            self.keep_up(**state)
            self.add_position()

    def add_position(self):
        self.my_positions.append((self.pos_x, self.pos_y))

    def keep_up(self, **state):
        if self.pos_x == state["pos_x"]:
            if self.pos_y > state["pos_y"]:
                self.move_down()
            else:
                self.move_up()
        elif self.pos_y == state["pos_y"]:
            if self.pos_x > state["pos_x"]:
                self.move_left()
            else:
                self.move_right()
        elif self.pos_x < state["pos_x"]:
            self.move_right()
            if self.pos_y < state["pos_y"]:
                self.move_up()
            elif self.pos_y > state["pos_y"]:
                self.move_down()
        elif self.pos_x > state["pos_x"]:
            self.move_left()
            if self.pos_y < state["pos_y"]:
                self.move_up()
            elif self.pos_y > state["pos_y"]:
                self.move_down()



class Head(Observable, End):
    def __init__(self):
        Observable.__init__(self)
        End.__init__(self)

    def go(self, direction, step):
        for _ in range(0, step):
            match direction:
                case "U":
                    self.move_up()
                case "D":
                    self.move_down()
                case "R":
                    self.move_right()
                case "L":
                    self.move_left()
            self.notify()


class Knot(Observable, Tail):
    def __init__(self):
        Observable.__init__(self)
        Tail.__init__(self)

    def update(self, **state):
        Tail.update(self, **state)
        self.notify()


def calc_distance(tail, **head):
    x_dif = abs(tail.pos_x - head["pos_x"])
    y_dif = abs(tail.pos_y - head["pos_y"])
    return x_dif, y_dif



if __name__ == "__main__":
    with open("inputs.txt") as inputs:
    # with open("test.txt") as inputs:
        inputs = inputs.read()
    grid = list()
    head = Head()
    knots = [Knot() for _ in range(0, 8)]
    tail = Tail()
    head.attach(knots[0])
    for index, knot in enumerate(knots[:7]):
        knot.attach(knots[index + 1])
    knots[7].attach(tail)
    for line in inputs.split("\n"):
        direction, step = line.split(" ")
        head.go(direction, int(step))
    position_set = set(tail.my_positions)
    print(len(position_set))
