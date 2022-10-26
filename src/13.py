


class Paper():
    def __init__(self, dot_coords) -> None:
        self.dots = []

        for dot_coord in dot_coords:
            self.dots.append(Dot(dot_coord))

    def __len__(self):
        return len(self.dots)

    def __str__(self):
        return self.show_dots()

    def fold(self, direction, fold_line):
        for dot in self.dots:
            dot.fold(direction, fold_line)

        self.dots = list(set(self.dots))
    
    def show_dots(self):
        max_x = max(self.dots, key=lambda x: x.x)
        max_y = max(self.dots, key=lambda x: x.y)

        page = [[' ' for j in range(max_x.x + 1)] for i in range(max_y.y + 1)]

        for dot in self.dots:
            page[dot.y][dot.x] = '#'

        str_repr = '\n'.join([''.join(i) for i in page])
        return str_repr



class Dot():
    def __init__(self, coords):
        self.x, self.y = coords

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'Dot({self.x}, {self.y})'

    def fold(self, direction, fold_line):
        if direction == 'y':
            y_delta = self.y - fold_line

            if y_delta > 0:
                self.y = fold_line - y_delta
        elif direction == 'x':
            x_delta = self.x - fold_line

            if x_delta > 0:
                self.x = fold_line - x_delta





if __name__ == "__main__":
    with open('src/13.txt') as file:
        text_input = file.read()

    dot_coords, folds = text_input.split('\n\n')

    folds = [i.strip().split(' ')[-1].split('=') for i in folds.split('\n')]

    dot_coords = [tuple([int(k) for k in i.strip().split(',')]) for i in dot_coords.split('\n')]

    paper = Paper(dot_coords)

    for fold in folds:
        paper.fold(fold[0], int(fold[1]))
        print(f'the current total dots are {len(paper)}')

    print(paper)


    