
#=====================================
# from constants import *

import os
import random
import time
import pygame
import sys
import ai
from pause_menu import draw_pause_menu
from game_over import draw_game_over
PLAY_WITH_AI = False  # Đổi thành False nếu muốn chơi 2 người
AI_PLAYER = 1        # Tèo (P2) sẽ là máy
# ==========================================
# 1. PHẦN LOGIC GAME
# ==========================================

N = 12
QUAN_L = 0
QUAN_R = 6

P1_CELLS = [1, 2, 3, 4, 5]
P2_CELLS = [7, 8, 9, 10, 11]
QUAN_CELLS = [QUAN_L, QUAN_R]

P1_VISUAL = [1, 2, 3, 4, 5]
P2_VISUAL = [11, 10, 9, 8, 7]


icon_restart = pygame.image.load("assets/icon_restart.png")
icon_restart = pygame.transform.scale(icon_restart, (40, 40))

icon_exit = pygame.image.load("assets/icon_exit.png")
icon_exit = pygame.transform.scale(icon_exit, (40, 40))

icon_restart_rect = pygame.Rect(400, 450, 60, 60)
icon_exit_rect   = pygame.Rect(500, 450, 60, 60)
def init_board():
    board = [0] * N
    board[QUAN_L] = 10
    board[QUAN_R] = 10
    for i in P1_CELLS:
        board[i] = 5
    for i in P2_CELLS:
        board[i] = 5
    return board


def get_player_pits(player):
    return P1_CELLS if player == 0 else P2_CELLS


def valid_moves(board, player):
    return [i for i in get_player_pits(player) if board[i] > 0]


def refill_if_empty(board, scores, player):
    cells = get_player_pits(player)
    if all(board[i] == 0 for i in cells):
        if scores[player] >= 5:
            for i in cells:
                board[i] = 1
            scores[player] -= 5
            print(f"Player {player} rải lại 5 quân")
        else:
            print(f"Player {player} không đủ quân để rải lại!")
            return False
    return True


def move(board, scores, player, cell, direction):
    board = list(board)
    scores = list(scores)

    # Mảng chứa các "khung hình" trạng thái bàn cờ sau mỗi hành động
    frames = []

    pos = cell
    stones = board[pos]
    board[pos] = 0
    # Khung hình 1: Nhấc quân lên (ô hiện tại về 0)
    frames.append((list(board), list(scores)))

    # Quá trình rải sỏi đầu tiên
    while stones > 0:
        pos = (pos + direction) % N
        board[pos] += 1
        stones -= 1
        frames.append((list(board), list(scores)))

    # --- KIỂM TRA TRẠNG THÁI SAU KHI RẢI XONG ---
    while True:
        next_pos = (pos + direction) % N

        # TRƯỜNG HỢP 1: Ô tiếp theo CÓ QUÂN
        if board[next_pos] > 0:
            if next_pos in QUAN_CELLS:
                # Chạm ô Quan -> Dừng lượt (Không được bốc Quan đi rải)
                break
            else:
                # Chạm ô dân -> Bốc lên rải tiếp
                stones = board[next_pos]
                board[next_pos] = 0
                frames.append((list(board), list(scores)))
                pos = next_pos

                while stones > 0:
                    pos = (pos + direction) % N
                    board[pos] += 1
                    stones -= 1
                    frames.append((list(board), list(scores)))

        # TRƯỜNG HỢP 2: Ô tiếp theo LÀ Ô TRỐNG -> Chuyển sang pha ĂN QUÂN
        elif board[next_pos] == 0:

            # Vòng lặp xét "Ăn liên tiếp" (Ăn rền)
            while True:
                o_trong = (pos + direction) % N
                o_bi_an = (o_trong + direction) % N

                # Điều kiện ăn: 1 ô trống -> 1 ô có quân
                if board[o_trong] == 0 and board[o_bi_an] > 0:
                    print(f"Player {player} ăn ô {o_bi_an}: {board[o_bi_an]} quân")

                    # --- THÊM 2 DÒNG NÀY ĐỂ CHECK XEM CÓ PHẢI LÀ ĂN QUAN KHÔNG ---
                    if o_bi_an in QUAN_CELLS and board[o_bi_an] >= 10:
                        scores[player + 2] += 1  # Cộng 1 vào ô "Số Quan ăn được" của player đó
                    # -----------------------------------------------------------

                    scores[player] += board[o_bi_an]
                    board[o_bi_an] = 0
                    frames.append((list(board), list(scores)))

                    # Cập nhật vị trí để vòng lặp xét tiếp xem có được ăn tiếp không
                    pos = o_bi_an
                else:
                    # Nếu đụng 2 ô trống liên tiếp, hoặc đụng ô tiếp theo không có quân -> Dừng ăn
                    break

            # Đã lọt vào pha Ăn Quân thì dù có ăn được hay không, sau đó cũng MẤT LƯỢT (Không rải tiếp)
            break

    return frames


