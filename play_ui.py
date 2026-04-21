import copy
import time

# import constants
#=====================================
from constants import *
from game import *

import os
import random
from ui import *

import pygame
import sys
import ai

icon_restart_rect = pygame.Rect(400, 450, 60, 60)
icon_exit_rect   = pygame.Rect(500, 450, 60, 60)

icon_restart = pygame.image.load("assets/icon_restart.png")
icon_restart = pygame.transform.scale(icon_restart, (40, 40))


# ==========================================
# 2. PHẦN GIAO DIỆN PYGAME
# ==========================================

AVATAR_P1 = pygame.Rect(RECT_AVARTAR_P1)
AVATAR_P2 = pygame.Rect(RECT_AVARTAR_P2)
SCORE_RECT_P2 = pygame.Rect(RECT_SCORE_P2)
SCORE_RECT_P1 = pygame.Rect(RECT_SCORE_P1)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)
bg_image = pygame.image.load(BACKGROUND)


font = pygame.font.Font(FONT, 40)
small_font = pygame.font.Font(FONT, 30)
font_so_dan = pygame.font.Font(FONT, 25)
time_font = pygame.font.Font(FONT, 20)

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




#===TIME===
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


def play():
    # Khởi tạo trạng thái game
    board = init_board()

    # [Điểm P1, Điểm P2, Số Quan P1 ăn, Số Quan P2 ăn]
    scores = [0, 0, 0, 0]

    current_player = 0
    selected_cell = None  # Ô đang được click chờ rải

    # Các biến phục vụ Animation (Nhảy số từ từ)
    is_animating = False       # Đang trong quá trình rải sỏi hay không?
    anim_frames = []           # Chứa danh sách các trạng thái bàn cờ
    anim_timer = 0             # Bộ đếm thời gian
    last_time = time.time()
    paused = False
    time_p1 = TIME
    time_p2 = TIME
    btn_continue = pygame.Rect(380, 250, 200, 60)
    btn_restart = pygame.Rect(380, 330, 200, 60)
    btn_quit = pygame.Rect(380, 410, 200, 60)
    display_time_p1 = TIME
    display_time_p2 = TIME

    while True:
        current_time = time.time()
        delta = current_time - last_time
        last_time = current_time

        if not paused and not is_animating and not game_over(board):
            if current_player == 0:
                time_p1 -= delta
            else:
                time_p2 -= delta

        time_p1 = max(0, time_p1)
        time_p2 = max(0, time_p2)

        display_time_p1 = time_p1
        display_time_p2 = time_p2

        # --- BƯỚC 1: CẬP NHẬT ANIMATION (NHẢY SỐ) ---
        if is_animating and not paused:
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
                        time_p1 = TIME
                    else:
                        time_p2 = TIME

        # --- BƯỚC 2: XỬ LÝ SỰ KIỆN CHUNG (Luôn chạy để tránh treo máy) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if paused:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if btn_continue.collidepoint(event.pos):
                        paused = False
                        last_time = time.time()
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
                        time_p1 = TIME
                        time_p2 = TIME
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

                        time_p1 = TIME
                        time_p2 = TIME
                        last_time = time.time()

                    elif icon_exit_rect.collidepoint(event.pos):
                        return
                if PAUSE_BACK_RECT.collidepoint(event.pos):
                    paused = True
                    continue

            # 1. UI global (pause, menu, button)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = event.pos
            #
            #     # click nút pause (ưu tiên xử lý trước)
            #     if PAUSE_BACK_RECT.collidepoint(mouse_pos):
            #         paused = True
            #         continue  # tránh click lan xuống các xử lý khác

            # 2. gameplay input
            # Chế độ Người chơi (Chỉ nhận lệnh khi không phải lượt AI và không đang animating)
            if not game_over(board) and not is_animating and not paused:
                if not (PLAY_WITH_AI and current_player == AI_PLAYER):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos
                        if selected_cell is None:
                            valid_pits = valid_moves(board, current_player)
                            for i in valid_pits:
                                if toa_do[i].collidepoint(mouse_pos):
                                    selected_cell = i
                        else:
                            direction = 0
                            if arrow_left_rect.collidepoint(mouse_pos):
                                direction = -1 if current_player == 0 else 1
                            elif arrow_right_rect.collidepoint(mouse_pos):
                                direction = 1 if current_player == 0 else -1
                            else:
                                selected_cell = None
                                valid_pits = valid_moves(board, current_player)
                                for i in valid_pits:
                                    if toa_do[i].collidepoint(mouse_pos):
                                        selected_cell = i

                            if direction != 0:
                                anim_frames = move(board, scores, current_player, selected_cell, direction)
                                is_animating = True
                                anim_timer = pygame.time.get_ticks()
                                selected_cell = None

                    elif event.type == pygame.KEYDOWN and selected_cell is not None:
                        direction = 0
                        if event.key == pygame.K_RIGHT:
                            direction = 1 if current_player == 0 else -1
                        elif event.key == pygame.K_LEFT:
                            direction = -1 if current_player == 0 else 1
                        if direction != 0:
                            anim_frames = move(board, scores, current_player, selected_cell, direction)
                            is_animating = True
                            anim_timer = pygame.time.get_ticks()
                            selected_cell = None

        # --- XỬ LÝ LƯỢT CỦA AI (Nằm ngoài vòng lặp event) ---
        if not game_over(board) and not is_animating and not paused:
            if PLAY_WITH_AI and current_player == AI_PLAYER:
                pygame.time.delay(200)  # Đợi 0.5s cho thật
                best_pit, best_dir = ai.get_best_move(board, scores, AI_PLAYER, move)
                if best_pit is not None:
                    anim_frames = move(board, scores, AI_PLAYER, best_pit, best_dir)
                    is_animating = True
                    anim_timer = pygame.time.get_ticks()
                    print(f"AI đã đi ô {best_pit} hướng {best_dir}")

        # --- HẾT GIỜ ---
        if not is_animating and not paused and not game_over(board):
            if current_player == 0 and time_p1 <= 0:
                best_pit, best_dir = ai.get_best_move(board, scores, 0, move)
                if best_pit is not None:
                    anim_frames = move(board, scores, 0, best_pit, best_dir)
                    is_animating = True
                    anim_timer = pygame.time.get_ticks()
                    # time_p1 = TIME
                    time_p1 = 0
                    display_time_p1 = 0

            elif current_player == 1 and time_p2 <= 0:
                best_pit, best_dir = ai.get_best_move(board, scores, 1, move)
                if best_pit is not None:
                    anim_frames = move(board, scores, 1, best_pit, best_dir)
                    is_animating = True
                    anim_timer = pygame.time.get_ticks()
                    # time_p2 = TIME
                    time_p2 = 0
                    display_time_p2 = 0

        if not game_over(board) and not is_animating:
            # Chỉ nạp lại quân (refill) khi đã rải xong hết
            refill_if_empty(board, scores, current_player)

        elif game_over(board) and not is_animating:
            # LUẬT KẾT THÚC: Thu quân (Vơ vét toàn bộ sỏi dân mang về làm điểm)
            co_thu_quan = False

            # Quét sỏi của Người chơi 1 (Dưới)
            for i in P1_CELLS:
                if board[i]["dan"] > 0:
                    scores[0] += board[i]["dan"]
                    board[i]["dan"] = 0
                    co_thu_quan = True

            # Quét sỏi của Người chơi 2 (Trên)
            for i in P2_CELLS:
                if board[i]["dan"] > 0:
                    scores[1] += board[i]["dan"]
                    board[i]["dan"] = 0
                    co_thu_quan = True

            if co_thu_quan:
                print("Hết quan, tàn dân, thu quân, bán ruộng!")

        # --- BƯỚC 4: VẼ LÊN MÀN HÌNH (RENDER) ---
        screen.blit(bg_image, (0, 0))

        # --- HIỆU ỨNG SÁNG VÀ THÔNG BÁO LƯỢT CHƠI ---
        if not game_over(board):
            if current_player == 0:
                # 1. Hiệu ứng sáng cho Tí (P1)
                pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P1.inflate(15, 15), width=3, border_radius=15)
                pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P1, width=6, border_radius=10)

                # 2. Chữ thông báo cho Tí (Dưới Avatar P1)
                txt_p1 = small_font.render("Luot cua Ti", True, GLOW_COLOR)
                txt_p2 = small_font.render("Doi Teo...", True, WAIT_COLOR)
            else:
                # 1. Hiệu ứng sáng cho Tèo (P2)
                # pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P2.inflate(15, 15), width=3, border_radius=15)
                # pygame.draw.rect(screen, GLOW_COLOR, AVATAR_P2, width=6, border_radius=10)
                pygame.draw.rect(screen, WARNING_COLOR, AVATAR_P2.inflate(15, 15), width=3, border_radius=15)
                pygame.draw.rect(screen, WARNING_COLOR, AVATAR_P2, width=6, border_radius=10)

                # 2. Chữ thông báo cho Tèo (Trên Avatar P2)
                txt_p1 = small_font.render("Doi Ti...", True, WAIT_COLOR)
                # txt_p2 = small_font.render("Luot cua Teo", True, GLOW_COLOR)
                txt_p2 = small_font.render("Luot cua Teo", True, WARNING_COLOR)

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
        # if game_over(board):
        #     # Làm tối mờ nền một chút cho màn hình kết thúc đẹp hơn
        #     overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        #     overlay.fill((0, 0, 0, 150))
        #     screen.blit(overlay, (0, 0))
        #
        #     # Tính toán phân định thắng thua
        #     if scores[0] > scores[1]:
        #         kq_text = "TI THANG!"
        #         color = (0, 255, 0)  # Xanh lá
        #     elif scores[1] > scores[0]:
        #         kq_text = "TEO THANG!"
        #         color = (0, 255, 0)
        #     else:
        #         kq_text = "HOA NHAU!"
        #         color = (255, 255, 0)  # Vàng
        #
        #     text_go = font.render("GAME OVER", True, (255, 50, 50))
        #     text_kq = font.render(kq_text, True, color)
        #
        #     screen.blit(text_go, text_go.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        #     screen.blit(text_kq, text_kq.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
        # else:
        #     if selected_cell is not None:
        #         huong_dan = small_font.render(f"Ban da chon o {selected_cell}. Chon huong rai!", True, (255, 255, 0))
        #         screen.blit(huong_dan, (WIDTH // 2 - 150, HEIGHT - 50))
        if game_over(board) and not is_animating:
            # draw_game_over(screen, board, scores, font,
            #                icon_restart, icon_exit,
            #                icon_restart_rect, icon_exit_rect)
            draw_game_over(screen, scores, font,
                           icon_restart, icon_exit,
                           icon_restart_rect, icon_exit_rect)
            # draw_game_over(screen, scores, font,
            #                icon_restart_rect, icon_exit_rect)
        else:
            if selected_cell is not None:
                huong_dan = small_font.render(f"Ban da chon o {selected_cell}. Chon huong rai!", True, (255, 255, 0))
                screen.blit(huong_dan, (WIDTH // 2 - 150, HEIGHT - 50))


            # Vẽ sỏi và bàn cờ
            for i in range(N):
                # so_luong = board[i]
                so_dan = board[i]["dan"]
                co_quan = board[i]["quan"] == 1

                if i in QUAN_CELLS:
                    # --- VẼ QUAN VÀ SỎI DÂN RƠI VÀO Ô QUAN ---
                    pos = toa_do[i]  # pos đang là (x, y) tâm ô
                    so_luong = board[i]["dan"] + (10 if board[i]["quan"] == 1 else 0)
                    co_quan = board[i]["quan"] == 1
                    so_dan_trong_quan = so_luong - 10 if co_quan else so_luong

                    # --- GIỮ NGUYÊN CODE CŨ ---
                    # 1. Vẽ ảnh Quan to (nếu vẫn chưa bị ăn)
                    if co_quan:
                        quan_img = img_quan_trai if i == QUAN_L else img_quan_phai
                        quan_rect = quan_img.get_rect(center=pos)
                        screen.blit(quan_img, quan_rect)

                    # 2. Vẽ các ảnh sỏi nhỏ (dân) rớt xung quanh viên Quan
                    for j in range(so_dan_trong_quan):
                        idx = (i * 20 + j) % len(VISUAL_STONES)
                        img_idx, dx, dy = VISUAL_STONES[idx]
                        soi_img = img_soi_list[img_idx]

                        soi_rect = soi_img.get_rect(center=(pos[0] + dx, pos[1] + dy))
                        screen.blit(soi_img, soi_rect)

                    # 3. Vẽ chữ số
                    if so_luong > 0:
                        text = small_font.render(str(so_luong), True, NUM_COLOR)

                        if i == QUAN_L:
                            text_rect = text.get_rect(center=(pos[0] + 30, pos[1] + 110))
                        else:
                            text_rect = text.get_rect(center=(pos[0] - 36, pos[1] - 90))

                        screen.blit(text, text_rect)

                else:
                    # --- VẼ DÂN ---
                    rect = toa_do[i]

                    # Viền vàng khi được chọn
                    if i == selected_cell:
                        pygame.draw.rect(screen, (244, 237, 159), rect, 5)

                    # Vẽ ảnh từng viên sỏi dân rơi lộn xộn
                    tam_x, tam_y = rect.centerx, rect.centery
                    # for j in range(so_luong):
                    for j in range(so_dan):
                        # đảm bảo mỗi ô có 1 kiểu rơi lộn xộn khác nhau
                        idx = (i * 15 + j) % len(VISUAL_STONES)
                        img_idx, dx, dy = VISUAL_STONES[idx]

                        # Lấy ảnh sỏi ra và in lên
                        soi_img = img_soi_list[img_idx]
                        soi_rect = soi_img.get_rect(center=(tam_x + dx, tam_y + dy))
                        screen.blit(soi_img, soi_rect)

                    # Tạo chữ số hiển thị ở góc
                    text = font_so_dan.render(str(so_dan), True, NUM_COLOR)

                    if i in P1_CELLS:
                        text_rect = text.get_rect(bottomright=(rect.right - 5, rect.bottom - -6))
                    else:
                        text_rect = text.get_rect(topleft=(rect.left + 5, rect.top + -6))

                    screen.blit(text, text_rect)

        # Vẽ mũi tên nếu đang có ô được chọn
        if selected_cell is not None and not game_over(board) and not paused:
            cell_rect = toa_do[selected_cell]
            offset = -5  # Khoảng cách từ mép ô đến mũi tên
            arrow_left_rect.centery = cell_rect.centery
            arrow_right_rect.centery = cell_rect.centery
            arrow_left_rect.right = cell_rect.left - offset
            arrow_right_rect.left = cell_rect.right + offset

            screen.blit(img_arrow_left, arrow_left_rect)
            screen.blit(img_arrow_right, arrow_right_rect)
        pygame.draw.rect(screen, PAUSE_BACK_COLOR, PAUSE_BACK_RECT, border_radius=2)
        screen.blit(img_pause_icon, PAUSE_ICON_POS)

        # ===== ĐỒNG HỒ =====

        # ===== HIỆU ỨNG NHẤP NHÁY =====
        # ===== MÀU MỚI ĐẸP HƠN =====
        # NORMAL_COLOR = (60, 40, 20)  # nâu đậm
        # ACTIVE_COLOR = (0, 200, 150)  # vàng nổi
        # WARNING_COLOR = (255, 255, 255)  # trắng nhấp nháy
        NORMAL_COLOR = (200, 200, 200)  # xám nhạt

        ACTIVE_COLOR = (255, 215, 0)  # vàng nổi bật
        WARNING_COLOR = (255, 50, 50)  # đỏ gấp gáp
        TIME_COLOR_P1 = (255, 100, 100)  # đỏ cho P1
        TIME_COLOR_P2 = (100, 255, 100)  # xanh cho

        blink = int(time.time() * 2) % 2

        # PLAYER 1
        # if time_p1 < 10:
        #     color_p1 = WARNING_COLOR if blink else ACTIVE_COLOR
        #     warning_p1 = "SAP HET GIO!"
        # else:
        #     color_p1 = ACTIVE_COLOR if current_player == 0 else NORMAL_COLOR
        #     # color_p1 = ACTIVE_COLOR if current_player == 0 else TIME_COLOR_P1
        #     warning_p1 = ""
        if time_p1 <= 0:
            color_p1 = NORMAL_COLOR  # hoặc giữ màu cố định bạn muốn
            warning_p1 = ""
        elif time_p1 < 10:
            color_p1 = WARNING_COLOR if blink else ACTIVE_COLOR
            warning_p1 = "SAP HET GIO!"
        else:
            color_p1 = ACTIVE_COLOR if current_player == 0 else NORMAL_COLOR
            warning_p1 = ""

        # PLAYER 2
        # if time_p2 < 10:
        #     color_p2 = WARNING_COLOR if blink else ACTIVE_COLOR
        #     warning_p2 = "SAP HET GIO!"
        # else:
        #     color_p2 = WARNING_COLOR if current_player == 1 else NORMAL_COLOR
        #     warning_p2 = ""
        if time_p2 <= 0:
            color_p2 = NORMAL_COLOR  # giữ nguyên, không blink
            warning_p2 = ""
        elif time_p2 < 10:
            color_p2 = WARNING_COLOR if blink else ACTIVE_COLOR
            warning_p2 = "SAP HET GIO!"
        else:
            color_p2 = WARNING_COLOR if current_player == 1 else NORMAL_COLOR
            warning_p2 = ""

        # ===== PLAYER 1 (DƯỚI) =====
        txt_time_p1 = time_font.render(f"{format_time(display_time_p1)}", True, color_p1)
        # draw_timer_box(screen, 50, HEIGHT - 80, txt_time_p1)
        screen.blit(txt_time_p1, (520, HEIGHT - 80))

        if warning_p1:
            warn1 = small_font.render(warning_p1, True, (255, 0, 0))
            screen.blit(warn1, (630, HEIGHT - 140))

        # ===== PLAYER 2 (TRÊN) =====
        txt_time_p2 = time_font.render(f"{format_time(display_time_p2)}", True, color_p2)
        # draw_timer_box(screen, 50, 40, txt_time_p2)
        screen.blit(txt_time_p2, (415, 50))

        if warning_p2:
            warn2 = small_font.render(warning_p2, True, (255, 0, 0))
            screen.blit(warn2, (200, 70))


        # ====== VẼ MENU PAUSE (LUÔN VẼ TRÊN CÙNG) ======
        if paused:
            draw_pause_menu(screen, btn_continue, btn_restart, btn_quit, font)
            # overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # overlay.fill((0, 0, 0, 180))
            # screen.blit(overlay, (0, 0))
            #
            # pygame.draw.rect(screen, (200, 200, 200), btn_continue)
            # pygame.draw.rect(screen, (200, 200, 200), btn_restart)
            # pygame.draw.rect(screen, (200, 200, 200), btn_quit)
            #
            # screen.blit(font.render("Continue", True, (0, 0, 0)), btn_continue.move(30, 10))
            # screen.blit(font.render("Restart", True, (0, 0, 0)), btn_restart.move(30, 10))
            # screen.blit(font.render("Quit", True, (0, 0, 0)), btn_quit.move(60, 10))



        # --- BƯỚC 4: CẬP NHẬT FRAME ---
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        choice = run_menu(screen)

        if choice == "quit":
            pygame.quit()
            sys.exit()

        elif choice == "pvp":
            PLAY_WITH_AI = False
            play()

        elif choice == "ai":
            PLAY_WITH_AI = True
            play()