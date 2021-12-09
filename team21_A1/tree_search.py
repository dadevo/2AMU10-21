from team21_A1.helper_functions import get_legal_moves, calculate_new_game_state, is_board_full
from team21_A1.evaluation import evaluate_move
from competitive_sudoku.sudoku import GameState, Move


class Node:
    def __init__(self, score: int = None, move: Move = None, game_state: GameState = None, father=None, our_move=True):
        self.score = score
        self.move = move
        self.game_state = game_state
        self.father = father
        self.children = []
        self.our_move = our_move
        self.full_board = is_board_full(self.game_state.board)

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def is_leaf(self):
        return self.children == []

    def node_score(self):
        return self.score

    def evaluate(self):
        self.score = evaluate_move(self.game_state, self.move, self.our_move, self.score)


# There should be a tree for every (currently possible) move, not just one tree for all moves
# This is both easier, and allows us to check which move is best by accessing the root (instead of through parent)
class Tree:
    def __init__(self, root_moves, cur_game_state, init_score):
        self.root = []
        self.init_score = init_score
        for cur_move in root_moves:
            new_game_state = calculate_new_game_state(cur_game_state, cur_move)
            cur_node = Node(score=init_score, move=cur_move, game_state=new_game_state)
            cur_node.evaluate()

            self.root.append(cur_node)

    def add_layer(self):
        for node in self.root:
            self.add_children(node)

    def add_children(self, parent_node: Node):
        # Recursively find leaf nodes:
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
                # Add all possible moves of the current node to the list of children of this node
                possible_moves = get_legal_moves(parent_node.game_state)
                for cur_move in possible_moves:

                    cur_game_state = calculate_new_game_state(parent_node.game_state, cur_move)
                    cur_node = Node(score=parent_node.score, move=cur_move, game_state=cur_game_state, father=parent_node, our_move=not parent_node.our_move)
                    cur_node.evaluate()

                    parent_node.add_child(cur_node)


def find_best_move(tree):
    best_node = None
    best_score = -987654321
    for root_node in tree.root:
        root_node.score = alpha_beta_prune(root_node)

        if root_node.score > best_score:
            best_score = root_node.score
            best_node = root_node
    print("Best move score: " + str(best_score))
    if best_score == -987654321:  # No move found: We have the last move of the game
        return
    else:
        return best_node.move


def alpha_beta_prune(root_node: Node):
    alpha = -999999999
    beta = 999999999

    for node in root_node.get_children():
        score = min_beta(node, alpha, beta)
        if score > alpha:
            alpha = score
    return alpha


def min_beta(node: Node, alpha, beta):
    if node.is_leaf():
        return node.node_score()
    else:
        score = 999999999
        for node in node.get_children():
            score = min(score, max_alpha(node, alpha, beta))
            beta = min(beta, score)
            if score <= alpha:
                return score

        return score


def max_alpha(node: Node, alpha, beta):
    if node.is_leaf():
        return node.node_score()
    else:
        score = -999999999
        for node in node.get_children():
            score = max(score, min_beta(node, alpha, beta))
            alpha = max(alpha, score)
            if score >= beta:
                return score

        return score
