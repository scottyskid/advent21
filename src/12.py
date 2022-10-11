

class CaveSystem():
    def __init__(self, cave_system_map_conns):
        self.cave_system_map = cave_system_map_conns

        self.caves = {}

        for conn in self.cave_system_map:
            caves_names = conn.split('-')

            caves = []

            for cave_name in caves_names:
                if cave_name in self.caves:
                    caves.append(self.caves[cave_name])
                else:
                    new_cave = Cave(cave_name)
                    self.caves[cave_name] = new_cave
                    caves.append(new_cave)

            self.add_cave_connection(*caves)

        self.start = self.caves['start']
        self.end = self.caves['end']

        self.routes = []
        self.find_cave_routes()

        self.routes_b = []
        self.find_cave_routes_b()

    def __repr__(self) -> str:
        repr_str = ''
        repr_str += ', '.join([str(i) for i in self.caves.values()])
        return repr_str
        
    def add_cave_connection(self, *args):
        cave_a, cave_b = args
        cave_a.add_connection(cave_b)
        cave_b.add_connection(cave_a)

    def find_cave_routes(self, existing_route=None):
        if existing_route is None:
            existing_route = [self.start]

        if existing_route[-1] == self.end:
            self.routes.append(existing_route)
            return existing_route

        next_caves = [i for i in existing_route[-1].connections if i not in existing_route or i.is_big]

        for next_cave in next_caves:
            self.find_cave_routes(existing_route + [next_cave])

    def find_cave_routes_b(self, existing_route=None):
        if existing_route is None:
            existing_route = [self.start]

        if existing_route[-1] == self.end:
            self.routes_b.append(existing_route)
            return existing_route

        current_small_caves = [i for i in existing_route if not i.is_big]
        unique_current_small_caves = set(current_small_caves)
        if len(unique_current_small_caves) < len(current_small_caves):
            next_caves = [i for i in existing_route[-1].connections if i not in existing_route or i.is_big]
        else:
            next_caves = [i for i in existing_route[-1].connections if i is not self.start]

        for next_cave in next_caves:
            self.find_cave_routes_b(existing_route + [next_cave])


class Cave():
    def __init__(self, name):
        self.name = name
        self.is_big = name.isupper()
        self.connections = []

    def __repr__(self) -> str:
        return f'Cave({self.name})'

    def add_connection(self, other_cave):
        self.connections.append(other_cave)


if __name__ == "__main__":
    with open('src/12.txt') as file:
        cave_system_map = file.readlines()
        cave_system_map = [i.strip() for i in cave_system_map]

    print(cave_system_map)
    cave_system = CaveSystem(cave_system_map)

    # cave_routes = cave_system.find_cave_routes()

    print(f'part 1 answer is {len(cave_system.routes)}')
    print(f'part 2 answer is {len(cave_system.routes_b)}')

