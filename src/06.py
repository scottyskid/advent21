

class School():
    def __init__(self, fish_ages) -> None:
        self.new_born_start = 8
        self.reset = 6
        self.qty = {}
        for i in range(self.new_born_start + 1):
            self.qty[i] = 0
        self.day = 0

        for fish in fish_ages:
            self.qty[fish] += 1

    def __repr__(self) -> str:
        return str(self.qty)

    def step_day(self):
        new_qty = {}
        for i in range(self.new_born_start, 0, -1):
            new_qty[i - 1] = self.qty[i]
        
        new_qty[self.reset] += self.qty[0]
        new_qty[self.new_born_start] = self.qty[0]

        self.qty = new_qty

        self.day += 1

    def step_days(self, days):
        for _ in range(days):
            self.step_day()

    def get_total_fish(self):
        return sum(self.qty.values())


if __name__ == "__main__":   
    with open('src/06.txt') as file:
        fish_ages = [int(i) for i in file.read().split(',')]
    
    school = School(fish_ages)
    school.step_days(256)

    print(school)
    print(f'total number of fish are {school.get_total_fish()}')