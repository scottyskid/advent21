
from math import sqrt
import re


class Probe():
    def __init__(self, *, x_pos=0, y_pos=0, x_velocity=0, y_velocity=0) -> None:
        self.x_pos_start = x_pos
        self.y_pos_start = y_pos
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.current_step = 0


    def set_velocity(self, x_velocity, y_velocity):
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def step(self):
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

        self.y_velocity -= 1

    
    
    def hit_target(self, x_pos, y_pos):
        # x and y velocities are tracked separately 
        # x can just be the closest triangular number between the start location and target
        # y will always land exacly on the same starting location just increase triangular numebrs from the starting y veloicy
        # then loop through all variations of y 
        pass


class Target():
    def __init__(self, target_rep):
        pattern = re.compile(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)$')
        found = [int(i) for i in re.findall(pattern, target_rep)[0]]
        self.x_min, self.x_max, self.y_min, self.y_max = found
        


def get_triangular_number(n):
    return int(abs(n) * (abs(n) + 1) / 2)

def get_triangular_root(n):
    return (sqrt((8 * abs(n)) + 1) - 1) / 2

def is_triangular_number(n):
    return get_triangular_root(n).is_integer()


if __name__ == "__main__":    
    with open('src/17.txt') as file:
        input_val = file.readline()

    target = Target(input_val)

    print(get_triangular_number(175))