def game_over(board):
    return (board[QUAN_L] == 0 and board[QUAN_R] == 0)


# ==========================================
# 2. PHẦN GIAO DIỆN PYGAME
# ==========================================
WIDTH, HEIGHT = 960, 720
START_X, START_Y = 210, 240
CELL_WIDTH, CELL_HEIGHT = 105, 110
TAM_QUAN_TRAI = (160, 350)
TAM_QUAN_PHAI = (810, 350)
ARROW_LEFT = 'assets/arrow-left.png'
ARROW_RIGHT = 'assets/arrow-right.png'
ARROW_TARGET_HEIGHT = 40
ICON_PAUSE_FILE = 'assets/pause.png'
PAUSE_ICON_SIZE = 40
PAUSE_BACK_COLOR = (76, 143, 21)

AVATAR_P1 = pygame.Rect(402, 546, 172, 131)
AVATAR_P2 = pygame.Rect(404, 46, 163, 120)
GLOW_COLOR = (255, 255, 100)


SCORE_RECT_P2 = pygame.Rect(644, 98, 150, 86) # Khung điểm người chơi Trên
SCORE_RECT_P1 = pygame.Rect(160, 529, 147, 88) # Khung điểm người chơi Dưới


SCORE_COLOR = (50, 30, 10)
NUM_COLOR = (137, 110, 29)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ô Ăn Quan")
bg_image = pygame.image.load('assets/background.png')


font = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 40)
small_font = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 30)
font_so_dan = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 25)

