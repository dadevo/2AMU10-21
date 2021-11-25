from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove

def isLegalMove(self, game_state: GameState, n, m, x):
    """
    Checks if the current move would disqualify you from the game
    @param game_state: The current game state of type GameState
    @param m: A row value in the range [0, ..., N)
    @param n: A column value in the range [0, ..., N)
    @param x: A value in the range [1, ..., N]
    """
    row = getRow(m)
    column = getColumn(n)
    block = getBlock(m, n)
    empty = isEmpty(m, n)
    #Move would disqualify you if:
    #1. Proposed number already in your coordinates' existing row/column/block
    #2. The coordinate is already filled in
    #3. The move is in taboo moves
    if x not in row and x not in column and x not in block and empty and not TabooMove(n, m, x) in game_state.taboo_moves:
        return True
    else:
        return False

def getRow(self, game_state: GameState, m):
    """
    Returns the m-th row of the board.
    @param game_state: The current game state of type GameState
    @param m: A row value in the range [0, ..., N)
    """
    row = []
    for n in range(0, game_state.board.N):
        row.append(game_state.board.get(m, n))
    return row


def getColumn(self, game_state: GameState, n):
    """
    Returns the n-th column of the board.
    @param game_state: The current game state of type GameState
    @param n: A column value in the range [0, ..., N)
    """
    column = []
    for m in range(0, game_state.board.N):
        column.append(game_state.board.get(m, n))
    return column


def getBlock(self, game_state: GameState, m, n):
    """
    Returns block that contains the intersection of row m and column n.
    @param game_state: The current game state of type GameState
    @param m: A row value in the range [0, ..., N)
    @param n: A column value in the range [0, ..., N)
    """
    rowBlock = m // game_state.board.m
    colBlock = n // game_state.board.n
    block = []
    for m in range(rowBlock * game_state.board.m - 1, (rowBlock + 1) * game_state.board.m):
        for n in range(colBlock * game_state.board.n - 1, (colBlock + 1) * game_state.board.n):
            block.append(game_state.board.get(m, n))
    return block

def isEmpty(self, game_state: GameState, m, n):
    if game_state.board.get(m, n) == 0:
        return True
    else:
        return False