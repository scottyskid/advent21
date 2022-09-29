

class Dashboard():
    def __init__(self, pannel_definitions: list) -> None:
        self.pannels = []
        for pannel_definitions in pannel_definitions:
            self.pannels.append(Pannel(*pannel_definitions))

    def __repr__(self) -> str:
        repr_str = 'Dashboard:\n'
        for display in self.pannels:
            repr_str += f'{display}\n'
        return repr_str

    def count_all_uniques(self):
        uniques = 0
        for display in self.pannels:
            uniques += display.count_uniques()
        
        return uniques

    def get_output_value_sum(self):
        total = 0
        for pannel in self.pannels:
            total += pannel.get_output_number()
        return total


class Pannel():
    def __init__(self, unique_signal_patterns: list, output_values: list) -> None:
        self.unique_signal_patterns = unique_signal_patterns
        self.output_values = output_values

        self.seven_segment_display = SevenSegmentDisplay(self.unique_signal_patterns)

    def __repr__(self) -> str:
        return f'Pannel({self.seven_segment_display} | {", ".join(self.output_values)}'

    def count_uniques(self):
        uniques = 0
        for value in self.output_values:
            if len(value) in [2, 4, 3, 7]:
                uniques += 1

        return uniques

    def get_output_number(self):
        output_string = ''
        for digit in self.output_values:
            output_string += str(self.seven_segment_display.get_digit(digit))

        return int(output_string)


class SevenSegmentDisplay():
    def __init__(self, unique_signal_patterns: list) -> None:
        self.unique_signal_patterns = unique_signal_patterns

        self._segment_count = {
            2: [1], 
            3: [7],
            4: [4],
            5: [2, 3, 5], # only 2 is missing f and only 5 is missing c  [c, f, b, e]
            6: [0, 6, 9], # 0 is missing d 6 is missing c and 9 is missing e [c, d, e]
            7: [8],
        }

        self.segment_values = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        self.decoder = self._generate_decoder()

    def __repr__(self) -> str:
        return f'Display({", ".join(self.unique_signal_patterns)})'

    def _generate_decoder(self) -> dict:
        decoder = {}

        sorted_patterns = sorted(self.unique_signal_patterns, key=len)

        # sort characters
        for i, _ in enumerate(sorted_patterns):
            sorted_patterns[i] = ''.join(sorted(sorted_patterns[i]))

        val_1 = sorted_patterns[0]
        val_4 = sorted_patterns[2]

        decoder[val_1] = 1
        decoder[val_4] = 4
        decoder[sorted_patterns[1]] = 7
        decoder[sorted_patterns[9]] = 8

        # 5 segments: 2, 3, 5
        # 3 is the only 5 segment that has exactly 2 overlaps with 1
        # 2 is the only 5 segment that has exactly 2 overlaps with 4
        for pattern in sorted_patterns[3:6]:
            if len(set(pattern) & set(val_1)) == 2:
                decoder[pattern] = 3
            elif len(set(pattern) & set(val_4)) == 2:
                decoder[pattern] = 2
            else:
                decoder[pattern] = 5
        
        # 6 segments: 0, 6, 9
        # 6 is the only 6 segment that has exactly 1 overlap with 1
        # 9 is the only 6 segment that has exactly 4 overlaps with 4
        for pattern in sorted_patterns[6:9]:
            if len(set(pattern) & set(val_1)) == 1:
                decoder[pattern] = 6
            elif len(set(pattern) & set(val_4)) == 4:
                decoder[pattern] = 9
            else:
                decoder[pattern] = 0

        return decoder

    def get_digit(self, segments):
        sorted_segments = ''.join(sorted(segments))

        return self.decoder[sorted_segments]
        


if __name__ == "__main__":    
    with open('src/08.txt') as file:
        pannel_definitions = [[k.split() for k in i.split(' | ')] for i in file.read().split('\n')]

    dashboard = Dashboard(pannel_definitions)

    print(f'total uniques for part 1 is: {dashboard.count_all_uniques()}')
    print(f'total output for part 2 is: {dashboard.get_output_value_sum()}')

    
    