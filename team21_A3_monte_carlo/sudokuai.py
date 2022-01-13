#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

from competitive_sudoku.sudoku import GameState
import competitive_sudoku.sudokuai
from team21_A3_monte_carlo.tree_search import get_heuristic_moves
from team21_A3_monte_carlo.evaluation import evaluate_move
from team21_A3_monte_carlo.monte_carlo import monte_carlo
import math


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

    def compute_best_move(self, game_state: GameState) -> None:
        """
        Sends the move that our agent should play whenever we find a good move
        @param game_state: The current GameState of the Competitive Sudoku game
        """

        # Get all legal moves, split by whether we know that the Oracle will call them taboo (but not disqualify us)
        legal_moves, legal_taboo_move = get_heuristic_moves(
            game_state.board, game_state.taboo_moves)

        # Check what player we are by the length of the GameStates' list of moves,
        # and calculate how well we are doing based on that and the current score of both players
        what_player_are_we = len(game_state.moves) % 2
        if what_player_are_we == 1:
            initial_scores = game_state.scores[1]-game_state.scores[0]
        else:
            initial_scores = game_state.scores[0]-game_state.scores[1]

        # Propose a move, so the agent does not get disqualified
        best_move = legal_moves[0]
        self.propose_move(best_move)

        # Now at least check which move gives us the most points (we are now at the level of the greedy_player agent)
        best_score = -math.inf
        for cur_move in legal_moves[0:]:
            score = evaluate_move(
                game_state.board, cur_move, True, initial_scores)
            if score > best_score:
                best_move = cur_move
        self.propose_move(best_move)

        monte_carlo(game_state.board, what_player_are_we,
                    legal_moves, self.propose_move)
