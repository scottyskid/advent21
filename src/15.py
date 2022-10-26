from pprint import pprint


class Point():
    def __init__(self, x, y, risk) -> None:
        self.x = x
        self.y = y
        self.key = (x, y)
        self.risk = risk
        self.h = 1
        self.adjacent_points = []

    def __repr__(self) -> str:
        return f'Point(x={self.x}, y={self.y}, r={self.risk})'

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x, self.y) == (other.x, other.y)
        return False

    def __hash__(self):
        return hash((self.x, self.y))


class Cavern():
    def __init__(self, risk_map) -> None:
        point_values = risk_map

        self.x_length = len(point_values[0])
        self.y_width = len(point_values)

        self.points = {}

        for y in range(self.y_width):
            for x in range(self.x_length): 
                self.points[(x, y)] = Point(x, y, int(point_values[y][x]))

        adj_deltas = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        for key, cur_point in self.points.items():
            cur_x, cur_y = key
            for x_delta, y_delta in adj_deltas:
                try:
                    cur_point.adjacent_points.append(self.points[(cur_x + x_delta, cur_y + y_delta)])
                except KeyError:
                    pass

        


    def __repr__(self) -> str:
        str_rep = f'point map ' + '\n'
        for y in range(self.y_width):
            for x in range(self.x_length): 
                str_rep += str(self.points[(x, y)].risk)
            str_rep += '\n'

        return str_rep

    def lowest_risk_route(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + v.h < g[n] + n.h:
                    n = v;

            if n == None:
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)
                reconst_path.reverse()

                return reconst_path

            # for all neighbors of the current node do
            for m in n.adjacent_points:
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + m.risk

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + m.risk:
                        g[m] = g[n] + m.risk
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        return None

    def calc_total_risk(self):
        
        start = self.points[(0, 0)]
        end = self.points[(self.x_length - 1, self.y_width - 1)]

        path = self.lowest_risk_route(start, end)

        total_risk = sum([i.risk for i in path[1:]])
        return total_risk


def expand_cavern_map(cavern_map, factor):
    expanded_map = []
    for k in range(factor):
        for row in cavern_map:
            new_row = ''
            for i in range(factor):
                for char in row:
                    new_row += str((int(char) + i + k - 1) % 9 + 1)

            expanded_map.append(new_row)
    
    return expanded_map

if __name__ == "__main__":    
    with open('src/15.txt') as file:
        point_map = file.read()
        point_map = point_map.split('\n')

    cavern_1 = Cavern(point_map)

    print(f'the total risk for part 1 is {cavern_1.calc_total_risk()}')


    expanded_map = expand_cavern_map(point_map, 5)

    cavern_2 = Cavern(expanded_map)

    print(f'the total risk for part 2 is {cavern_2.calc_total_risk()}')

