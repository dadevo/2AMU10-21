import numpy as np
from competitive_sudoku.sudoku import SudokuBoard, Move
from team21_A3_lessCopy.helper_functions import is_empty_cell, find_row, find_column, find_region


def remove_possible_value_row(board, m, value):
    """
    Removes a value from possible options for a cell in a row if it is already present somewhere else in the row
    @param board: The current SudokuBoard of the Competitive Sudoku game
    @param m: The row-value for the specific row in the SudokuBoard
    @param value: The value that we are checking for
    """
    for n in range(len(board)):
        cur_possibilities = board[m, n]
        if cur_possibilities is not None and len(cur_possibilities) > 1 and value in cur_possibilities:
            cur_possibilities.remove(value)
            board[m, n] = cur_possibilities

    return board


def remove_possible_value_column(board, n, value):
    """
    Removes a value from possible options for a cell in a column if it is already present somewhere else in the column
    @param board: The current SudokuBoard of the Competitive Sudoku game
    @param n: The column-value for the specific row in the SudokuBoard
    @param value: The value that we are checking for
    """
    for m in range(len(board)):
        cur_possibilities = board[m, n]
        if cur_possibilities is not None and len(cur_possibilities) > 1 and value in cur_possibilities:
            cur_possibilities.remove(value)
            board[m, n] = cur_possibilities

    return board


def remove_possible_value_region(board, m, n, bm, bn, value):
    """
    Removes a value from possible options for a cell in a region if it is already present somewhere else in the region
    @param board: The current SudokuBoard of the Competitive Sudoku game
    @param m: The row-value for the specific region in the SudokuBoard
    @param n: The column-value for the specific region in the SudokuBoard
    @param value: The value that we are checking for
    """

    # We can define the region using the row/column coordinates using some clever math
    row_region_index = (m // bm) * bm
    column_region_index = (n // bn) * bn

    for m_i in range(row_region_index, row_region_index + bm):
        for n_i in range(column_region_index, column_region_index + bn):
            cur_possibilities = board[m, n]
            if cur_possibilities is not None and len(cur_possibilities) > 1 and value in cur_possibilities:
                cur_possibilities.remove(value)
                board[m, n] = cur_possibilities

    return board


def only_square_possibilities_remover(board: SudokuBoard, possibilities, m, n, value):
    """
    Removes a value from possible options for a cell by checking if that value already exists in a row/column/region
    @param board: The current SudokuBoard of the Competitive Sudoku game
    @param possibilities: The current board containing all possible moves
    @param m: The row-value for the specific region in the SudokuBoard
    @param n: The column-value for the specific region in the SudokuBoard
    @param value: The value that we are checking for
    """
    possibilities = remove_possible_value_row(possibilities, m, value)
    possibilities = remove_possible_value_column(possibilities, n, value)
    possibilities = remove_possible_value_region(possibilities, m, n, board.m, board.n, value)

    return possibilities


def initialize_board(board: SudokuBoard):
    """
    Initializes a board with all possible values per cell
    @param board: The current SudokuBoard of the Competitive Sudoku game
    """

    possible_values_board = np.empty((board.N, board.N), dtype=list)

    # We find the possible legal values for every empty cell on the Sudoku Board (without considering taboo moves)
    for m in range(0, board.N):
        for n in range(0, board.N):
            if is_empty_cell(board, m, n):
                all_moves = list(range(1, board.N+1))
                possible_values = [x for x in all_moves if x not in find_row(board, m)
                                   and x not in find_column(board, n)
                                   and x not in find_region(board, m, n)]
                possible_values_board[m][n] = possible_values

    return possible_values_board


def convert_matrix_into_moves(value_matrix, taboo_moves):
    """
    Converts a numpy matrix into a list of possible moves (also removing taboo moves)
    @param value_matrix: The current matrix containing all possibilities
    @param taboo_moves: A list of all moves marked as taboo by the Oracle
    """

    move_list = []
    for m in range(len(value_matrix)):
        for n in range(len(value_matrix)):
            values = value_matrix[m][n]
            if values is not None:
                for value in values:
                    cur_move = Move(m, n, value)
                    matches_taboo = False
                    for taboo_move in taboo_moves:
                        if cur_move.i == taboo_move.i and cur_move.j == taboo_move.j and cur_move.value == taboo_move.value:
                            matches_taboo = True
                            break
                    if not matches_taboo:
                        move_list.append(cur_move)

    return move_list


def only_square(board: SudokuBoard, taboo_moves):
    """
    Applies the only square Sudoku rule to remove possibilities (see https://www.sudokudragon.com/sudokustrategy.htm)
    @param board: The current SudokuBoard of the Competitive Sudoku game
    @param taboo_moves: A list of all moves marked as taboo by the Oracle
    """

    # First we initialize a Numpy matrix containing all possbile moves (unfiltered)
    possible_values_board = initialize_board(board)

    # Then, for every cell, we check what values are possible, and then remove some using the only square Sudoku rule
    for m in range(0, board.N):
        for n in range(0, board.N):
            possible_values = possible_values_board[m][n]
            if possible_values is not None:  # None means its an already filled-in square
                if len(possible_values) == 1:
                    possible_values_board = only_square_possibilities_remover(board, possible_values_board, m, n, possible_values[0])

    # Finally, we convert the Numpy matrix into a list of possible & legal moves
    return convert_matrix_into_moves(possible_values_board, taboo_moves)