def load_arrow(filename, target_height):
    if (os.path.exists(filename)):
        img = pygame.image.load(filename).convert_alpha()
        ratio = img.get_width() / img.get_height()
        target_width = int(target_height * ratio)
        return pygame.transform.scale(img, (target_width, target_height))
    else:
        # Nếu chưa có ảnh, vẽ tạm cục màu đỏ để test code không bị lỗi
        surf = pygame.Surface((target_height, target_height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 0, 0), (target_height//2, target_height//2), target_height//2)
        return surf

img_arrow_left = load_arrow(ARROW_LEFT, ARROW_TARGET_HEIGHT)
img_arrow_right = load_arrow(ARROW_RIGHT, ARROW_TARGET_HEIGHT)

# Dùng tạm hàm load_arrow để load icon pause luôn cho tiện
img_pause_icon = load_arrow(ICON_PAUSE_FILE, PAUSE_ICON_SIZE)
# Định vị trí icon ở góc trên cùng bên trái (cách lề 20 pixel)
PAUSE_ICON_POS = (4, 4)
PAUSE_BACK_RECT = pygame.Rect(PAUSE_ICON_POS[0] - 2, PAUSE_ICON_POS[1] - 2, PAUSE_ICON_SIZE + 4, PAUSE_ICON_SIZE + 4)

# Tạo khung Rect ẩn để bắt sự kiện click chuột
arrow_left_rect = img_arrow_left.get_rect()
arrow_right_rect = img_arrow_right.get_rect()

# --- LOAD ẢNH QUAN VÀ SỎI ---
# 1. Load ảnh Quan (Kích thước khoảng 60x60 pixel)
img_quan_trai = pygame.transform.scale(pygame.image.load('assets/quan1.png').convert_alpha(), (60, 60))
img_quan_phai = pygame.transform.scale(pygame.image.load('assets/quan2.png').convert_alpha(), (60, 60))


# 2. Load 6 ảnh Sỏi Dân (Kích thước khoảng 25x25 pixel)
img_soi_list = []
for i in range(1, 7): # Load từ soi_1.png đến soi_6.png
    if os.path.exists(f'assets/dan{i}.png'):
        img = pygame.transform.scale(pygame.image.load(f'assets/dan{i}.png').convert_alpha(), (25, 25))
        img_soi_list.append(img)
    else:
        # Chống lỗi nếu thiếu ảnh: Vẽ tạm hình tròn
        surf = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(surf, (150, 150, 150), (12, 12), 12)
        img_soi_list.append(surf)

VISUAL_STONES = []
for _ in range(150):
    img_idx = random.randint(0, 5) # Random chọn 1 trong 6 ảnh sỏi
    dx = random.randint(-25, 25)   # Lệch tọa độ X trong ô
    dy = random.randint(-25, 25)   # Lệch tọa độ Y trong ô
    VISUAL_STONES.append((img_idx, dx, dy))


toa_do = [None] * N

toa_do[0] = TAM_QUAN_TRAI
toa_do[1] = pygame.Rect(210, 355, 105, 125)
toa_do[2] = pygame.Rect(318, 356, 106, 122)
toa_do[3] = pygame.Rect(425, 355, 110, 120)
toa_do[4] = pygame.Rect(534, 355, 111, 121)
toa_do[5] = pygame.Rect(645, 355, 110, 123)

toa_do[6] = TAM_QUAN_PHAI

toa_do[7] = pygame.Rect(640, 238, 113, 111)
toa_do[8] = pygame.Rect(535, 239, 108, 112)
toa_do[9] = pygame.Rect(428, 239, 108, 113)
toa_do[10] = pygame.Rect(318, 238, 106, 113)
toa_do[11] = pygame.Rect(210, 240, 105, 110)


# Khởi tạo trạng thái game
board = init_board()

# [Điểm P1, Điểm P2, Số Quan P1 ăn, Số Quan P2 ăn]
scores = [0, 0, 0, 0]

current_player = 0
selected_cell = None  # Ô đang được click chờ rải



def format_time(t):
    minutes = int(t // 60)
    seconds = int(t % 60)
    return f"{minutes:02}:{seconds:02}"

def draw_timer_box(screen, x, y, text_surface):
    padding = 10
    rect = text_surface.get_rect(topleft=(x, y))

    box = pygame.Rect(
        rect.x - padding,
        rect.y - padding,
        rect.width + padding*2,
        rect.height + padding*2
    )

    pygame.draw.rect(screen, (255, 240, 200), box, border_radius=10)
    pygame.draw.rect(screen, (160, 110, 40), box, 2, border_radius=10)

    screen.blit(text_surface, rect)

def main(screen):
    # Các biến phục vụ Animation (Nhảy số từ từ)
    global board, scores, current_player, selected_cell
    selected_cell = None
    paused = False
    time_out = None
    btn_continue = pygame.Rect(380, 250, 200, 60)
    btn_restart = pygame.Rect(380, 330, 200, 60)
    btn_quit = pygame.Rect(380, 410, 200, 60)
    is_animating = False       # Đang trong quá trình rải sỏi hay không?
    anim_frames = []           # Chứa danh sách các trạng thái bàn cờ
    anim_timer = 0             # Bộ đếm thời gian
    ANIM_SPEED = 800           # Độ trễ giữa mỗi lần nhảy số (Tính bằng mili-giây, 300ms = 0.3s)
    time_p1 = 45
    time_p2 = 45

    last_time = time.time()

    while True:
        current_time = time.time()
        delta = current_time - last_time
        last_time = current_time

        if not paused and not is_animating and not game_over(board):
            if current_player == 0:
                time_p1 -= delta
            else:
                time_p2 -= delta
        # không cho âm
        time_p1 = max(0, time_p1)
        time_p2 = max(0, time_p2)
        # ===== HẾT GIỜ → AI ĐÁNH THAY =====
        if not is_animating and not paused and not game_over(board):

            if current_player == 0 and time_p1 <= 0:
                moves = valid_moves(board, 0)
                if moves:
                    cell = random.choice(moves)
                    direction = random.choice([-1, 1])

                    anim_frames = move(board, scores, 0, cell, direction)
                    is_animating = True
                    anim_timer = pygame.time.get_ticks()

                    time_p1 = 45  # reset time

            elif current_player == 1 and time_p2 <= 0:
                moves = valid_moves(board, 1)
                if moves:
                    cell = random.choice(moves)
                    direction = random.choice([-1, 1])

                    anim_frames = move(board, scores, 1, cell, direction)
                    is_animating = True
                    anim_timer = pygame.time.get_ticks()

                    time_p2 = 45  # reset time
        # ===== AI TỰ CHƠI KHI HẾT GIỜ =====
        if not is_animating and not paused and not game_over(board):
            if PLAY_WITH_AI:
                if (current_player == AI_PLAYER):
                    moves = valid_moves(board, current_player)
                    if moves:
                        cell = random.choice(moves)
                        direction = random.choice([-1, 1])

                        anim_frames = move(board, scores, current_player, cell, direction)
                        is_animating = True
                        anim_timer = pygame.time.get_ticks()
        # --- BƯỚC 1: CẬP NHẬT ANIMATION (NHẢY SỐ) ---
        if is_animating:
            now = pygame.time.get_ticks()  # Lấy thời gian hiện tại của game

            # Nếu đã qua đủ thời gian trễ (300ms)
            if now - anim_timer > ANIM_SPEED:
                if len(anim_frames) > 0:
                    # Lấy khung hình tiếp theo ra để hiển thị
                    board, scores = anim_frames.pop(0)
                    anim_timer = now  # Reset đồng hồ
                else:
                    # Nếu đã chiếu hết các khung hình -> Kết thúc Animation
                    is_animating = False
                    current_player = 1 - current_player  # Đổi lượt!
                    # reset thời gian lượt mới
                    if current_player == 0:
                        time_p1 = 45
                    else:
                        time_p2 = 45

        # --- BƯỚC 2: XỬ LÝ SỰ KIỆN CHUNG (Luôn chạy để tránh treo máy) ---
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if paused:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if btn_continue.collidepoint(event.pos):
                        paused = False
                        selected_cell = None
                        is_animating = False
                        anim_frames = []
                    elif btn_restart.collidepoint(event.pos):
                        board = init_board()
                        scores = [0, 0, 0, 0]
                        current_player = 0

                        selected_cell = None
                        is_animating = False
                        anim_frames = []

                        paused = False
                        time_p1 = 45
                        time_p2 = 45
                        last_time = time.time()
                    elif btn_quit.collidepoint(event.pos):
                        return

                continue

            # 👉 CLICK NÚT PAUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over(board):
                    if icon_restart_rect.collidepoint(event.pos):
                        board = init_board()
                        scores = [0, 0, 0, 0]
                        current_player = 0
                        selected_cell = None
                        is_animating = False

                        time_p1 = 45
                        time_p2 = 45
                        last_time = time.time()

                    elif icon_exit_rect.collidepoint(event.pos):
                        return
                if PAUSE_BACK_RECT.collidepoint(event.pos):
                    paused = True
        # 👉 CLICK GAME
            if not game_over(board) and not is_animating and not paused:
                if not (PLAY_WITH_AI and current_player == AI_PLAYER):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos

                        # ===== 1. ƯU TIÊN CHECK MŨI TÊN TRƯỚC =====
                        if selected_cell is not None:

                            cell_rect = toa_do[selected_cell]
                            offset = -5

                            arrow_left_rect.centery = cell_rect.centery
                            arrow_right_rect.centery = cell_rect.centery

                            arrow_left_rect.right = cell_rect.left - offset
                            arrow_right_rect.left = cell_rect.right + offset

                            if arrow_left_rect.collidepoint(mouse_pos):
                                direction = -1 if current_player == 0 else 1

                            elif arrow_right_rect.collidepoint(mouse_pos):
                                direction = 1 if current_player == 0 else -1

                            else:
                                direction = 0

                            if direction != 0:
                                anim_frames = move(board, scores, current_player, selected_cell, direction)
                                is_animating = True
                                anim_timer = pygame.time.get_ticks()
                                selected_cell = None
                                continue  # 🔥 QUAN TRỌNG

                        # ===== 2. SAU ĐÓ MỚI CHỌN Ô =====
                        valid_pits = valid_moves(board, current_player)

                        for i in valid_pits:
                            if toa_do[i].collidepoint(mouse_pos):
                                selected_cell = i
                                break
        # # --- BƯỚC 2: CẬP NHẬT LOGIC (Check hết quân) ---
        # if not game_over(board):
        #     refill_if_empty(board, scores, current_player)

        # --- BƯỚC 3: CẬP NHẬT LOGIC KHÁC ---
        if not game_over(board) and not is_animating and not paused:
            # Chỉ nạp lại quân (refill) khi đã rải xong hết
            refill_if_empty(board, scores, current_player)

        elif game_over(board) and not is_animating:
            # LUẬT KẾT THÚC: Thu quân (Vơ vét toàn bộ sỏi dân mang về làm điểm)
            co_thu_quan = False

            # Quét sỏi của Người chơi 1 (Dưới)
            for i in P1_CELLS:
                if board[i] > 0:
                    scores[0] += board[i]
                    board[i] = 0
                    anim_frames.append((list(board), list(scores)))
                    co_thu_quan = True

            # Quét sỏi của Người chơi 2 (Trên)
            for i in P2_CELLS:
                if board[i] > 0:
                    scores[1] += board[i]
                    board[i] = 0
                    anim_frames.append((list(board), list(scores)))
                    co_thu_quan = True

            if co_thu_quan:
                print("Hết quan, tàn dân, thu quân, bán ruộng!")
                is_animating = True
                anim_timer = pygame.time.get_ticks()

            # Quét sỏi của Người chơi 1 (Dưới)
            for i in P1_CELLS:
                if board[i] > 0:
                    scores[0] += board[i]
                    board[i] = 0
                    co_thu_quan = True

            # Quét sỏi của Người chơi 2 (Trên)
            for i in P2_CELLS:
                if board[i] > 0:
                    scores[1] += board[i]
                    board[i] = 0
                    co_thu_quan = True

            if co_thu_quan:
                print("Hết quan, tàn dân, thu quân, bán ruộng!")

        # --- BƯỚC 4: VẼ LÊN MÀN HÌNH (RENDER) ---
        screen.blit(bg_image, (0, 0))

        # --- HIỆU ỨNG SÁNG VÀ THÔNG BÁO LƯỢT CHƠI ---
        if not game_over(board):
            # Màu sắc cho chữ
            TEXT_COLOR = (255, 255, 255)  # Màu trắng cho nổi bật
            WAIT_COLOR = (93, 97, 87)  # Màu xám cho trạng thái đợi

            if current_player == 0:
                # 1. Hiệu ứng sáng cho Tí (P1)
                pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P1.inflate(15, 15), width=3, border_radius=15)
                pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P1, width=6, border_radius=10)

                # 2. Chữ thông báo cho Tí (Dưới Avatar P1)
                txt_p1 = small_font.render("Luot cua Ti", True, GLOW_COLOR)
                txt_p2 = small_font.render("Doi Teo...", True, WAIT_COLOR)
            else:
                # 1. Hiệu ứng sáng cho Tèo (P2)
                pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P2.inflate(15, 15), width=3, border_radius=15)
                pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P2, width=6, border_radius=10)

                # 2. Chữ thông báo cho Tèo (Trên Avatar P2)
                txt_p1 = small_font.render("Doi Ti...", True, WAIT_COLOR)
                txt_p2 = small_font.render("Luot cua Teo", True, GLOW_COLOR)

            # --- VẼ CHỮ LÊN MÀN HÌNH ---
            # Chữ của Tí: Đặt dưới Avatar P1 (Y + chiều cao + 5px)
            rect_p1 = txt_p1.get_rect(midtop=(AVATAR_P1.centerx, AVATAR_P1.bottom + 10))
            screen.blit(txt_p1, rect_p1)

            # Chữ của Tèo: Đặt trên Avatar P2 (Y - chiều cao chữ - 5px)
            rect_p2 = txt_p2.get_rect(midbottom=(AVATAR_P2.centerx, AVATAR_P2.top - 10))
            screen.blit(txt_p2, rect_p2)

        # ==================================================
        # VẼ SỎI TÍCH LŨY VÀ ĐIỂM CỦA 2 PLAYER (Luôn vẽ)
        # ==================================================
        # ===== ĐỒNG HỒ =====

        # ===== HIỆU ỨNG NHẤP NHÁY =====
        # ===== MÀU MỚI ĐẸP HƠN =====
        NORMAL_COLOR = (60, 40, 20)  # nâu đậm
        ACTIVE_COLOR = (0, 200, 150)  # vàng nổi
        WARNING_COLOR = (255, 255, 255)  # trắng nhấp nháy

        blink = int(time.time() * 2) % 2

        # PLAYER 1
        if time_p1 < 10:
            color_p1 = WARNING_COLOR if blink else ACTIVE_COLOR
            warning_p1 = "SAP HET GIO!"
        else:
            color_p1 = ACTIVE_COLOR if current_player == 0 else NORMAL_COLOR
            warning_p1 = ""

        # PLAYER 2
        if time_p2 < 10:
            color_p2 = WARNING_COLOR if blink else ACTIVE_COLOR
            warning_p2 = "SAP HET GIO!"
        else:
            color_p2 = ACTIVE_COLOR if current_player == 1 else NORMAL_COLOR
            warning_p2 = ""

        # ===== PLAYER 1 (DƯỚI) =====
        txt_time_p1 = small_font.render(f"{format_time(time_p1)}", True, color_p1)
        draw_timer_box(screen, 50, HEIGHT - 80, txt_time_p1)

        if warning_p1:
            warn1 = small_font.render(warning_p1, True, (255, 0, 0))
            screen.blit(warn1, (50, HEIGHT - 140))

        # ===== PLAYER 2 (TRÊN) =====
        txt_time_p2 = small_font.render(f"{format_time(time_p2)}", True, color_p2)
        draw_timer_box(screen, 50, 40, txt_time_p2)

        if warning_p2:
            warn2 = small_font.render(warning_p2, True, (255, 0, 0))
            screen.blit(warn2, (50, 70))
        # PLAYER 1 (DƯỚI)
        tam_x1, tam_y1 = SCORE_RECT_P1.centerx, SCORE_RECT_P1.centery
        so_quan_p1 = scores[2]
        so_dan_p1 = scores[0] - (so_quan_p1 * 10)

        while so_dan_p1 < 0 and so_quan_p1 > 0:
            so_quan_p1 -= 1
            so_dan_p1 += 10

        for q in range(so_quan_p1):
            quan_img = img_quan_trai if q == 0 else img_quan_phai
            quan_rect = quan_img.get_rect(center=(tam_x1 - 25 + q * 50, tam_y1))
            screen.blit(quan_img, quan_rect)

        for j in range(so_dan_p1):
            idx = (100 + j) % len(VISUAL_STONES)
            img_idx, dx, dy = VISUAL_STONES[idx]
            soi_img = img_soi_list[img_idx]
            soi_rect = soi_img.get_rect(center=(tam_x1 + int(dx * 1.8), tam_y1 + int(dy * 1.2)))
            screen.blit(soi_img, soi_rect)

        diem_p1_surface = font.render(f"{scores[0]}", True, NUM_COLOR)
        toa_do_p1 = (SCORE_RECT_P1.right - 10, SCORE_RECT_P1.top + 10)
        diem_p1_rect = diem_p1_surface.get_rect(topright=toa_do_p1)
        screen.blit(diem_p1_surface, diem_p1_rect)

        # PLAYER 2 (TRÊN)
        tam_x2, tam_y2 = SCORE_RECT_P2.centerx, SCORE_RECT_P2.centery
        so_quan_p2 = scores[3]
        so_dan_p2 = scores[1] - (so_quan_p2 * 10)

        while so_dan_p2 < 0 and so_quan_p2 > 0:
            so_quan_p2 -= 1
            so_dan_p2 += 10

        for q in range(so_quan_p2):
            quan_img = img_quan_trai if q == 0 else img_quan_phai
            quan_rect = quan_img.get_rect(center=(tam_x2 - 25 + q * 50, tam_y2))
            screen.blit(quan_img, quan_rect)

        for j in range(so_dan_p2):
            idx = (200 + j) % len(VISUAL_STONES)
            img_idx, dx, dy = VISUAL_STONES[idx]
            soi_img = img_soi_list[img_idx]
            soi_rect = soi_img.get_rect(center=(tam_x2 + int(dx * 1.8), tam_y2 + int(dy * 1.2)))
            screen.blit(soi_img, soi_rect)

        # Vẽ Text điểm (Góc dưới bên trái)
        diem_p2_surface = font.render(f"{scores[1]}", True, NUM_COLOR)
        toa_do_p2 = (SCORE_RECT_P2.left + 5, SCORE_RECT_P2.bottom - -6)
        diem_p2_rect = diem_p2_surface.get_rect(bottomleft=toa_do_p2)
        screen.blit(diem_p2_surface, diem_p2_rect)

        # ==================================================
        # CHỮ GAME OVER HOẶC HƯỚNG DẪN
        # ==================================================

        if game_over(board) and not is_animating:
            draw_game_over(screen, board, scores, font,
                           icon_restart, icon_exit,
                           icon_restart_rect, icon_exit_rect)
        else:
            if selected_cell is not None:
                huong_dan = small_font.render(f"Ban da chon o {selected_cell}. Chon huong rai!", True, (255, 255, 0))
                screen.blit(huong_dan, (WIDTH // 2 - 150, HEIGHT - 50))


            # Vẽ sỏi và bàn cờ
            for i in range(N):
                so_luong = board[i]

                if i in QUAN_CELLS:
                    # --- VẼ QUAN VÀ SỎI DÂN RƠI VÀO Ô QUAN ---
                    pos = toa_do[i]  # pos đang là (x, y) tâm ô

                    # Xác định xem Quan to còn không và có bao nhiêu sỏi nhỏ
                    co_quan = True if so_luong >= 10 else False
                    so_dan_trong_quan = so_luong - 10 if co_quan else so_luong

                    # 1. Vẽ ảnh Quan to (nếu vẫn chưa bị ăn)
                    if co_quan:
                        quan_img = img_quan_trai if i == QUAN_L else img_quan_phai
                        quan_rect = quan_img.get_rect(center=pos)
                        screen.blit(quan_img, quan_rect)

                    # 2. Vẽ các ảnh sỏi nhỏ (dân) rớt xung quanh viên Quan
                    for j in range(so_dan_trong_quan):
                        # Vẫn dùng mảng random để sỏi rơi lộn xộn tự nhiên
                        idx = (i * 20 + j) % len(VISUAL_STONES)
                        img_idx, dx, dy = VISUAL_STONES[idx]
                        soi_img = img_soi_list[img_idx]

                        soi_rect = soi_img.get_rect(center=(pos[0] + dx, pos[1] + dy))
                        screen.blit(soi_img, soi_rect)

                    # 3. Vẽ chữ số đè lên quan (chỉ vẽ khi ô có quân)
                    if so_luong > 0:
                        text = small_font.render(str(so_luong), True, NUM_COLOR)

                        if i == QUAN_L:
                            # Ô Quan 0 (Bên Trái): Đẩy chữ số xuống góc dưới (Cộng thêm Y)
                            # pos[0] là tọa độ X (giữ nguyên ở giữa), pos[1] + 50 là đẩy Y xuống dưới 50 pixel
                            text_rect = text.get_rect(center=(pos[0] + 30, pos[1] + 110))
                        else:
                            # Ô Quan 2 (Bên Phải - QUAN_R): Đẩy chữ số lên góc trên (Trừ đi Y)
                            # pos[1] - 50 là đẩy Y lên trên 50 pixel
                            text_rect = text.get_rect(center=(pos[0] - 36, pos[1] - 90))

                        screen.blit(text, text_rect)

                else:
                    # --- VẼ DÂN ---
                    rect = toa_do[i]  # toa_do ô dân đang là pygame.Rect

                    # Viền vàng khi được chọn
                    if i == selected_cell:
                        pygame.draw.rect(screen, (244, 237, 159), rect, 5)

                    # Vẽ ảnh từng viên sỏi dân rơi lộn xộn
                    tam_x, tam_y = rect.centerx, rect.centery
                    for j in range(so_luong):
                        # Dùng (i*15 + j) để đảm bảo mỗi ô có 1 kiểu rơi lộn xộn khác nhau
                        idx = (i * 15 + j) % len(VISUAL_STONES)
                        img_idx, dx, dy = VISUAL_STONES[idx]

                        # Lấy ảnh sỏi ra và in lên
                        soi_img = img_soi_list[img_idx]
                        soi_rect = soi_img.get_rect(center=(tam_x + dx, tam_y + dy))
                        screen.blit(soi_img, soi_rect)

                    # Tạo chữ số hiển thị ở góc
                    text = font_so_dan.render(str(so_luong), True, NUM_COLOR)

                    if i in P1_CELLS:
                        # Người chơi 1 (Hàng dưới): Ép xuống góc dưới bên phải, cách mép 8 pixel
                        text_rect = text.get_rect(bottomright=(rect.right - 5, rect.bottom - -6))
                    else:
                        # Người chơi 2 (Hàng trên): Giữ nguyên ở góc trên bên trái, cách mép 8 pixel
                        text_rect = text.get_rect(topleft=(rect.left + 5, rect.top + -6))

                    screen.blit(text, text_rect)

        # Vẽ mũi tên nếu đang có ô được chọn
        if selected_cell is not None and not game_over(board) and not is_animating:
            cell_rect = toa_do[selected_cell]
            offset = -5  # Khoảng cách từ mép ô đến mũi tên
            arrow_left_rect.centery = cell_rect.centery
            arrow_right_rect.centery = cell_rect.centery
            arrow_left_rect.right = cell_rect.left - offset
            arrow_right_rect.left = cell_rect.right + offset

            screen.blit(img_arrow_left, arrow_left_rect)
            screen.blit(img_arrow_right, arrow_right_rect)
        if not game_over(board):
            pygame.draw.rect(screen, PAUSE_BACK_COLOR, PAUSE_BACK_RECT, border_radius=8)
            screen.blit(img_pause_icon, PAUSE_ICON_POS)

        if paused:
            draw_pause_menu(screen, btn_continue, btn_restart, btn_quit,font)
        # --- BƯỚC 4: CẬP NHẬT FRAME ---
        pygame.display.flip()

def run_game(screen, play_with_ai=True):
    global PLAY_WITH_AI, board, scores, current_player

    PLAY_WITH_AI = play_with_ai

    board = init_board()
    scores = [0,0,0,0]
    current_player = 0

    main(screen)