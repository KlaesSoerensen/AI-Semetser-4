from enum import Enum
from typing import Self


class Symbols(Enum):
    X = "X"
    O = "O"
    UNPLACED = "i"

    def __str__(self):
        return self.value

    @classmethod
    def placed(cls) -> tuple[Self, Self]:
        return cls.X, cls.O


type Board = list[Symbols]


def minmax_decision(state: Board) -> int:
    def max_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = -infinity
        for (a, s) in successors_of(state_option):
            expected_value = max(expected_value, min_value(s))
        return expected_value

    def min_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = infinity
        for (a, s) in successors_of(state_option):
            expected_value = min(expected_value, max_value(s))
        return expected_value

    infinity = float('inf')
    action, state = max(successors_of(state), key=lambda a: min_value(a[1]))
    return action


def is_terminal(state: Board) -> bool:
    # Check if there's a winner or the board is full.
    return utility_of(state) != 0 or all(symbol != Symbols.UNPLACED for symbol in state)


    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard.
    Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return:
    """


def utility_of(state: Board) -> int:
    # Check rows, columns, and diagonals for wins.
    for i in range(3):
        # Check rows
        if state[3 * i] == state[3 * i + 1] == state[3 * i + 2] != Symbols.UNPLACED:
            return 1 if state[3 * i] == Symbols.X else -1
        # Check columns
        if state[i] == state[i + 3] == state[i + 6] != Symbols.UNPLACED:
            return 1 if state[i] == Symbols.X else -1

    # Check diagonals
    if state[0] == state[4] == state[8] != Symbols.UNPLACED or state[2] == state[4] == state[6] != Symbols.UNPLACED:
        return 1 if state[4] == Symbols.X else -1

    return 0  # No winner


def successors_of(state: Board) -> list[tuple[int, Board]]:
    successors = []
    current_symbol = Symbols.X if state.count(Symbols.X) <= state.count(Symbols.O) else Symbols.O
    for i, symbol in enumerate(state):
        if symbol == Symbols.UNPLACED:
            new_state = state.copy()
            new_state[i] = current_symbol
            successors.append((i, new_state))
    return successors



def display(state: list[Symbols]) -> None:
    print("-----")
    for i in range(0, 3):
        for c in range(i * 3, i * 3 + 3):
            print("|", end="")
            symbol = c if state[c] == Symbols.UNPLACED else state[c]
            print(symbol, end="")
        print("|")


def main():
    board = [Symbols.UNPLACED] * 9
    while not is_terminal(board):
        board[minmax_decision(board)] = Symbols.X
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = Symbols.O
    display(board)


if __name__ == '__main__':
    main()
