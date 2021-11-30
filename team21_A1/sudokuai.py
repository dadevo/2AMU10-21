#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove
import competitive_sudoku.sudokuai
from team21_A1.helper_functions import get_legal_moves
from team21_A1.tree_search import Node, Tree, ABSearch


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N

        # Get all legal moves
        legal_moves = get_legal_moves(game_state)

        # oh god just submit a good move who cares about depth searching
        best_move = legal_moves[0]  # TODO: Is there a nicer way to do this?
        best_score = -999999999 # TODO: Calculate move score here
        for cur_move in legal_moves[1:]:
            # TODO: Calculate move score here, or maybe even make a Move class extension to include score?
            score = 0
            if score > best_score:
                best_move = cur_move

        self.propose_move(best_move)

        # Now we start doing search tree stuff and offering a new move every depth
        search_tree = ABSearch(Tree(legal_moves, game_state))
        while True:
            # Extend the depth of the trees by 1
            search_tree.tree.add_layer()

            # Return best move in tree for current depth
            best_move = search_tree.find_best_move()
            self.propose_move(best_move)


