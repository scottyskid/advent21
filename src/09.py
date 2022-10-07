

from math import prod
from typing import OrderedDict


class Point():
    def __init__(self, x, y, height) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.adjacent_points = []

    def __repr__(self) -> str:
        return f'Point(x={self.x}, y={self.y}, h={self.height})'

    def is_low_point(self) -> bool:
        for p in self.adjacent_points:
            if self.height >= p.height:
                return False
        return True

    def get_risk_level(self):
        return self.height + 1


class Basin():
    def __init__(self, low_point: Point) -> None:
        self.low_point = low_point

        self.contained_points = [self.low_point]

        for point in self.contained_points:
            for adjacent_point in point.adjacent_points:
                if adjacent_point not in self.contained_points and adjacent_point.height < 9:
                    self.contained_points.append(adjacent_point)
        
    def get_size(self):
        return len(self.contained_points)

        

class SeaFloor():
    def __init__(self, height_map) -> None:
        point_values = height_map.split('\n')

        self.x_length = len(point_values[0])
        self.y_width = len(point_values)

        self.points = {}

        for y in range(self.y_width):
            for x in range(self.x_length):
                self.points[(x, y)] = Point(x, y, int(point_values[y][x]))

        # add adjacent_points
        for key, cur_point in self.points.items():
            cur_x, cur_y = key

            if cur_x > 0:
                cur_point.adjacent_points.append(self.points[(cur_x - 1, cur_y)])
            if cur_x < self.x_length - 1:
                cur_point.adjacent_points.append(self.points[(cur_x + 1, cur_y)])
            if cur_y > 0:
                cur_point.adjacent_points.append(self.points[(cur_x, cur_y - 1)])
            if cur_y < self.y_width - 1:
                cur_point.adjacent_points.append(self.points[(cur_x, cur_y + 1)])

        self.basins = []

        for point in self.points.values():
            if point.is_low_point():
                self.basins.append(Basin(point))


    def __repr__(self) -> str:
        repr_str = 'SeaFloor:\n'
        for y in range(self.y_width):
            for x in range(self.x_length):
                repr_str += f'{self.points[(x, y)].height}'
            repr_str += '\n'

        return repr_str

    def get_low_point_risk_levels(self) -> int:
        risk_levels_sum = 0
        for point in self.points.values():
            if point.is_low_point():
                risk_levels_sum += point.get_risk_level()
                # print(f'{point} is a adjacent to {point.adjacent_points}')
        return risk_levels_sum

    def get_largest_basins(self, x_largest=3):
        orderd_basins = sorted(self.basins, key=lambda x: x.get_size(), reverse=True)

        return orderd_basins[:x_largest]

    def get_part_2_answer(self):
        largest_basins = self.get_largest_basins(3)

        total = prod([i.get_size() for i in largest_basins])

        return total




if __name__ == "__main__":    
    with open('src/09.txt') as file:
        height_map = file.read()
    
    sea_floor = SeaFloor(height_map)
    print(f'part 1 total risk level: {sea_floor.get_low_point_risk_levels()}')

    print(f'part 2 get lowest basins: {sea_floor.get_part_2_answer()}')


