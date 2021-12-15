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
    """
    Runs the heuristics on the set of all legal moves, separating moves that can solve the Sudoku board from moves that cannot
    Returns a (hopefully) smaller list of legal moves and a single move that the Oracle would identify as taboo
    @param game_board: The current Sudoku board
    @param taboo_moves: The list of known taboo moves (that will disqualify you)
    @param moves: The list of legal moves (that will not disqualify you)
    """

    filtered_moves = moves
    future_taboo_moves = None

    # We return a filtered list of legal moves, and a taboo move if one was found by the heuristic,
    # and then update our variables with the result
    heuristic_filtered, heuristic_taboo = hidden_twin_exclusion(game_board, taboo_moves, filtered_moves)
    filtered_moves = heuristic_filtered
    if future_taboo_moves is not None and heuristic_taboo is not None:
        future_taboo_moves = heuristic_taboo

    # We can simply repeat the same process for every heuristic, using the filtered list as input for the new heuristic
    heuristic_filtered, heuristic_taboo = hidden_twin_exclusion(game_board, taboo_moves, filtered_moves)
    filtered_moves = heuristic_filtered
    if future_taboo_moves is not None and heuristic_taboo is not None:
        future_taboo_moves = heuristic_taboo

    # Once we've used all the heuristics, we return the filtered list of legal moves and a taboo move (if any).
    return filtered_moves, future_taboo_moves
