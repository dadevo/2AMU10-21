#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

from competitive_sudoku.sudoku import GameState
import competitive_sudoku.sudokuai
from team21_A2.helper_functions import get_legal_moves
from team21_A2.tree_search import Tree, find_best_move
from team21_A2.evaluation import evaluate_move
# import cProfile


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

    def compute_best_move(self, game_state: GameState) -> None:

        # Get all legal moves
        legal_moves, legal_taboo_moves = get_legal_moves(game_state.board, game_state.taboo_moves)

        what_player_are_we = len(game_state.moves) % 2
        if what_player_are_we == 1:
            initial_scores = game_state.scores[1]-game_state.scores[0]
        else:
            initial_scores = game_state.scores[0]-game_state.scores[1]

        # oh god just submit a move who cares about depth searching
        best_move = legal_moves[0]
        self.propose_move(best_move)

        best_score = -999
        for cur_move in legal_moves[0:]:
            score = evaluate_move(game_state.board, cur_move, True, initial_scores)
            if score > best_score:
                best_move = cur_move
        self.propose_move(best_move)

        # Now we start doing search tree stuff and offering a new move every depth
        search_tree = Tree(legal_moves, game_state.taboo_moves, legal_taboo_moves, game_state, initial_scores)
        depth = 0
        search_tree.add_layer()

        while depth < 5:
            depth += 1
            if depth > 15:
                break

            # Return best move in tree for current depth
            best_move = find_best_move(search_tree)
            print("Best move at tree depth " + str(depth) + " found, increasing depth")
            self.propose_move(best_move)

            # Extend the depth of the trees by 1 (1 being both our move and the other agents' moves combined)
            # Debugging, ignore: cProfile.runctx('search_tree.add_layer()', None, locals())
            search_tree.add_layer()
            search_tree.add_layer()

