


class Octopus():
    def __init__(self, x, y, energy) -> None:
        self.x = x
        self.y = y
        self.energy = energy
        self.adjacent_octopus = []

        self.has_flashed = False

    def __repr__(self) -> str:
        return f'Point(x={self.x}, y={self.y}, e={self.energy})'

    def flash(self):
        self.has_flashed = True

        for octopus in self.adjacent_octopus:
            octopus.energy += 1



    def step_clean_up(self):
        if self.has_flashed:
            self.energy = 0
            self.has_flashed = False



class Cavern():
    def __init__(self, octopus_map) -> None:
        point_values = octopus_map.split('\n')

        self.x_length = len(point_values[0])
        self.y_width = len(point_values)

        self.current_step = 0
        self.flashes = 0

        self.octopus = {}

        for y in range(self.y_width):
            for x in range(self.x_length): 
                self.octopus[(x, y)] = Octopus(x, y, int(point_values[y][x]))

        adj_deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for key, cur_octopus in self.octopus.items():
            cur_x, cur_y = key
            for x_delta, y_delta in adj_deltas:
                try:
                    cur_octopus.adjacent_octopus.append(self.octopus[(cur_x + x_delta, cur_y + y_delta)])
                except KeyError:
                    pass

    def current_energy_map(self):
        str_rep = f'Energy map at step {self.current_step}' + '\n'
        for y in range(self.y_width):
            for x in range(self.x_length): 
                str_rep += str(self.octopus[(x, y)].energy)
            str_rep += '\n'

        return str_rep

    

    def progress_step(self):

        for octopus in self.octopus.values():
            octopus.energy += 1

        while True:
            flashable = [o for o in self.octopus.values() if o.energy > 9 and not o.has_flashed]

            if len(flashable) == 0:
                break
            
            for octopus in flashable:
                octopus.flash()
                self.flashes += 1

        hasnt_flashed = [True for o in self.octopus.values() if not o.has_flashed]

        for octopus in self.octopus.values():
            octopus.step_clean_up()

        self.current_step += 1

        if len(hasnt_flashed) > 0:
            return False
        else: 
            return True


if __name__ == "__main__":    
    with open('src/11.txt') as file:
        octopus_map = file.read()

    cavern = Cavern(octopus_map)

    while True:
        has_synced = cavern.progress_step()
        if has_synced:
            break
    print(cavern.current_energy_map())

    print(f'total flashes are {cavern.flashes}')
    print(f'total final_step are {cavern.current_step}')

