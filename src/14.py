
from collections import defaultdict


class Polymer():
    def __init__(self, starting_polymer, rules) -> None:
        self.rules = rules
        self.step_number = 0

        self.polymer_pairs = defaultdict(int)
        starting_pairs = [''.join(t) for t in zip(starting_polymer, starting_polymer[1:])]

        for pair in starting_pairs:
            self.polymer_pairs[pair] += 1

        self.last_letter = starting_polymer[-1]

    def __repr__(self) -> str:
        return str(self.polymer_pairs)

    def step(self):
        new_polymer_pairs = defaultdict(int)

        for pair, val in self.polymer_pairs.items():
            first_pair = pair[0] + self.rules[pair]
            new_polymer_pairs[first_pair] += val

            second_pair = self.rules[pair] + pair[1]
            new_polymer_pairs[second_pair] += val

        self.polymer_pairs = new_polymer_pairs
        self.step_number += 1

    def count_characters(self):
        chars = defaultdict(int)

        for pair, val in self.polymer_pairs.items():
            chars[pair[0]] += val

        chars[self.last_letter] += 1

        return dict(chars)

    def diff_highest_lowest(self):
        char_counts = self.count_characters()

        return max(char_counts.values()) - min(char_counts.values())
    

if __name__ == "__main__":
    with open('src/14.txt') as file:
        text_input = file.readlines()

    starting_polymer = text_input[0].strip()
    rules = {i.split(' -> ')[0]: i.split(' -> ')[1].strip() for i in text_input[2:]}

    polymer = Polymer(starting_polymer, rules)

    for i in range(40):
        if i == 10:
            print(f'part 1 response is {polymer.diff_highest_lowest()}')
        polymer.step()

    print(f'part 2 response is {polymer.diff_highest_lowest()}')
