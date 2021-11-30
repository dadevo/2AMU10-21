from helper_functions import get_legal_moves, calculate_new_game_state


class Node:
    def __init__(self, node_id=None, score=None, move=None, game_state=None, max=True, father=None):
        self.node_id = node_id
        self.score = score
        self.move = move
        self.game_state = game_state
        self.max = max  # True = max, False = min    #TODO: Currently not used, is done in AB-searching
        self.father = father
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# There should be a tree for every (currently possible) move, not just one tree for all moves
# This is both easier, and allows us to check which move is best by accessing the root (instead of through parent)
# Also, give the root id = 0
# TODO: Check if node ID is actually useful
class Tree:
    def __init__(self, root_node):
        self.root = root_node
        self.next_node_id = 1

    def calculate_deeper(self, parent_node):
        # Root case
        possible_moves = get_legal_moves(parent_node.game_state)

        for cur_move in possible_moves:
            cur_game_state = calculate_new_game_state(parent_node.game_state, cur_move)
            # TODO: Get value of move through eval function
            cur_score = 0

            node = Node(node_id=self.next_node_id, score=cur_score, move=cur_move, game_state=cur_game_state,
                        max=not parent_node.max, father=parent_node)
            parent_node.add_child(node)
            self.next_node_id += 1

class ABSearch:
    def __init__(self, tree):
        self.tree = tree
        self.root = tree.root

    def alpha_beta_prune(self, node):
        alpha = -999999999
        beta = 999999999

        possible_moves = self.get_children(node)
        best_move = None
        for move in possible_moves:
            score = self.min(move, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = move
        return best_move  # Maybe also score?

    def min_beta(self, node, alpha, beta):
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

    def max_alpha(self, node, alpha, beta):
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

    def get_children(self, node):
        return node.children

    def is_leaf(self, node):
        return node.children == []

    def node_score(self, node):
        return node.score
