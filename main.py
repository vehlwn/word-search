import random
import typing

Cell = typing.Tuple[int, int]
Path = typing.List[Cell]
Board = typing.List[str]


def gen_shuffled_iota(n: int) -> typing.List[int]:
    ret = list(range(n))
    random.shuffle(ret)
    return ret


class Solver:
    def __init__(self, board: Board) -> None:
        self.__board = board
        self.__path: Path = []

    def solve(self, word: str) -> Path:
        self.__path = []
        for start_row in gen_shuffled_iota(self.__board_height()):
            for start_col in gen_shuffled_iota(self.__board_width()):
                start_cell = (start_row, start_col)
                if self.__solve_impl(word, start_cell):
                    break
        return self.__path

    def __solve_impl(self, word: str, start_cell: Cell) -> bool:
        if len(self.__path) > len(word):
            return False
        word_from_path = self.__get_word_from_path()
        print(f"{word_from_path=}")
        if word_from_path == word:
            return True
        candidates = self.__gen_candidates(start_cell)
        for cell in candidates:
            self.__path.append(cell)
            if self.__solve_impl(word, cell):
                return True
            else:
                self.__path.pop()
        return False

    def __board_height(self) -> int:
        return len(self.__board)

    def __board_width(self) -> int:
        return len(self.__board[0])

    def __get_word_from_path(self) -> str:
        ret = ""
        for (row, col) in self.__path:
            ret += self.__board[row][col]
        return ret

    def __gen_candidates(self, start_cell: Cell) -> Path:
        tmp = [
            [start_cell[0], start_cell[1] + 1],
            [start_cell[0], start_cell[1] - 1],
            [start_cell[0] + 1, start_cell[1]],
            [start_cell[0] - 1, start_cell[1]],
        ]
        ret = []
        for (row, col) in tmp:
            if (
                0 <= row < self.__board_height()
                and 0 <= col < self.__board_width()
                and (row, col) not in self.__path
            ):
                ret.append((row, col))
        return ret


def main():
    word = ""
    board = []
    with open("input.txt", "rt") as in_file:
        word = in_file.readline().strip()
        height = int(in_file.readline())
        for _ in range(height):
            line = in_file.readline().strip()
            board.append(line)
    print(f"{word=}")
    print(f"{board=}")
    s = Solver(board)
    path = s.solve(word)
    if len(path) > 0:
        print("found")
        print(path)
    else:
        print("no")


if __name__ == "__main__":
    main()
