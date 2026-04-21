import pygame
from constants import *

icon_restart = pygame.image.load("assets/icon_restart.png")
icon_restart = pygame.transform.scale(icon_restart, (40, 40))
icon_restart_rect = pygame.Rect(400, 450, 60, 60)


def draw_button_base(screen, rect, text=None, icon=None, font=None):
    mouse = pygame.mouse.get_pos()
    color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)

    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, (120, 80, 30), rect, 2, border_radius=12)

    if text and font:
        txt = font.render(text, True, (30, 20, 10))
        screen.blit(txt, txt.get_rect(center=rect.center))

    if icon:
        icon_rect = icon.get_rect(center=rect.center)
        screen.blit(icon, icon_rect)

#======PAUSE========
def draw_pause_menu(screen, btn_continue, btn_restart, btn_quit, font):
    mouse = pygame.mouse.get_pos()

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    # card_rect = pygame.Rect(300, 160, 360, 400)
    WIDTH, HEIGHT = screen.get_size()
    card_rect = pygame.Rect(0, 0, 360, 400)
    card_rect.center = (WIDTH // 2, HEIGHT // 2)

    pygame.draw.rect(screen, (255, 235, 180), card_rect, border_radius=25)
    pygame.draw.rect(screen, (200, 150, 50), card_rect, 3, border_radius=25)

    title = font.render("TAM DUNG", True, (80, 50, 10))
    screen.blit(title, title.get_rect(center=(480, 200)))

    # def draw_btn(rect, text):
    #     color = (255, 210, 120) if rect.collidepoint(mouse) else (240, 180, 90)
    #     pygame.draw.rect(screen, color, rect, border_radius=15)
    #     pygame.draw.rect(screen, (160, 110, 40), rect, 2, border_radius=15)
    #
    #     txt = font.render(text, True, (50, 30, 10))
    #     screen.blit(txt, txt.get_rect(center=rect.center))
    #
    # draw_btn(btn_continue, "Tiep tuc")
    # draw_btn(btn_restart, "Choi lai")
    # draw_btn(btn_quit, "Thoat")
    draw_button_base(screen, btn_continue, text="Tiep tuc", font=font)
    draw_button_base(screen, btn_restart, text="Choi lai", font=font)
    draw_button_base(screen, btn_quit, text="Thoat", font=font)


#=====GAME OVER========
# def draw_game_over(screen, board, scores, font,
#                    icon_restart, icon_exit,
#                    icon_restart_rect, icon_exit_rect):
#
#     # nền mờ
#     overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
#     overlay.fill((0, 0, 0, 150))
#     screen.blit(overlay, (0, 0))
#
#     # kết quả
#     if scores[0] > scores[1]:
#         kq_text = "TI THANG!"
#         color = (0, 255, 0)
#     elif scores[1] > scores[0]:
#         kq_text = "TEO THANG!"
#         color = (0, 255, 0)
#     else:
#         kq_text = "HOA NHAU!"
#         color = (255, 255, 0)
#
#     text_go = font.render("GAME OVER", True, (255, 50, 50))
#     text_kq = font.render(kq_text, True, color)
#
#     screen.blit(text_go, text_go.get_rect(center=(480, 300)))
#     screen.blit(text_kq, text_kq.get_rect(center=(480, 360)))
#
#     # ===== HIỂN THỊ ĐIỂM =====
#     score_text_p1 = font.render(f"Ti: {scores[0]}", True, (255, 255, 255))
#     score_text_p2 = font.render(f"Teo: {scores[1]}", True, (255, 255, 255))
#
#     WIDTH, HEIGHT = screen.get_size()
#
#     y_score = HEIGHT // 2 + 60
#
#     screen.blit(score_text_p1, score_text_p1.get_rect(center=(WIDTH // 2 - 120, y_score)))
#     screen.blit(score_text_p2, score_text_p2.get_rect(center=(WIDTH // 2 + 120, y_score)))
#     # ===== ICON BUTTON =====
#     mouse = pygame.mouse.get_pos()
#
#
#     draw_button_base(screen, icon_restart_rect, icon=icon_restart)
#     draw_button_base(screen, icon_exit_rect, icon=icon_exit)

# def draw_game_over(screen, scores, font, btn_restart, btn_quit):
def draw_game_over(screen, scores, font, icon_restart, icon_exit, icon_restart_rect, icon_exit_rect):
    WIDTH, HEIGHT = screen.get_size()

    # ===== NỀN MỜ =====
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    # ===== CARD CHÍNH =====
    card = pygame.Rect(0, 0, 500, 400)
    card.center = (WIDTH // 2, HEIGHT // 2)

    pygame.draw.rect(screen, (255, 235, 180), card, border_radius=25)
    pygame.draw.rect(screen, (200, 150, 50), card, 3, border_radius=25)

    # ===== TITLE =====
    title_font = pygame.font.Font(FONT, 70)

    if scores[0] > scores[1]:
        winner = "TI THANG"
    elif scores[1] > scores[0]:
        winner = "TEO THANG"
    else:
        winner = "HOA NHAU"

    title = title_font.render(winner, True, (80, 50, 10))
    screen.blit(title, title.get_rect(center=(card.centerx, card.top + 60)))

    # ===== CHIA 2 BÊN =====
    mid_x = card.centerx
    pygame.draw.line(screen, (120, 80, 30),
                     (mid_x, card.top + 150),
                     (mid_x, card.bottom - 130), 3)

    # ===== FONT =====
    label_font = pygame.font.Font(FONT, 28)
    score_font = pygame.font.Font(FONT, 50)

    # ===== BÊN TRÁI (WINNER) =====
    left_x = card.left + 180

    txt_score1 = score_font.render(str(scores[0]), True, (30, 20, 10))
    screen.blit(txt_score1, txt_score1.get_rect(center=(left_x, card.centery - 20)))

    txt_label1 = label_font.render("Tí", True, (80, 50, 10))
    screen.blit(txt_label1, txt_label1.get_rect(center=(left_x, card.centery + 40)))

    # ===== BÊN PHẢI =====
    right_x = card.right - 180

    txt_score2 = score_font.render(str(scores[1]), True, (30, 20, 10))
    screen.blit(txt_score2, txt_score2.get_rect(center=(right_x, card.centery - 20)))

    txt_label2 = label_font.render("Tèo", True, (80, 50, 10))
    screen.blit(txt_label2, txt_label2.get_rect(center=(right_x, card.centery + 40)))

    # ===== BUTTON =====
    # btn_restart.center = (card.centerx - 120, card.bottom - 50)
    # btn_quit.center    = (card.centerx + 120, card.bottom - 50)

    # draw_button_base(screen, btn_restart, text="Chơi lại", font=label_font)
    # draw_button_base(screen, btn_quit, text="Thoát", font=label_font)
    # draw_button_base(screen, icon_restart_rect, icon=icon_restart)
    # draw_button_base(screen, icon_exit_rect, icon=icon_exit)
    # padding = 15
    # icon_restart_rect.topright = (card.right - padding - 70, card.top + padding)
    # icon_exit_rect.topright = (card.right - padding, card.top + padding)
    padding = 15

    icon_exit_rect.bottomright = (card.right - padding, card.bottom - padding)
    icon_restart_rect.bottomright = (card.right - padding - 60, card.bottom - padding)
    draw_button_base(screen, icon_restart_rect, icon=icon_restart)
    draw_button_base(screen, icon_exit_rect, icon=icon_exit)
#=====RULE========

# nút thoát

icon_exit = pygame.image.load(EXIT)
icon_exit = pygame.transform.scale(icon_exit, (40, 40))
icon_exit_rect = pygame.Rect(850, 20, 60, 60)

# def draw_icon_exit_button(screen, rect, text, font):
#     mouse = pygame.mouse.get_pos()
#
#     color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)
#
#     # SHADOW
#     shadow = rect.copy()
#     shadow.y += 3
#     pygame.draw.rect(screen, (100, 70, 30), shadow, border_radius=12)
#
#     # NỀN
#     pygame.draw.rect(screen, color, rect, border_radius=12)
#
#     # VIỀN
#     pygame.draw.rect(screen, (120, 80, 30), rect, 2, border_radius=12)
#
#     # ICON
#     icon_rect = icon_exit.get_rect(center=rect.center)
#     screen.blit(icon_exit, icon_rect)
def draw_rule(screen, font):
    screen.fill((50, 100, 50))
    title_font = pygame.font.Font(FONT, 50)
    title = title_font.render("LUAT CHOI", True, (255, 255, 0))
    screen.blit(title, (WIDTH // 2 - 120, 60))

    lines = [
        "- Moi nguoi chon 1 o de rai",
        "- Gap o trong thi an",
        "- An duoc nhieu hon thi thang",
    ]

    y = 150
    for line in lines:
        txt = font.render(line, True, (255,255,255))
        screen.blit(txt, (150, y))
        y += 50


def run_rule(screen):
    font = pygame.font.Font(FONT, 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if icon_exit_rect.collidepoint(event.pos):
                    return "back"

        draw_rule(screen, font)
        # vẽ icon thoát
        # draw_button(screen, icon_exit_rect, "", font)
        draw_button_base(screen, rule_exit_rect, icon=icon_exit)
        pygame.display.flip()


#=====MENU========


menu_bg = pygame.image.load(MENU_BACKGROUND)
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

icon_rule = pygame.image.load(RULE)
icon_rule = pygame.transform.scale(icon_rule, (40, 40))

icon_exit = pygame.image.load(EXIT)
icon_exit = pygame.transform.scale(icon_exit, (40, 40))

rule_exit_rect  = pygame.Rect(850, 20, 60, 60)
menu_exit_rect  = pygame.Rect(850, 100, 60, 60)

center_x = WIDTH // 2 - 350

btn_play_pvp = pygame.Rect(center_x, 470, 220, 50)
btn_play_ai  = pygame.Rect(center_x, 540, 220, 50)


# def draw_menu_button(screen, rect, text, btn_font):
#     mouse = pygame.mouse.get_pos()
#
#     color = (255, 170, 60) if rect.collidepoint(mouse) else (230, 140, 40)
#
#     # nền nút
#     pygame.draw.rect(screen, color, rect, border_radius=15)
#
#     # viền
#     pygame.draw.rect(screen, (120, 70, 20), rect, 2, border_radius=15)
#
#     # chữ
#     txt = btn_font.render(text, True, (30, 20, 10))
#     screen.blit(txt, txt.get_rect(center=rect.center))

# def draw_icon_button(screen, rect, icon):
#     mouse = pygame.mouse.get_pos()
#
#     # nền be vàng nâu
#     color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)
#
#     # nền
#     pygame.draw.rect(screen, color, rect, border_radius=12)
#
#     # viền nâu đậm
#     pygame.draw.rect(screen, (120, 80, 30), rect, 2, border_radius=12)
#
#     # icon ở giữa
#     icon_rect = icon.get_rect(center=rect.center)
#     screen.blit(icon, icon_rect)


def draw_menu(screen, font, btn_font):
    screen.blit(menu_bg, (0, 0))

    # draw_button(screen, btn_play_pvp, "Choi 2 nguoi", btn_font)
    # draw_button(screen, btn_play_ai, "Choi voi may", btn_font)
    # draw_icon_button(screen, icon_rule_rect, icon_rule)
    # draw_icon_button(screen, icon_exit_rect, icon_exit)
    draw_button_base(screen, btn_play_pvp, text="Choi 2 nguoi", font=btn_font)
    draw_button_base(screen, btn_play_ai, text="Choi voi may", font=btn_font)
    draw_button_base(screen, menu_exit_rect, icon=icon_rule)
    draw_button_base(screen, icon_exit_rect, icon=icon_exit)


def run_menu(screen):
    pygame.font.init()

    font = pygame.font.Font(FONT, 60)
    btn_font = pygame.font.Font(FONT, 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play_pvp.collidepoint(event.pos):
                    return "pvp"

                elif btn_play_ai.collidepoint(event.pos):
                    return "ai"

                elif rule_exit_rect.collidepoint(event.pos):
                    result = run_rule(screen)
                    if result == "quit":
                        return "quit"

                elif icon_exit_rect.collidepoint(event.pos):
                    return "quit"

        draw_menu(screen, font, btn_font)
        pygame.display.flip()