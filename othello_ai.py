import copy

BOARD_SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1), (1, 0),  (1, 1)]

def init_board():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2
    return board

def is_on_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def get_valid_moves(board, player):
    opponent = 3 - player
    valid_moves = []

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] != 0:
                continue
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                found_opponent = False
                while is_on_board(nx, ny) and board[nx][ny] == opponent:
                    nx += dx
                    ny += dy
                    found_opponent = True
                if found_opponent and is_on_board(nx, ny) and board[nx][ny] == player:
                    valid_moves.append([x, y])
                    break
    return valid_moves

def apply_move(board, x, y, player):
    board = copy.deepcopy(board)
    board[x][y] = player
    opponent = 3 - player

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        pieces_to_flip = []

        while is_on_board(nx, ny) and board[nx][ny] == opponent:
            pieces_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if is_on_board(nx, ny) and board[nx][ny] == player:
            for px, py in pieces_to_flip:
                board[px][py] = player

    return board

# 簡易評価関数
def evaluate(board, player):
    score = 0
    for row in board:
        for cell in row:
            if cell == player:
                score += 1
            elif cell == 3 - player:
                score -= 1
    return score

# ミニマックス + αβ枝刈り
def minimax(board, depth, player, maximizing, alpha, beta):
    valid_moves = get_valid_moves(board, player)
    if depth == 0 or not valid_moves:
        return evaluate(board, player), None

    best_move = None
    if maximizing:
        max_eval = float("-inf")
        for move in valid_moves:
            new_board = apply_move(board, move[0], move[1], player)
            eval_score, _ = minimax(new_board, depth - 1, 3 - player, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in valid_moves:
            new_board = apply_move(board, move[0], move[1], player)
            eval_score, _ = minimax(new_board, depth - 1, 3 - player, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def ai_move(board, player):
    _, move = minimax(board, depth=3, player=player, maximizing=True, alpha=float("-inf"), beta=float("inf"))
    return move
