import cProfile
import re
from pprint import pprint
from itertools import combinations


class Coordinate():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'{self.coords}'

    def __repr__(self) -> str:
        return f'{self.coords}'

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError('Invalid type')

    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError('Invalid type')

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    @property
    def coords(self):
        return (self.x, self.y, self.z)

    @coords.setter
    def coords(self, value):
        self.x, self.y, self.z = value

    def get_manhattan_distance(self, other):
        if isinstance(other, Coordinate):
            return sum(abs(point_1 - point_2) for point_1, point_2 in zip(self.coords, other.coords))
        else:
            raise ValueError('not a valid type')

    def pitch(self, centre=None, inplace=False, invert=False):
        if centre is None:
            centre = Coordinate(0, 0, 0)

        modifier = -1 if invert else 1

        new_coord = self - centre
        new_coord.coords = (new_coord.x, modifier * new_coord.z, modifier * -new_coord.y)
        new_coord += centre

        if inplace:
            self.coords = new_coord.coords
        else:
            return new_coord

    def roll(self, centre=None, inplace=False, invert=False):
        if centre is None:
            centre = Coordinate(0, 0, 0)

        modifier = -1 if invert else 1

        new_coord = self - centre
        new_coord.coords = (modifier * -new_coord.y, modifier * new_coord.x, new_coord.z)
        new_coord += centre

        if inplace:
            self.coords = new_coord.coords
        else:
            return new_coord

    def yaw(self, centre=None, inplace=False, invert=False):
        if centre is None:
            centre = Coordinate(0, 0, 0)

        modifier = -1 if invert else 1

        new_coord = self - centre
        new_coord.coords = (modifier * -new_coord.z, new_coord.y, modifier * new_coord.x)
        new_coord += centre

        if inplace:
            self.coords = new_coord.coords
        else:
            return new_coord

    def modify_relitive_origin(self, current_origin=None, new_origin=None):
        if new_origin is None:
            new_origin = Coordinate(0, 0, 0)
        if current_origin is None:
            current_origin = Coordinate(0, 0, 0)
        
        return self + current_origin - new_origin


class Beacon():
    def __init__(self, coords) -> None:
        if isinstance(coords, Coordinate):
            self.coords = coords
        else:
            self.coords = Coordinate(*coords)

    def __str__(self) -> str:
        return f'{self.coords}'
    
    def __repr__(self) -> str:
        return f'{self.coords}'

    def __hash__(self) -> int:
        return hash(f'{self.coords.x},{self.coords.y},{self.coords.z}')

    def __eq__(self, other) -> bool:
        is_equal = self.coords.x == other.coords.x
        is_equal = is_equal and self.coords.y == other.coords.y
        is_equal = is_equal and self.coords.z == other.coords.z

        return is_equal

    def get_distance(self, other, manhattan=False):
        if isinstance(other, Beacon):
            if manhattan:
                return self.coords.get_manhattan_distance(other.coords)
            else:
                return self.coords - other.coords
        else:
            raise ValueError('not a valid type')

    def get_distances(self, other_objects: list, manhattan=False):
        distance_list = {}
        for other_beacon in other_objects:
            distance_list[other_beacon] = self.get_distance(other_beacon, manhattan)

        return distance_list

    def pitch(self, invert=False):
        self.coords = self.coords.pitch(invert=invert)
    
    def roll(self, invert=False):
        self.coords = self.coords.roll(invert=invert)

    def yaw(self, invert=False):
        self.coords = self.coords.roll(invert=invert)


class Scanner():
    def __init__(self, beacon_coords):

        self.beacons = []
        for beacon in beacon_coords:
            self.beacons.append(Beacon(beacon))


    def __str__(self) -> str:
        return f'S()'

    def get_distance_matrix(self, manhattan=False):
        distance_matrix = {}
        for beacon in self.beacons:
            distance_matrix[beacon] = beacon.get_distances(self.beacons, manhattan)

        return distance_matrix

    def get_max_number_equal_distances(self, other, manhattan=False) -> int:
        max_distances = 0
        highest_beacon_self = None
        highest_beacon_other = None

        self_distance_matrix = self.get_distance_matrix(manhattan)
        other_distance_matrix = other.get_distance_matrix(manhattan)

        for beacon_self, distances_self in self_distance_matrix.items():
            for beacon_other, distances_other in other_distance_matrix.items():
                total_matching = len(list(set(distances_self.values()).intersection(distances_other.values())))
                if total_matching >= 12:
                    max_distances = total_matching
                    highest_beacon_self = beacon_self
                    highest_beacon_other = beacon_other
 
        return max_distances, highest_beacon_self, highest_beacon_other


