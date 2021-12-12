import unittest


from team21_A2.helper_functions import get_legal_moves
from team21_A2.heuristics import hidden_twin_exclusion
from competitive_sudoku.sudoku import GameState, TabooMove, Move, load_sudoku_from_text

board_text_2x2 = '''2 2
    1   2   3   4
    3   4   .   2
    2   1   .   3
    .   .   .   1
'''

board_text_2x2_1 = '''2 2
    1   2   3   4
    3   4   1   2
    2   1   4   3
    .   3   2   1
'''

board_text_2x2_2 = '''2 2
    .   .   3   .
    .   .   .   .
    2   1   .   .
    .   .   .   1
'''


class TestHelperFunction(unittest.TestCase):
    def test_get_legal_moves_no_taboo(self):
        sudoku_board = load_sudoku_from_text(board_text_2x2)
        game_state = GameState(sudoku_board, sudoku_board, [], [], [])
        moves = get_legal_moves(game_state)
        expected_moves = [
            Move(1, 2, 1),
            Move(2, 2, 4),
            Move(3, 0, 4),
            Move(3, 1, 3),
            Move(3, 2, 2),
            Move(3, 2, 4)
        ]
        self.assertEqual(moves, expected_moves)

    def test_get_legal_moves_with_taboo(self):
        pass
        sudoku_board = load_sudoku_from_text(board_text_2x2)
        game_state = GameState(sudoku_board, sudoku_board, [
                               TabooMove(1, 2, 1)], [], [])
        moves = get_legal_moves(game_state)
        expected_moves = [
            Move(2, 2, 4),
            Move(3, 0, 4),
            Move(3, 1, 3),
            Move(3, 2, 2),
            Move(3, 2, 4)
        ]
        self.assertEqual(moves, expected_moves)

    def test_get_legal_moves_with_one_move(self):
        sudoku_board = load_sudoku_from_text(board_text_2x2_1)
        game_state = GameState(sudoku_board, sudoku_board, [], [], [])
        moves = get_legal_moves(game_state)
        expected_moves = [Move(3, 0, 4)]
        self.assertEqual(moves, expected_moves)

    def test_heuristic_hidden_twin_exclusion(self):
        sudoku_board = load_sudoku_from_text(board_text_2x2_2)
        game_state = GameState(sudoku_board, sudoku_board, [], [], [])
        moves = get_legal_moves(game_state)
        new_moves = hidden_twin_exclusion(game_state, moves)
        diff = []

        for m in moves:
            if m not in new_moves:
                diff.append(m)

            else:
                continue

        expected_moves = [Move(1, 0, 1), Move(1, 1, 2), Move(1, 2, 1)]
        self.assertEqual(diff, expected_moves)


if __name__ == '__main__':
    unittest.main()
