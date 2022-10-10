
class Subsystem():
    def __init__(self, lines):
        self.lines = [Line(i.strip()) for i in lines]
        corrupt_chars = [line.check_corruption() for line in self.lines]

        print(f'part 1 response is {self.part_1(corrupt_chars)}')

        # remove corrupted parts
        self.lines = [self.lines[i] for i, c_char in enumerate(corrupt_chars) if c_char is None]

        print(f'part 2 response is {self.get_winner().score}')


    def part_1(self, corrupt_chars):
        
        total_score = 0
        for i in corrupt_chars:
            if i == ')':
                total_score += 3
            elif i == ']':
                total_score += 57
            elif i == '}':
                total_score += 1197
            elif i == '>':
                total_score += 25137

        return total_score

    def get_winner(self):
        sorted_lines = sorted(self.lines, key=lambda x: x.score)

        return sorted_lines[int(len(sorted_lines)/2)]


class Line():
    def __init__(self, line):
        self.line = line

        self.openers = '([{<'
        self.closers = ')]}>'

        self.pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}

        self.line_end = self.get_line_completion()

        self.score = self.get_score()
        
    def check_corruption(self):
        current_chunks = []
        for item in self.line:
            if item in self.openers:
                current_chunks.append(item)
            else:
                opener = current_chunks.pop()
                if item != self.pairs[opener]:
                    return item
        return None

    def get_line_completion(self):
        current_chunks = []
        for item in self.line:
            if item in self.openers:
                current_chunks.append(item)
            else:
                current_chunks.pop()
        
        line_completion = ''
        for item in current_chunks[::-1]:
            line_completion += self.pairs[item]

        return line_completion

    def get_score(self):
        final_score = 0
        for i in self.line_end:
            final_score *= 5
            if i == ')':
                final_score += 1
            elif i == ']':
                final_score += 2
            elif i == '}':
                final_score += 3
            elif i == '>':
                final_score += 4

        return final_score





if __name__ == "__main__":    

    lines = []
    with open('src/10.txt') as file:
        lines = file.readlines()

    subsystem = Subsystem(lines)

    