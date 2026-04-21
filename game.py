import copy
from constants import *


def init_board():
    board = [{"dan": 0, "quan": 0} for _ in range(N)]

    board[QUAN_L] = {"dan": 0, "quan": 1}
    board[QUAN_R] = {"dan": 0, "quan": 1}

    for i in P1_CELLS:
        board[i]["dan"] = 5
    for i in P2_CELLS:
        board[i]["dan"] = 5
    return board


def get_player_pits(player):
    return P1_CELLS if player == 0 else P2_CELLS


def valid_moves(board, player):
    return [i for i in get_player_pits(player) if board[i]["dan"] > 0]


def refill_if_empty(board, scores, player):
    cells = get_player_pits(player)
    if all(board[i]["dan"] == 0 for i in cells):
        if scores[player] >= 5:
            for i in cells:
                board[i]["dan"] = 1
            scores[player] -= 5
            print(f"Player {player} rải lại 5 quân")
        else:
            print(f"Player {player} không đủ quân để rải lại!")
            return False
    return True


def move(board, scores, player, cell, direction):
    board = copy.deepcopy(board)
    scores = list(scores)

    # Mảng chứa các "khung hình" trạng thái bàn cờ sau mỗi hành động
    frames = []

    pos = cell
    stones = board[pos]["dan"]
    board[pos]["dan"] = 0
    # Khung hình 1: Nhấc quân lên (ô hiện tại về 0)
    frames.append((copy.deepcopy(board), list(scores)))

    # Quá trình rải sỏi đầu tiên
    while stones > 0:
        pos = (pos + direction) % N
        board[pos]["dan"] += 1
        stones -= 1
        frames.append((copy.deepcopy(board), list(scores)))

    # --- KIỂM TRA TRẠNG THÁI SAU KHI RẢI XONG ---
    while True:
        next_pos = (pos + direction) % N

        # TRƯỜNG HỢP 1: Ô tiếp theo CÓ QUÂN
        if board[next_pos]["dan"] > 0:
            if next_pos in QUAN_CELLS:
                # Chạm ô Quan -> Dừng lượt (Không được bốc Quan đi rải)
                break
            else:
                # Chạm ô dân -> Bốc lên rải tiếp
                stones = board[next_pos]["dan"]
                board[next_pos]["dan"] = 0
                frames.append((copy.deepcopy(board), list(scores)))
                pos = next_pos

                while stones > 0:
                    pos = (pos + direction) % N
                    board[pos]["dan"] += 1
                    stones -= 1
                    frames.append((copy.deepcopy(board), list(scores)))

        # TRƯỜNG HỢP 2: Ô tiếp theo LÀ Ô TRỐNG -> Chuyển sang pha ĂN QUÂN
        elif board[next_pos]["dan"] == 0 and board[next_pos]["quan"] == 0:

            # Vòng lặp xét "Ăn liên tiếp" (Ăn rền)
            while True:
                o_trong = (pos + direction) % N
                o_bi_an = (o_trong + direction) % N

                # Điều kiện ăn: 1 ô trống -> 1 ô có quân
                if board[o_trong]["dan"] == 0 and (board[o_bi_an]["dan"] > 0 or board[o_bi_an]["quan"] == 1):
                    print(f"Player {player} ăn ô {o_bi_an}: {board[o_bi_an]} quân")

                    # Ăn QUAN
                    if o_bi_an in QUAN_CELLS and board[o_bi_an]["quan"] == 1:
                        scores[player + 2] += 1
                        scores[player] += 10
                        board[o_bi_an]["quan"] = 0

                    # Ăn DÂN
                    scores[player] += board[o_bi_an]["dan"]
                    board[o_bi_an]["dan"] = 0

                    frames.append((copy.deepcopy(board), list(scores)))

                    # Cập nhật vị trí để vòng lặp xét tiếp xem có được ăn tiếp không
                    pos = o_bi_an
                else:
                    # Nếu đụng 2 ô trống liên tiếp, hoặc đụng ô tiếp theo không có quân -> Dừng ăn
                    break

            # Đã lọt vào pha Ăn Quân thì dù có ăn được hay không, sau đó cũng MẤT LƯỢT (Không rải tiếp)
            break

    return frames


def game_over(board):
    return (board[QUAN_L]["quan"] == 0 and board[QUAN_R]["quan"] == 0)
