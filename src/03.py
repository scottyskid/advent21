# from decimal import (
#     Decimal,
#     localcontext,
# )

class Diagnostics():
    def __init__(self, numbers: list):

        self.numbers = []
        for row in numbers:
            self.numbers.append([int(i) for i in row.strip()])

    def sum_columns(self, rows_to_include: list = None):
        if rows_to_include is None:
            rows_to_include = list(range(len(self.numbers)))

        bit_counter = []

        for row_idx in rows_to_include:
                
            for i, bit in enumerate(self.numbers[row_idx]):
                int_bit = int(bit)
                if i < len(bit_counter):
                    bit_counter[i] += int_bit
                else:
                    bit_counter.append(int_bit)

        return bit_counter, len(rows_to_include)


    def get_highest_digits(self, rows_to_include: list = None):
        sums, total = self.sum_columns(rows_to_include)

        highest_digits = []

        for val in sums:
            highest_digits.append(0 if val < total / 2 else 1)

        return highest_digits

    def get_lowest_digits(self, rows_to_include: list = None):
        sums, total = self.sum_columns(rows_to_include)

        lowest_digits = []

        for val in sums:
            lowest_digits.append(0 if val >= total / 2 else 1)

        return lowest_digits

    def get_gamma_epsilon(self):
        higest_digits = self.get_highest_digits()
        gamma = self._binary_to_dec(higest_digits)

        
        lowest_digits = self.get_lowest_digits()
        epsilon = self._binary_to_dec(lowest_digits)

        return gamma * epsilon

    def get_rating(self, digit_func):
        valid_rows = list(range(len(self.numbers)))
        for i in range(len(self.numbers[0])):
            if len(valid_rows) <= 1:
                break
            digit = digit_func(valid_rows)[i]
            new_valid_rows = []
            for k in valid_rows:
                if self.numbers[k][i] == digit:
                    new_valid_rows.append(k)
            valid_rows = new_valid_rows

        rating = self._binary_to_dec(self.numbers[valid_rows[0]])

        return rating

    def get_part2(self):
        oxygen_rating = self.get_rating(self.get_highest_digits)
        co2_rating = self.get_rating(self.get_lowest_digits)

        return oxygen_rating * co2_rating


    def _binary_to_dec(self, binary: list):
        dec = 0

        for i, val in enumerate(binary):
            unit = len(binary) - i - 1
            dec += val * (2 ** unit)

        return dec



if __name__ == "__main__":

    with open('src/03.txt') as file:
        diag = Diagnostics(list(file))

    part1 = diag.get_gamma_epsilon()
    print(f'part1 result: {part1}')

    part2 = diag.get_part2()
    print(f'part2 result: {part2}')