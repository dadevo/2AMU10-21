from team21_A2.helper_functions import check_legal_column, check_legal_region, check_legal_row


def evaluate_move(game_board, move, our_move, score):

    count = 0 
    if check_legal_row(game_board, move.i, 0):
        count += 1
    if check_legal_column(game_board, move.j, 0):
        count += 1      
    if check_legal_region(game_board, move.i, move.j, 0):
        count += 1

    if count == 0:
        player_score = 0
    elif count == 1:
        player_score = 1
    elif count == 2:
        player_score = 3
    else:
        player_score = 7
    
    if our_move:
        return score + player_score
    else:
        return score - player_score
