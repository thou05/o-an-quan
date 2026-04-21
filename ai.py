import random


# Hàm đánh giá bàn cờ: AI sẽ ưu tiên ăn nhiều quân và bảo vệ ô quan của mình
def evaluate(board, scores, player_ai):
    # Điểm AI = (Điểm hiện có) + (Số quân đang nằm trên phía sân của mình)
    # Trừ đi điểm của đối thủ
    opponent = 1 - player_ai

    # AI muốn tổng điểm của mình cao nhất
    score_val = scores[player_ai] - scores[opponent]

    # Cộng thêm điểm từ quân trên sân (để AI rải quân thông minh hơn)
    player_pits = [1, 2, 3, 4, 5] if player_ai == 0 else [7, 8, 9, 10, 11]
    # score_val += sum(board[i] for i in player_pits) * 0.5
    score_val += sum(board[i]["dan"] for i in player_pits) * 0.5

    return score_val


def get_best_move(board, scores, player_ai, move_func):
    """
    Tìm nước đi tốt nhất cho AI
    move_func: truyền hàm move từ file chính vào để AI giả lập nước đi
    """
    # valid_pits = [i for i in ([7, 8, 9, 10, 11] if player_ai == 1 else [1, 2, 3, 4, 5]) if board[i] > 0]
    valid_pits = [i for i in ([7, 8, 9, 10, 11] if player_ai == 1 else [1, 2, 3, 4, 5]) if board[i]["dan"] > 0]

    if not valid_pits:
        return None, None

    best_score = -float('inf')
    best_move = (valid_pits[0], 1)  # Mặc định

    for pit in valid_pits:
        for direction in [1, -1]:
            # Giả lập nước đi
            # move_func trả về danh sách các frames, ta chỉ lấy frame cuối cùng [-1]
            frames = move_func(board, scores, player_ai, pit, direction)
            final_board, final_scores = frames[-1]

            # Đánh giá kết quả sau khi đi thử
            current_score = evaluate(final_board, final_scores, player_ai)

            if current_score > best_score:
                best_score = current_score
                best_move = (pit, direction)
            elif current_score == best_score:
                # Nếu điểm bằng nhau, chọn ngẫu nhiên để AI không bị máy móc
                if random.random() > 0.5:
                    best_move = (pit, direction)

    return best_move  # Trả về (ô chọn, hướng)