from team21_A1.helper_functions import get_legal_moves, calculate_new_game_state
from competitive_sudoku.sudoku import GameState, Move


class Node:
    def __init__(self, score: int = None, move: Move = None, game_state: GameState = None, father=None):
        self.score = score
        self.move = move
        self.game_state = game_state
        self.father = father
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# There should be a tree for every (currently possible) move, not just one tree for all moves
# This is both easier, and allows us to check which move is best by accessing the root (instead of through parent)
class Tree:
    def __init__(self, root_moves, cur_game_state):
        self.root = []
        for cur_move in root_moves:
            # TODO: Get value of move through eval function
            self.root.append(Node(score=-123456789, move=cur_move, game_state=cur_game_state))

    def add_layer(self):
        for node in self.root:
            self.add_children(node)

    def add_children(self, parent_node: Node):
        # Recursively find leaf nodes
        if len(parent_node.children) > 0:
            for child in parent_node.children:
                self.add_children(child)
        # This is a leaf node, so we need to expand it
        else:
            possible_moves = get_legal_moves(parent_node.game_state)

            for cur_move in possible_moves:
                cur_game_state = calculate_new_game_state(parent_node.game_state, cur_move)
                # TODO: Get value of move through eval function
                cur_score = 0

                node = Node(score=cur_score, move=cur_move, game_state=cur_game_state, father=parent_node)
                parent_node.add_child(node)


# This is more for form than for functionality, could honestly be turned into loose functions like helperFunctions.py
class ABSearch:
    def __init__(self, tree: Tree):
        self.tree = tree

    def find_best_move(self):
        best_move = None
        best_score = -987654321
        for root_node in self.tree.root:
            root_node.score = self.alpha_beta_prune(root_node)
            if root_node.score > best_score:
                best_score = root_node.score
                best_move = root_node.move

        return best_move

    def alpha_beta_prune(self, root_node: Node):
        alpha = -999999999
        beta = 999999999

        possible_moves = self.get_children(root_node)
        for move in possible_moves:
            score = self.min_beta(move, alpha, beta)
            if score > alpha:
                alpha = score
        return alpha

    def min_beta(self, node: Node, alpha, beta):
        if self.is_leaf(node):
            return self.node_score(node)
        else:
            score = 999999999
            possible_moves = self.get_children(node)
            for move in possible_moves:
                score = min(score, self.max_alpha(move, alpha, beta))
                if score <= alpha:
                    return score
                beta = min(beta, score)

        return score

    def max_alpha(self, node: Node, alpha, beta):
        if self.is_leaf(node):
            return self.node_score(node)
        else:
            score = -999999999
            possible_moves = self.get_children(node)
            for move in possible_moves:
                score = max(score, self.min_beta(move, alpha, beta))
                if score >= beta:
                    return score
                alpha = max(alpha, score)

        return score

    def get_children(self, node: Node):
        return node.children

    def is_leaf(self, node: Node):
        return node.children == []

    def node_score(self, node: Node):
        return node.score
