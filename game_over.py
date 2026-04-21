import pygame

def draw_game_over(screen, board, scores, font,
                   icon_restart, icon_exit,
                   icon_restart_rect, icon_exit_rect):

    # nền mờ
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    # kết quả
    if scores[0] > scores[1]:
        kq_text = "TI THANG!"
        color = (0, 255, 0)
    elif scores[1] > scores[0]:
        kq_text = "TEO THANG!"
        color = (0, 255, 0)
    else:
        kq_text = "HOA NHAU!"
        color = (255, 255, 0)

    text_go = font.render("GAME OVER", True, (255, 50, 50))
    text_kq = font.render(kq_text, True, color)

    screen.blit(text_go, text_go.get_rect(center=(480, 300)))
    screen.blit(text_kq, text_kq.get_rect(center=(480, 360)))

    # ===== HIỂN THỊ ĐIỂM =====
    score_text_p1 = font.render(f"Ti: {scores[0]}", True, (255, 255, 255))
    score_text_p2 = font.render(f"Teo: {scores[1]}", True, (255, 255, 255))

    WIDTH, HEIGHT = screen.get_size()

    y_score = HEIGHT // 2 + 60

    screen.blit(score_text_p1, score_text_p1.get_rect(center=(WIDTH // 2 - 120, y_score)))
    screen.blit(score_text_p2, score_text_p2.get_rect(center=(WIDTH // 2 + 120, y_score)))
    # ===== ICON BUTTON =====
    mouse = pygame.mouse.get_pos()

    def draw_btn(rect, icon):
        color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)

        color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)

        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, (120, 80, 30), rect, 2, border_radius=12)

        icon_rect = icon.get_rect(center=rect.center)
        screen.blit(icon, icon_rect)

    draw_btn(icon_restart_rect, icon_restart)
    draw_btn(icon_exit_rect, icon_exit)