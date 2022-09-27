

class BingoTile():
    def __init__(self, value: int, x: int, y: int, checked: bool = False) -> None:
        self.value = value
        self.x = x
        self.y = y
        self.checked = checked

    def __repr__(self) -> str:
        # if not self.checked:
        #     return ' '
        return f'{self.value}'


class BingoBoard():
    def __init__(self, board_numbers: str, board_id: int) -> None:
        self.board = []
        self.board_id = board_id
        self.last_number_called = 0
        self._board_x_size = 0 
        self._board_y_size = 0
        for y, i in enumerate(board_numbers.split('\n')):
            self._board_y_size = y if y > self._board_y_size else self._board_y_size
            for x, k in enumerate(i.split()):
                self._board_x_size = x if y > self._board_x_size else self._board_x_size
                self.board.append(BingoTile(int(k), x, y))

    
        self._board_x_size += 1 
        self._board_y_size += 1

        self.winning_tile_groups = []

        for col in range(self._board_x_size):
            group = []
            for tile in self.board:
                if tile.x == col:
                    group.append(tile)
            self.winning_tile_groups.append(group)
        
        for row in range(self._board_y_size):
            group = []
            for tile in self.board:
                if tile.y == row:
                    group.append(tile)
            self.winning_tile_groups.append(group)


    def __repr__(self) -> str:
        repr_val = f'board number {self.board_id}\n'
        for row_num in range(self._board_y_size):
            repr_val += f'{self.board[row_num:row_num + self._board_x_size]}\n'

        sum_unchecked_tiles = self.sum_unchecked_tiles()
        repr_val += f'with a value of { sum_unchecked_tiles * self.last_number_called}\n'
        return repr_val

    def find_tile(self, value: int) -> (BingoTile):
        for tile in self.board:
            if tile.value == value:
                return tile
    
    def check_off_number(self, number: int) -> None:
        tile = self.find_tile(number)
        if tile is None:
            return False
        else:
            tile.checked = True
            self.last_number_called = number
            return tile
    
    def has_won(self):
        for group in self.winning_tile_groups:
            tile_status = [tile.checked for tile in group]
            if all(tile_status):
                return True
        return False

    def sum_unchecked_tiles(self):
        total = 0
        for tile in self.board:
            total += 0 if tile.checked else tile.value

        return total


class BingoGame():
    def __init__(self, numbers: str, boards: list) -> None:
        self.future_numbers = [int(i) for i in numbers.split(',')]
        self.past_numbers = []
        self.winners = []

        self.boards = []
        for board_id, board_numbers in enumerate(boards):
            self.boards.append(BingoBoard(board_numbers, board_id))

    def __repr__(self) -> str:
        repr_val = '\n'
        repr_val += f'future numbers: {self.future_numbers}\n'
        repr_val += f'called numbers: {self.past_numbers}\n'
        repr_val += '\n'

        for board in self.boards:
            repr_val += board.__repr__()
            repr_val += '\n'

        repr_val += f'the winners are \n'

        for board in self.winners:
            repr_val += board.__repr__()

            repr_val += '\n'

        return repr_val

    def has_winner(self):
        if len(self.winners) > 0:
            return True
        return False

    def is_game_over(self):
        if len(self.future_numbers) == 0:
            return True
        return False

    def next_turn(self):
        called_number = self.future_numbers.pop(0)
        for board in self.boards:
            if not board.has_won():
                board.check_off_number(called_number)

        self.past_numbers.append(called_number)

        for board in self.boards:
            if board.has_won() and board not in self.winners:
                self.winners.append(board)

        self.is_game_over()
        

if __name__ == "__main__":
    with open('src/04.txt') as file:
        file_split_sections = file.read().split('\n\n')

    bingo_game = BingoGame(file_split_sections[0], file_split_sections[1:])
    # print(bingo_game.boards[0].winning_tile_groups)
    while not bingo_game.is_game_over():
        bingo_game.next_turn()

    print(f'the best board is {bingo_game.winners[0]}')    
    print(f'the worst board is {bingo_game.winners[-1]}')    

