import numpy as np
from competitive_sudoku.sudoku import SudokuBoard, Move
from team21_A3.helper_functions import is_empty_cell, find_row, find_column, find_region


def remove_possible_value_row(board, m, value):
    for n in range(len(board)):
        cur_possibilities = board[m, n]
        if cur_possibilities is not None and len(cur_possibilities) > 1 and value in cur_possibilities:
            cur_possibilities.remove(value)
            board[m, n] = cur_possibilities

    return board


def remove_possible_value_column(board, n, value):
    for m in range(len(board)):
        cur_possibilities = board[m, n]
        if cur_possibilities is not None and len(cur_possibilities) > 1 and value in cur_possibilities:
            cur_possibilities.remove(value)
            board[m, n] = cur_possibilities

    return board


def remove_possible_value_region(board, m, n, bm, bn, value):
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

    possibilities = remove_possible_value_row(possibilities, m, value)
    possibilities = remove_possible_value_column(possibilities, n, value)
    possibilities = remove_possible_value_region(possibilities, m, n, board.m, board.n, value)

    return possibilities


def initialize_board(board: SudokuBoard):
    possible_values_board = np.empty((board.N, board.N), dtype=list)

    # We find the possible legal values for every cell on the Sudoku Board (without considering taboo moves)
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

    possible_values_board = initialize_board(board)

    for m in range(0, board.N):
        for n in range(0, board.N):
            possible_values = possible_values_board[m][n]
            if possible_values is not None:  # None means its an already filled-in square
                if len(possible_values) == 1:
                    possible_values_board = only_square_possibilities_remover(board, possible_values_board, m, n, possible_values[0])

    return convert_matrix_into_moves(possible_values_board, taboo_moves)
