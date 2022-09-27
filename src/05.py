
class Vent():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.overlaps = 1
    
    def __repr__(self):
        return f'Vent(x:{self.x}, y:{self.y}, o:{self.overlaps})'

    def increase(self):
        self.overlaps += 1


class Line():
    def __init__(self, line_string):
        self.points = []
        start, end = line_string.split(' -> ', 1)

        self.start_x, self.start_y = [int(i) for i in start.split(',')]
        self.end_x, self.end_y = [int(i) for i in end.split(',')]

        self._populate()

    def __repr__(self):
        return f'Line({self.start_x}, {self.start_y}), ({self.end_x}, {self.end_y})'

    def _populate(self):
        if self.start_x < self.end_x:
            step_x = 1
        elif self.start_x > self.end_x:
            step_x = -1
        else:
            step_x = 0

        if self.start_y < self.end_y:
            step_y = 1
        elif self.start_y > self.end_y:
            step_y = -1
        else:
            step_y = 0

        distance = max(abs(self.end_x - self.start_x), abs(self.end_y - self.start_y))

        for i in range(distance + 1):
            self.points.append((self.start_x + i * step_x, self.start_y + i * step_y))


class Floor():
    def __init__(self, list_of_lines) -> None:
        self.vents = {}

        for line_string in list_of_lines:
            line = Line(line_string)
            for point in line.points:
                self.add_vent(*point)

    def __repr__(self):
        return str(self.vents)

    def add_vent(self, x, y):
        dict_key = f'{x,y}'
        if dict_key in self.vents:
            self.vents[dict_key].increase()
        else:
            self.vents[dict_key] = Vent(x, y)

        return self.vents[dict_key]

    def count_above_one(self):
        total = 0
        for vent in self.vents.values():
            if vent.overlaps > 1:
                total += 1
        return total

if __name__ == "__main__":
    with open('src/05.txt') as file:
        file_lines = file.read().split('\n')

    floor = Floor(file_lines)

    print(f'the total number above one is {floor.count_above_one()}')