from team21_A2.helper_functions import get_legal_moves, calculate_new_game_board, is_board_full
from team21_A2.evaluation import evaluate_move
from competitive_sudoku.sudoku import SudokuBoard, Move


class Node:
    def __init__(self, score: int = None, move: Move = None, game_board: SudokuBoard = None, father=None, our_move=None):
        self.score = score
        self.move = move
        self.game_board = game_board
        self.father = father
        self.children = []
        self.our_move = our_move
        self.full_board = is_board_full(self.game_board)

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def is_leaf(self):
        return self.children == []

    def node_score(self):
        return self.score

    def evaluate(self):
        self.score = evaluate_move(self.game_board, self.move, self.our_move, self.score)


# There should be a tree for every (currently possible) move, not just one tree for all moves
# This is both easier, and allows us to check which move is best by accessing the root (instead of through parent)
class Tree:
    def __init__(self, root_moves, taboo_moves, future_taboo_moves, cur_game_state, init_score):
        self.root = []
        self.taboo_moves = taboo_moves
        self.future_taboo_moves = future_taboo_moves
        self.init_score = init_score
        for cur_move in root_moves:
            new_game_board = calculate_new_game_board(cur_game_state.board, cur_move)
            cur_node = Node(score=init_score, move=cur_move, game_board=new_game_board, our_move=True)
            cur_node.evaluate()

            self.root.append(cur_node)

    def add_layer(self):
        for node in self.root:
            self.add_children(node)

    def add_children(self, parent_node: Node):
        # Find leaf nodes:
        # If it has children, it is NOT a leaf node, so check its' children for leaf nodes
        if len(parent_node.children) > 0:
            for child in parent_node.children:
                self.add_children(child)
        # This is a leaf node, so we need to expand it
        else:
            # If the board is full this move, we can't add anything meaningful to its' children, so we don't
            if parent_node.full_board:
                return
            else:
                # Add all possible moves of the current node to the list of children of this node, split in future taboo & non-taboo moves
                non_taboo_moves, future_taboo_moves = get_legal_moves(parent_node.game_board, self.taboo_moves)
                for cur_move in non_taboo_moves:

                    cur_game_board = calculate_new_game_board(parent_node.game_board, cur_move)

                    cur_node = Node(score=parent_node.score, move=cur_move, game_board=cur_game_board,
                                    father=parent_node, our_move=not parent_node.our_move)
                    cur_node.evaluate()

                    parent_node.add_child(cur_node)
                    #print("Non-taboo: " + str(cur_node.our_move) + " - " + str(cur_node.score) + " - " + str(cur_move.i) + "," + str(cur_move.j) + "," + str(cur_move.value))

                for cur_move in future_taboo_moves:

                    cur_game_board = parent_node.game_board
                    cur_node = Node(score=parent_node.score, move=cur_move, game_board=cur_game_board,
                                    father=parent_node, our_move=not parent_node.our_move)

                    parent_node.add_child(cur_node)
                    #print("Taboo: " + str(cur_node.our_move) + " - " + str(cur_node.score) + " - " + str(cur_move.i) + "," + str(cur_move.j) + "," + str(cur_move.value))


def find_best_move(tree):
    best_node = None
    best_score = -987654321
    for root_node in tree.root:
        root_node.score = min_beta(root_node, -999, 999)

        if root_node.score > best_score:
            best_score = root_node.score
            best_node = root_node
    print("New score with best move: " + str(best_score))
    if best_score == -987654321:  # No move found: We have the last move of the game
        return
    else:
        return best_node.move


def min_beta(node: Node, alpha, beta):
    if node.is_leaf():
        return node.node_score()
    else:
        score = 999999999
        for node in node.get_children():
            score = min(score, max_alpha(node, alpha, beta))
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score


def max_alpha(node: Node, alpha, beta):
    if node.is_leaf():
        return node.node_score()
    else:
        score = -999999999
        for node in node.get_children():
            score = max(score, min_beta(node, alpha, beta))
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score
