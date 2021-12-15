from team21_A2.helper_functions import is_empty_cell, is_legal_move
from team21_A2.heuristics import hidden_twin_exclusion
from competitive_sudoku.sudoku import SudokuBoard, Move, load_sudoku_from_text

board_text_3x3_random = '''3 3
   .   .   1   6   8   2   9   3   .
   9   .   .   .   4   1   .   .   5
   .   .   .   .   7   9   .   4   .
   3   1   .   .   .   .   .   8   9
   7   .   .   1   9   3   .   5   .
   6   .   4   7   5   8   3   2   1
   1   4   .   .   .   7   .   .   .
   .   .   .   .   1   .   8   .   .
   8   .   .   9   .   5   6   .   4
'''

def get_legal_moves_without_heuristic(game_board: SudokuBoard, taboo_moves):
    """
    A method to calculate all legal moves from a GameState return a list of legal moves.
    @param game_board: The current Sudoku board of type SudokuBoard
    @param taboo_moves: The list of current taboo moves
    """
    legal_moves = []

    # Go over all possible index combination of the board
    for i in range(game_board.N):
        for j in range(game_board.N):
            # if the cell is not empty we can skip evaluating values
            if not is_empty_cell(game_board, i, j):
                continue
            else:
                # Try all possible values [1, ..., N] for a cell
                for k in range(1, game_board.N + 1):
                    # If a move is legal append to list of legal moves
                    if is_legal_move(game_board, taboo_moves, i, j, k):
                        cur_move = Move(i, j, k)
                        legal_moves.append(cur_move)

    return legal_moves, taboo_moves

board = load_sudoku_from_text(board_text_3x3_random)
moves, taboo_moves = get_legal_moves_without_heuristic(board, [])
new_moves, new_taboo_moves = hidden_twin_exclusion(board, moves)
print('Original moves\t:', len(moves))
print('New moves\t:', len(new_moves))