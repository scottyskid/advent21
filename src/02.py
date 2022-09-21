

class Move():
    def __init__(self, movement) -> None:
        direction, distance = movement.split(' ', 1) 
        distance = int(distance)
        self.x = 0
        self.y = 0

        if direction == 'forward':
            self.x = distance
        elif direction == 'up':
            self.y = -distance
        elif direction == 'down':
            self.y = distance


class Move_v2():
    def __init__(self, movement) -> None:
        direction, distance = movement.split(' ', 1) 
        distance = int(distance)
        self.x = 0
        self.y = 0
        self.aim = 0

        if direction == 'forward':
            self.x = distance
            self.y = distance
        elif direction == 'up':
            self.aim = -distance
        elif direction == 'down':
            self.aim = distance

class Sub():
    def __init__(self, x: int = 0, y: int = 0, aim: int = 0) -> None:
        self.x = x
        self.y = y
        self.aim = aim


    def move(self, move: Move):
        self.x += move.x
        self.y += move.y

    def move_v2(self, move: Move_v2):
        self.x += move.x
        self.y += move.y * self.aim
        self.aim += move.aim

    def calc_output(self):
        return self.x * self.y


if __name__ == "__main__":

    sub1 = Sub()
    sub2 = Sub()

    with open('src/02.txt') as file:
        for line in file:
            move = Move(line)
            sub1.move(move)

            move = Move_v2(line)
            sub2.move_v2(move)
            pass
    
    print(f'part 1 output: {sub1.calc_output()}')
    print(f'part 2 output: {sub2.calc_output()}')