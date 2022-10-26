from abc import ABC
from itertools import product
from pprint import pprint


class Pixel(ABC):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def coords(self):
        return (self.x, self.y)


class LightPixel(Pixel):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.val = 1

    def __repr__(self) -> str:
        return f'P({self.x}, {self.y}, #)'

    def __str__(self) -> str:
        return '#'

    
class DarkPixel(Pixel):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.val = 0

    def __repr__(self) -> str:
        return f'P({self.x}, {self.y}, .)'

    def __str__(self) -> str:
        return '.'


class Image():
    def __init__(self, initial_image, enhancement_algorithm) -> None:
        self.infinite_flip = enhancement_algorithm[0] == '#'
        self.infinite_pixel = DarkPixel

        self.enhancement_count = 0

        self.algo_light_locations = []

        for loc, i in enumerate(enhancement_algorithm):
            if i == '#':
                self.algo_light_locations.append(loc)

        self.pixels = {}

        for y, line in enumerate(initial_image.split('\n')):
            for x, char in enumerate(line):
                if char == '#':
                    new_pixel = LightPixel(x, y)
                else:
                    new_pixel = DarkPixel(x, y)
                self.pixels[new_pixel.coords] = new_pixel

        

    def __repr__(self) -> str:
        dimentions = self.image_dimensions
        image_output = ''
        for y in range(dimentions['min_y'], dimentions['max_y'] + 1):
            for x in range(dimentions['min_x'], dimentions['max_x'] + 1):
                image_output += str(self.pixels.get((x, y), '_'))
            image_output += '\n'

        return image_output


    @property
    def image_dimensions(self):
        """gets the range of the x and y axes
        """
        dims = {}
        dims['min_x'] = min([i.x for i in self.pixels.values()])
        dims['min_y'] = min([i.y for i in self.pixels.values()])
        dims['max_x'] = max([i.x for i in self.pixels.values()])
        dims['max_y'] = max([i.y for i in self.pixels.values()])

        return dims

    def enhance(self):
        self.enhancement_count += 1
        dimentions = self.image_dimensions

        # add border pixels
        border_pixel_coords = set(product((dimentions['min_x'] - 1, dimentions['max_x'] + 1), range(dimentions['min_y'] - 1, dimentions['max_y'] + 2)))
        border_pixel_coords |= set(product(range(dimentions['min_x'], dimentions['max_x'] + 1), (dimentions['min_y'] - 1, dimentions['max_y'] + 1)))

        for x, y in border_pixel_coords:
            new_pixel = self.infinite_pixel(x, y)
            self.pixels[new_pixel.coords] = new_pixel

        new_pixels = {}
        for pixel in self.pixels.values():
            algo_index = self.get_binary_value(pixel)
            if algo_index in self.algo_light_locations:
                new_pixel = LightPixel(pixel.x, pixel.y)
            else:
                new_pixel = DarkPixel(pixel.x, pixel.y)
            new_pixels[new_pixel.coords] = new_pixel

        self.pixels = new_pixels

        if self.infinite_flip and self.infinite_pixel == DarkPixel:
            self.infinite_pixel = LightPixel
        elif self.infinite_flip and self.infinite_pixel == LightPixel:
            self.infinite_pixel = DarkPixel


    def get_binary_value(self, pixel):
        coord_deltas = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), ]
        binary_string = ''

        for xd, yd in coord_deltas:
            adj_pixel = self.pixels.get((pixel.x + xd, pixel.y + yd), self.infinite_pixel(pixel.x + xd, pixel.y + yd))
            binary_string += str(adj_pixel.val)

        value = int(binary_string, 2)

        return value

    def get_lit_pixel_count(self):
        total = 0
        for pixel in self.pixels.values():
            total += 1 if isinstance(pixel, LightPixel) else 0

        return total

                

if __name__ == "__main__":  
    with open('src/20.txt', mode='r') as file:
        algo = file.readline().strip()
        initial_image = file.read().strip()

    image = Image(initial_image, algo)
    for _ in range(50):
        image.enhance()

    print(f'the total number of lit pixels is {image.get_lit_pixel_count()}')