from competitive_sudoku.sudoku import SudokuBoard

def calculate_region_index(board: SudokuBoard, m, n):
    row_region_index = (m // board.m) * board.m
    column_region_index = (n // board.n) * board.n

    return (row_region_index, column_region_index)

def hidden_twin_exclusion(board: SudokuBoard, taboo_moves: list, moves: list):
    """
    Returns a filtered list of moves using the hidden twin exclusion.
    @param board: A sudoku board. It contains the current position of a game.
    @param moves: A list of moves to evaluate.
    """
    filtered_moves = []
    new_taboo_moves = []
    potential_twins = {}
    twins = {}

    # Store the moves in a dictionary where the key is the position of the move
    # and the value is a list of possible values
    for m in moves:
        position = (m.i, m.j)
        if position in potential_twins:
            potential_twins[position].append(m.value)
        else:
            potential_twins[position] = [m.value]

    # Check if the potential twins are valid by comparing for each position the possible values
    for k, v in potential_twins.items():
        for k_, v_ in potential_twins.items():
            # Check if the two positions are not the same and that they are in the same region
            if k != k_ and calculate_region_index(board, k[0], k[1]) == calculate_region_index(board, k_[0], k_[1]):
                intersection = set(v) & set(v_)
                if len(intersection) == 2:
                    twins[k] = list(intersection)
                    twins[k_] = list(intersection)
            else:
                continue
    
    # Filter out moves using the twins
    for move in moves:
        key = (move.i, move.j)
        if key in twins:
            if move.value in twins[key]:
                filtered_moves.append(move)
            else:
                new_taboo_moves.append(move)
        else:
            filtered_moves.append(move)

    new_taboo_moves.extend(taboo_moves)

    return filtered_moves, new_taboo_moves


def run_heuristics(game_board: SudokuBoard, taboo_moves, moves):
    # filtered_moves = []
    # future_taboo_moves = []

    hf, ht = hidden_twin_exclusion(game_board, taboo_moves, moves)
    # future_taboo_moves = merge_uniques_in_lists(future_taboo_moves, ht)
    # filtered_moves = merge_uniques_in_lists(filtered_moves, hf)

    return hf, ht


def merge_uniques_in_lists(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    uniques_2 = set2-set1
    return list1+list(uniques_2)
