from os import lseek
from competitive_sudoku.sudoku import SudokuBoard
from team21_A1.helper_functions import check_legal_row, check_legal_region, check_legal_column

def list_empty_cells(board: SudokuBoard):
    """
    returns a list of coordinates which are empty on the sudokuboard
    @param game_state: A sudoku board. It contains the current position of a game.
    """
    empty_cells = []
    for m in range(board.m):
        for n in range(board.n):
            if board.get(m, n) == 0:
                empty_cells.append(board.rc2f(m, n))
    return empty_cells

def check_column_values(board: SudokuBoard, n):
    """
    Returns whether a list of values for a column.
    @param board: A sudoku board. It contains the current position of a game.
    @param n: A column value in the range [0, ..., N).
    """
    column = []

    for m in range(board.N):
        column.append(board.get(m, n))

    return column

def check_row_values(board: SudokuBoard, m):
    """
    Returns whether a list of values for a row.
    @param board: A sudoku board. It contains the current position of a game.
    @param m: A row value in the range [0, ..., N).
    """
    row = []

    for n in range(board.N):
        row.append(board.get(m, n))

    return row

def check_region_values(board: SudokuBoard, m, n):
    """
    Returns whether a list of values for a region.
    @param board: A sudoku board. It contains the current position of a game.
    @param n: A column value in the range [0, ..., N).
    @param m: A row value in the range [0, ..., N).
    """

    row_region_index = (m // board.m) * board.m
    column_region_index = (n // board.n) * board.n
    region = []

    for m_i in range(row_region_index, row_region_index + board.m):
        for n_i in range(column_region_index, column_region_index + board.n):
            region.append(board.get(m_i, n_i))

    return region

def get_smallest_group(board: SudokuBoard, i, j):
    """"
    Returns 0 if there are more squares filled in the column,
    returns 1 if there are more squares filled in the row 
    and 2 if there are more squares filled in the region of a certain index
    @param board: A sudoku board. It contains the current position of a game.
    @param i: An index of a row in the range [0, ..., N]
    @param i: An index of a column in the range [0, ..., N]
    """
    row_list = check_row_values(board, i)
    empty_count_row = row_list.count(0)
    column_list = check_column_values(board, j)
    empty_count_column = column_list.count(0)
    region_list = check_region_values(board, i, j)
    empty_count_region = region_list.count(0)
    groups = (empty_count_column, empty_count_row, empty_count_region)
    min_group = min(groups)
    return groups.index(min_group)


def missing_value_group(board: SudokuBoard, i, j):
    """"
    Returns the smallest list of possible values we can input in the i,j coordinate
    @param board: A sudoku board. It contains the current position of a game.
    @param i: An index of a row in the range [0, ..., N]
    @param i: An index of a column in the range [0, ..., N]
    """
    group_id = get_smallest_group(board, i, j)
    # Group id's correspond to which group contains the least empty cells
    if group_id == 0:
        value_list = check_column_values(board, j)
    if group_id == 1:
        value_list = check_row_values(board, i)
    if group_id == 2:
        value_list = check_region_values(board, i, j)
    complete_list = []
    for value in range(board.N):
        # List of values that should be in a complete group
        complete_list.append(value)
    diff_list = list(set(complete_list) - set(value_list))
    return diff_list

def only_square(board: SudokuBoard):
    """"
    Executes a move on the board according to the "only square" rule
    if it is legal move.
    @param board: A sudoku board. It contains the current position of a game.
    @param i: An index of a row in the range [0, ..., N]
    @param i: An index of a column in the range [0, ..., N]
    """
    empty_cells = list_empty_cells(board)
    # Get all empty cells on the board
    for cell in empty_cells:
        i, j = board.f2rc(cell)
        missing_values = missing_value_group(board, i, j)
        # convert them into coordinates and get the smallest list of missing values
        for value in missing_values:
            if (check_legal_column(board, j, value) == True and check_legal_row(board, i, value) == True and check_legal_region(board, i , j, value) == True):
                # executes the move but we can also just add it to a list
                board.put(i, j, value)
            else:
                pass