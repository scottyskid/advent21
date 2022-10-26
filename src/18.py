from abc import ABC, abstractmethod
from builtins import ValueError
from itertools import permutations 
from math import ceil, floor
from pprint import pprint


class Side(ABC):
    @abstractmethod
    def reasign_item(self, item, new_item):
        pass

    def find_adjacent_element(self, element):
        pass

class Left(Side):
    def reasign_item(self, item, new_item):
        item.parent.left = new_item
        new_item.parent = item.parent
        new_item.side = item.side
    
    def find_adjacent_element(self, element):
        top_level_item = element.get_root()
        all_elements = top_level_item.child_elements()
        element_index = all_elements.index(element)
        if element_index == 0:
            return None
        else:
            return all_elements[element_index - 1]

class Right(Side):
    def reasign_item(self, item, new_item):
        item.parent.right = new_item
        new_item.parent = item.parent
        new_item.side = item.side

    def find_adjacent_element(self, element):
        top_level_item = element.get_root()
        all_elements = top_level_item.child_elements()
        element_index = all_elements.index(element)
        if element_index == len(all_elements) - 1:
            return None
        else:
            return all_elements[element_index + 1]

class Item(ABC):
    def __init__(self, parent=None, side=None):
        self.parent = parent
        self.side = side

    def depth(self):
        total_depth = 0
        cur_pair = self.parent
        while cur_pair is not None:
            total_depth += 1
            cur_pair = cur_pair.parent

        return total_depth

    def get_root(self):
        cur_pair = self
        while cur_pair.parent is not None:
            cur_pair = cur_pair.parent
        
        return cur_pair
    
    @abstractmethod
    def explode(self):
        pass

    @abstractmethod
    def magnitude(self):
        pass


class Element(Item):
    def __init__(self, value: int, parent, side: Side):
        super().__init__(parent, side)
        self.value = value

    def __repr__(self):
        return f'E({self.value})'

    def __str__(self):
        return f'{self.value}'

    def split(self):
        new_left = floor(self.value / 2)
        new_right = ceil(self.value / 2)
        split_pair = Pair(new_left, new_right, parent=self.parent, side=self.side)
        self.side.reasign_item(self, split_pair)

    def explode(self):
        adjacent_element = self.side.find_adjacent_element(self)
        if adjacent_element is not None:
            adjacent_element.value += self.value

    def magnitude(self):
        return self.value
    

class Pair(Item): 
    def __init__(self, left, right, *, parent=None, side: Side=None) -> None:
        super().__init__(parent, side)
        if isinstance(left, list):
            self._left = Pair(*left, parent=self, side=Left())
        elif isinstance(left, Pair):
            if left.parent is None:
                self._left = left
                self._left.parent = self
                self._left.side = Left()
            else:
                raise ValueError('left value is not a root pair')
        elif isinstance(left, int):
            self._left = Element(left, parent=self, side=Left())
        else:
            raise TypeError('left must be a valid type')
        
        if isinstance(right, list):
            self._right = Pair(*right, parent=self, side=Right())
        elif isinstance(right, Pair):
            if right.parent is None:
                self._right = right
                self._right.parent = self
                self._right.side = Right()
            else:
                raise ValueError('right value is not a root pair')
        elif isinstance(right, int):
            self._right = Element(right, parent=self, side=Right())
        else:
            raise TypeError('right must be a valid type')

    def __repr__(self):
        return f'P[{self.left}, {self.right}]'

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __add__(self, other):
        if isinstance(other, Pair):
            new_pair = Pair(self, other)
            new_pair.reduce()
            return new_pair
        else:
            raise TypeError(f'cannot add {type(other)} to {type(self)}')

    def child_pairs(self):
        child_pairs = []
        if isinstance(self.left, Pair):
            child_pairs += [self.left]
            child_pairs += self.left.child_pairs()
        if isinstance(self.right, Pair):
            child_pairs += [self.right]
            child_pairs += self.right.child_pairs()
        return child_pairs

    def base_child_pairs(self):
        return [pair for pair in self.child_pairs() if pair.is_base_pair()]

    def child_elements(self):
        child_elements = []
        if isinstance(self.left, Element):
            child_elements += [self.left]
        else:
            child_elements += self.left.child_elements()
        if isinstance(self.right, Element):
            child_elements += [self.right]
        else:
            child_elements += self.right.child_elements()
        return child_elements

    def find_explosion_pair(self):
        # all_pairs = []
        for pair in self.base_child_pairs():
            if pair.depth() > 3:
                # all_pairs.append(pair)
                return pair
        return None

    def find_split_element(self):
        child_elements = self.child_elements()
        for element in child_elements:
            if element.value >= 10:
                return element
        return None

    def is_base_pair(self):
        return isinstance(self.left, Element) and isinstance(self.right, Element)
        
    def reduce(self):
        while True:
            explosion_pair = self.find_explosion_pair()
            if explosion_pair is not None:
                explosion_pair.explode()
                continue
            split_element = self.find_split_element()
            if split_element is not None:
                split_element.split()
                continue
            break

    def explode(self):
        if not self.is_base_pair():
            raise ValueError('self must be a base pair to be able to explode')

        self.left.explode()
        self.right.explode()

        self.side.reasign_item(self, Element(0, self.parent, self.side))

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_left):
        self._left = new_left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_right):
        self._right = new_right
        



if __name__ == "__main__":    
    with open('src/18.txt') as file:
        input_val = file.readlines()

        number = Pair(*eval(input_val[0].strip()))

        for line in input_val[1:]:
            next_number = Pair(*eval(line.strip()))
            number += next_number

        print(f'part 1 final number is {number} and its magnitude is {number.magnitude()}')

        # find the largest magnitude
        groups = permutations(input_val, 2)

        largest_magnitude = 0
        largest_groups = [None, None]
        
        for a, b in groups:
            a_number = Pair(*eval(a.strip()))
            b_number = Pair(*eval(b.strip()))

            number = a_number + b_number
            magnitude = number.magnitude()
            
            if magnitude > largest_magnitude:
                largest_magnitude = magnitude
                largest_groups = [a_number, b_number]

        
        print(f'part 2 the largest magnitude is {largest_magnitude}')



    
