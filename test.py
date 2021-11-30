from team21_A1.helper_functions import get_legal_moves
from competitive_sudoku.sudoku import GameState, load_sudoku_from_text

board_text = '''2 2
    1   2   3   4
    3   4   .   2
    2   1   .   3
    .   .   .   1
'''

sudoku_board = load_sudoku_from_text(board_text)
game_state = GameState(sudoku_board, sudoku_board, [], [], [])
moves = get_legal_moves(game_state)

for m in moves:
    print(m)

# Seems to work, might want to clean this up a bit
