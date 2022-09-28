from statistics import mean, median
import sys

class Crabs():
    def __init__(self, positions):
        self.crab_positions = positions
        self.crab_positions.sort()

    def __repr__(self) -> str:
        return str(self.crab_positions)

    def get_fuel_consumption(self, horizontal_alignment):
        fuel_consumed = 0
        for pos in self.crab_positions:
            fuel_consumed += abs(pos - horizontal_alignment)

        return fuel_consumed
    
    def get_fuel_consumption_triangle(self, horizontal_alignment):
        fuel_consumed = 0
        for pos in self.crab_positions:
            places_moved = abs(pos - horizontal_alignment)
            fuel_consumed +=  int(places_moved*(places_moved+1)/2)

        return fuel_consumed

    def get_minimum_fuel_consumption(self):
        middle_crab = median(self.crab_positions)

        fuel_used = self.get_fuel_consumption(middle_crab)

        return middle_crab, fuel_used

    def get_minimum_fuel_consumption_triangle(self):
        lowest_pos = -1
        fuel_used = self.get_fuel_consumption_triangle(0)

        middle_crab = mean(self.crab_positions)
        for i in range(min(self.crab_positions), max(self.crab_positions) + 1):
            cur_fuel_used = self.get_fuel_consumption_triangle(i)
            if cur_fuel_used < fuel_used:
                fuel_used = cur_fuel_used
                lowest_pos = i

        return lowest_pos, fuel_used


if __name__ == "__main__":    
    with open('src/07.txt') as file:
        crab_positions = [int(i) for i in file.read().split(',')]

    crabs = Crabs(crab_positions)
    
    print(crabs)
    
    print(f' total part 1: {crabs.get_minimum_fuel_consumption()}')

    print(f' total part 2: {crabs.get_minimum_fuel_consumption_triangle()}')
