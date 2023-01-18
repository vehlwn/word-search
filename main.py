import itertools
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
        self.__word = ""

    def solve(self, word: str) -> Path:
        self.__word = word
        for (start_row, start_col) in itertools.product(
            gen_shuffled_iota(self.__board_height()),
            gen_shuffled_iota(self.__board_width()),
        ):
            start_cell = (start_row, start_col)
            self.__path = []
            if self.__solve_impl([start_cell]):
                break
        return self.__path

    def __solve_impl(self, candidates: Path) -> bool:
        if len(self.__path) > len(self.__word):
            return False
        word_from_path = self.__get_word_from_path()
        print(f"{word_from_path=}")
        if word_from_path == self.__word:
            return True
        for cell in candidates:
            self.__path.append(cell)
            adj = self.__gen_candidates(cell)
            if self.__solve_impl(adj):
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
        random.shuffle(ret)
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
