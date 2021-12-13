from competitive_sudoku.sudoku import SudokuBoard


def hidden_twin_exclusion(game_board: SudokuBoard, taboo_moves, moves: list):
    """
    Returns a filtered list of moves using the hidden twin exclusion.
    @param game_board: A sudoku board. It contains the current position of a game.
    @param taboo_moves: The list of current taboo moves
    @param moves: A list of moves to evaluate.
    """
    filtered_moves = []
    new_taboo_moves = []
    twins = {}

    # O(m*m*n*n*N*N) == O(N^4) Pretty shit
    for m in range(game_board.m):  # O(m)
        row_start_index = m * game_board.m
        row_end_index = game_board.m + (m * game_board.m)

        for n in range(game_board.n):  # O(n)
            column_start_index = n * game_board.n
            column_end_index = game_board.n + (n * game_board.n)

            # Check per region if there are hidden twins
            # TODO: Improve this by using the passed on moves!!!
            potential_twins = {}
            for i in range(row_start_index, row_end_index):  # O(m)
                for j in range(column_start_index, column_end_index):  # O(n)
                    # if the cell is not empty we can skip evaluating values
                    if not game_board.get(i, j) == 0:  # Had to remove call to is_empty_cell because of circular dependency
                        continue
                    else:
                        # Try all possible values [1, ..., N] for a cell
                        for k in range(1, game_board.N + 1):  # O(N)
                            # If a move is legal append to list of legal moves <- is always legal, we pass only legal moves. so commented out
                            # if is_legal_move(game_board, taboo_moves, i, j, k): # O(N)
                            if (i, j) in potential_twins:
                                potential_twins[(i, j)].append(k)
                            else:
                                potential_twins[(i, j)] = [k]
            
            # Check if the potential twins are valid
            for k, v in potential_twins.items():
                for k_, v_ in potential_twins.items():
                    if k != k_:
                        # Only handling twins atm
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
