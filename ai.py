import random
import copy

DEPTH = 5  # Tăng lên nếu muốn AI mạnh hơn (nhưng chậm hơn)


def evaluate(board, scores, player_ai):
    opponent = 1 - player_ai

    score_val = (scores[player_ai] - scores[opponent]) * 10

    # Quân trên sân của mình
    player_pits = [1, 2, 3, 4, 5] if player_ai == 0 else [7, 8, 9, 10, 11]
    opp_pits    = [7, 8, 9, 10, 11] if player_ai == 0 else [1, 2, 3, 4, 5]
    score_val += sum(board[i]["dan"] for i in player_pits) * 0.5

    # Phạt nếu ô ngay trước quan đối thủ có nhiều quân
    quan_opp = 6 if player_ai == 0 else 0
    pre_quan_opp = (quan_opp - 1) % 12
    score_val -= board[pre_quan_opp]["dan"] * 0.3

    # Thưởng nếu có thể ăn ngay
    for i in player_pits:
        if board[i]["dan"] == 0:
            next_cw  = (i + 1) % 12
            next_ccw = (i - 1) % 12
            if board[next_cw]["dan"] > 0:
                score_val += board[next_cw]["dan"] * 0.4
            if board[next_ccw]["dan"] > 0:
                score_val += board[next_ccw]["dan"] * 0.4

    return score_val


def minimax(board, scores, current_player, player_ai, depth,
            alpha, beta, move_func):
    pits = [1, 2, 3, 4, 5] if current_player == 0 else [7, 8, 9, 10, 11]
    valid_pits = [i for i in pits if board[i]["dan"] > 0]

    # Terminal: hết quân hoặc hết độ sâu
    if depth == 0 or not valid_pits:
        return evaluate(board, scores, player_ai), None

    is_maximizing = (current_player == player_ai)
    best_val  = -float('inf') if is_maximizing else float('inf')
    best_move = None

    for pit in valid_pits:
        for direction in [1, -1]:
            frames = move_func(board, scores, current_player, pit, direction)
            new_board, new_scores = frames[-1]

            val, _ = minimax(
                new_board, new_scores,
                1 - current_player,   # đổi lượt
                player_ai,
                depth - 1,
                alpha, beta,
                move_func
            )

            if is_maximizing:
                if val > best_val:
                    best_val  = val
                    best_move = (pit, direction)
                alpha = max(alpha, val)
            else:
                if val < best_val:
                    best_val  = val
                    best_move = (pit, direction)
                beta = min(beta, val)

            # Cắt tỉa
            if beta <= alpha:
                break

    return best_val, best_move


def get_best_move(board, scores, player_ai, move_func):
    """Giao diện chính — thay thế hàm cũ, dùng Minimax."""
    pits = [1, 2, 3, 4, 5] if player_ai == 0 else [7, 8, 9, 10, 11]
    if not any(board[i]["dan"] > 0 for i in pits):
        return None

    _, best_move = minimax(
        board, scores,
        player_ai,          # AI đi trước
        player_ai,
        DEPTH,
        -float('inf'), float('inf'),
        move_func
    )

    return best_move  # (pit, direction)