class ScrodingerScanner(Scanner):
    def __init__(self, scanner_id, beacon_coords):
        super().__init__(beacon_coords)
        self.scanner_id = scanner_id

        self.orientation_sequence = self.create_orientation_sequence()
        self.orientation_step_count = 0


    def pitch(self, invert=False):
        for beacon in self.beacons:
            beacon.pitch(invert=invert)

            # for distance_coords in self.distance_matrix.values():
            #     for coord in distance_coords:
            #         coord.pitch(invert=invert)

    def roll(self, invert=False):
        for beacon in self.beacons:
            beacon.roll(invert=invert)

            # for distance_coords in self.distance_matrix.values():
            #     for coord in distance_coords:
            #         coord.roll(invert=invert)

    def yaw(self, invert=False):
        for beacon in self.beacons:
            beacon.yaw(invert=invert)

            # for distance_coords in self.distance_matrix.values():
            #     for coord in distance_coords:
            #         coord.yaw(invert=invert)

    def create_orientation_sequence(self):
        # https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
        sequence = []
        for cycle in range(2):
            for step in range(3): 
                for i in range(3): 
                    sequence.append([self.roll])
                if step < 2:
                    sequence.append([self.pitch])
                else:
                    sequence.append([self.pitch, self.pitch, self.roll, self.pitch])

        return sequence

    def step_orientation(self):
        self.orientation_step_count = (1 + self.orientation_step_count) % len(self.orientation_sequence)

        current_step = self.orientation_sequence.pop(0)

        for func in current_step:
            func()
        
        self.orientation_sequence.append(current_step)


# concrete beacon list
class Cavern(Scanner):
    def __init__(self, beacons) -> None:
        super().__init__(beacons)
        self.origin = Coordinate(0, 0, 0)

        self.distance_matrix = super().get_distance_matrix()
        self.distance_matrix_manhattan = super().get_distance_matrix(manhattan=True)
        self.scanners = {0: Coordinate(0, 0, 0)}


    def __len__(self):
        return len(self.beacons)

    def get_distance_matrix(self, manhattan=False):
        if manhattan:
            return self.distance_matrix_manhattan
        else:
            return self.distance_matrix
    

    def check_scanner_intergration(self, scanner):

        total_matching_needed = 12
        if isinstance(scanner, ScrodingerScanner):
            # todo add initial check for matching distances of any orientation (manhattan maybe)
            total_matching, self_beacon, other_beacon = self.get_max_number_equal_distances(scanner, manhattan=True)
            if total_matching < total_matching_needed:
                return None, None
            for _ in range(24):
                total_matching, self_beacon, other_beacon = self.get_max_number_equal_distances(scanner)
                if total_matching >= total_matching_needed:
                    scanner_coords = self_beacon.coords - other_beacon.coords
                    return total_matching, scanner_coords
                scanner.step_orientation()
        else:
            raise TypeError()

        return None, None

    def add_beacons_from_scanner(self, scanner, scanner_coords):
        current_coords = [i.coords for i in self.beacons]

        for scanner_beacon in scanner.beacons:
            actual_location = scanner_beacon.coords.modify_relitive_origin(scanner_coords)
            if actual_location not in current_coords:
                self.beacons.append(Beacon(actual_location))
            else:
                print(f'existing beacon at {actual_location=}')

        self.distance_matrix = super().get_distance_matrix()
        self.distance_matrix_manhattan = super().get_distance_matrix(manhattan=True)

        self.scanners[scanner.scanner_id] = scanner_coords

    def get_furthest_scanners(self):
        largest_distance = 0
        for a, b in combinations(self.scanners.values(), 2):
            distance = a.get_manhattan_distance(b)
            if distance > largest_distance:
                largest_distance = distance

        return largest_distance




if __name__ == "__main__":    
    with open('src/19.txt' ,mode='r') as file:
        input_val = file.read().strip()

    scanners_config_val = {}
    for scanner_text in input_val.split('\n\n'):
        line_split = scanner_text.split('\n')
        scanner_id_val = int(re.findall( r'--- scanner (\d+) ---', line_split[0])[0])
        
        scanners_config_val[scanner_id_val] = []
        for beacon_text in line_split[1:]:
            scanners_config_val[scanner_id_val].append(tuple([int(i) for i in beacon_text.strip().split(',')]))

    del input_val
    
    # create scanners
    cavern = Cavern(scanners_config_val[0])
    del scanners_config_val[0]

    limbo_scanners = []
    for scanner_id, coords in scanners_config_val.items():
        limbo_scanners.append(ScrodingerScanner(scanner_id, coords))


    # map the beacons
    while len(limbo_scanners) > 0:
        found_scanner = -1
        for i, scanner in enumerate(limbo_scanners):
            total_matches, scanner_location = cavern.check_scanner_intergration(scanner)
            if total_matches is not None:
                print(f'matched_scanner {scanner.scanner_id} with {total_matches=} and {scanner_location=}')

                cavern.add_beacons_from_scanner(scanner, scanner_location)
                found_scanner = i
                break

        if found_scanner < 0:
            raise ValueError("No matching scanner found")
        else:
            del limbo_scanners[found_scanner]

    print(f'total number of beacons is {len(cavern)}')

    print(f' part 2 answer {cavern.get_furthest_scanners()}')


