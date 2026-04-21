# import random
#
#
# # Hàm đánh giá bàn cờ: AI sẽ ưu tiên ăn nhiều quân và bảo vệ ô quan của mình
# def evaluate(board, scores, player_ai):
#     # Điểm AI = (Điểm hiện có) + (Số quân đang nằm trên phía sân của mình)
#     # Trừ đi điểm của đối thủ
#     opponent = 1 - player_ai
#
#     # AI muốn tổng điểm của mình cao nhất
#     score_val = scores[player_ai] - scores[opponent]
#
#     # Cộng thêm điểm từ quân trên sân (để AI rải quân thông minh hơn)
#     player_pits = [1, 2, 3, 4, 5] if player_ai == 0 else [7, 8, 9, 10, 11]
#     # score_val += sum(board[i] for i in player_pits) * 0.5
#     score_val += sum(board[i]["dan"] for i in player_pits) * 0.5
#
#     return score_val
#
#
# def get_best_move(board, scores, player_ai, move_func):
#     """
#     Tìm nước đi tốt nhất cho AI
#     move_func: truyền hàm move từ file chính vào để AI giả lập nước đi
#     """
#     # valid_pits = [i for i in ([7, 8, 9, 10, 11] if player_ai == 1 else [1, 2, 3, 4, 5]) if board[i] > 0]
#     valid_pits = [i for i in ([7, 8, 9, 10, 11] if player_ai == 1 else [1, 2, 3, 4, 5]) if board[i]["dan"] > 0]
#
#     if not valid_pits:
#         return None, None
#
#     best_score = -float('inf')
#     best_move = (valid_pits[0], 1)  # Mặc định
#
#     for pit in valid_pits:
#         for direction in [1, -1]:
#             # Giả lập nước đi
#             # move_func trả về danh sách các frames, ta chỉ lấy frame cuối cùng [-1]
#             frames = move_func(board, scores, player_ai, pit, direction)
#             final_board, final_scores = frames[-1]
#
#             # Đánh giá kết quả sau khi đi thử
#             current_score = evaluate(final_board, final_scores, player_ai)
#
#             if current_score > best_score:
#                 best_score = current_score
#                 best_move = (pit, direction)
#             elif current_score == best_score:
#                 # Nếu điểm bằng nhau, chọn ngẫu nhiên để AI không bị máy móc
#                 if random.random() > 0.5:
#                     best_move = (pit, direction)
#
#     return best_move  # Trả về (ô chọn, hướng)



import random
import copy

DEPTH = 5  # Tăng lên nếu muốn AI mạnh hơn (nhưng chậm hơn)


def evaluate(board, scores, player_ai):
    opponent = 1 - player_ai

    # 1. Hiệu điểm cơ bản
    score_val = (scores[player_ai] - scores[opponent]) * 10

    # 2. Quân trên sân của mình (lợi thế tài nguyên)
    player_pits = [1, 2, 3, 4, 5] if player_ai == 0 else [7, 8, 9, 10, 11]
    opp_pits    = [7, 8, 9, 10, 11] if player_ai == 0 else [1, 2, 3, 4, 5]
    score_val += sum(board[i]["dan"] for i in player_pits) * 0.5

    # 3. Phạt nếu ô ngay trước quan đối thủ có nhiều quân
    # (đối thủ sẽ ăn được nhiều nếu đi đúng hướng)
    quan_opp = 6 if player_ai == 0 else 0
    pre_quan_opp = (quan_opp - 1) % 12
    score_val -= board[pre_quan_opp]["dan"] * 0.3

    # 4. Thưởng nếu có thể ăn ngay (ô trống rồi đến ô có quân)
    for i in player_pits:
        if board[i]["dan"] == 0:
            # Ô kế tiếp (cả 2 hướng) có quân → có thể ăn
            next_cw  = (i + 1) % 12
            next_ccw = (i - 1) % 12
            if board[next_cw]["dan"] > 0:
                score_val += board[next_cw]["dan"] * 0.4
            if board[next_ccw]["dan"] > 0:
                score_val += board[next_ccw]["dan"] * 0.4

    return score_val


def minimax(board, scores, current_player, player_ai, depth,
            alpha, beta, move_func):
    """
    Minimax với Alpha-Beta Pruning.
    - current_player: người đang đến lượt trong nhánh giả lập
    - player_ai: AI gốc (cố định để evaluate đúng góc nhìn)
    """
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