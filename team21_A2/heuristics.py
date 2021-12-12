from competitive_sudoku.sudoku import GameState
from team21_A2.helper_functions import is_legal_move, is_empty_cell


def hidden_twin_exclusion(game_state: GameState, moves: list):
    """
    Returns a filtered list of moves using the hidden twin exclusion.
    @param board: A sudoku board. It contains the current position of a game.
    @param list: A list of moves to evaluate.
    """
    filtered_moves = []
    twins = {}

    # O(m*m*n*n*N*N) == O(N^4) Pretty shit
    for m in range(game_state.board.m):  # O(m)
        row_start_index = m * game_state.board.m
        row_end_index = game_state.board.m + (m * game_state.board.m)

        for n in range(game_state.board.n):  # O(n)
            column_start_index = n * game_state.board.n
            column_end_index = game_state.board.n + (n * game_state.board.n)

            # Check per region if there are hidden twins
            # TODO: Improve this by using the passed on moves!!!
            potential_twins = {}
            for i in range(row_start_index, row_end_index):  # O(m)
                for j in range(column_start_index, column_end_index):  # O(n)
                    # if the cell is not empty we can skip evaluating values
                    if not is_empty_cell(game_state.board, i, j):
                        continue
                    else:
                        # Try all possible values [1, ..., N] for a cell
                        for k in range(1, game_state.board.N + 1):  # O(N)
                            # If a move is legal append to list of legal moves
                            if is_legal_move(game_state, i, j, k): # O(N)
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
                continue
        else:
            filtered_moves.append(move)

    return filtered_moves
