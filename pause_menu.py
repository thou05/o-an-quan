import pygame

def draw_pause_menu(screen, btn_continue, btn_restart, btn_quit, font):
    mouse = pygame.mouse.get_pos()

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    card_rect = pygame.Rect(300, 160, 360, 400)
    pygame.draw.rect(screen, (255, 235, 180), card_rect, border_radius=25)
    pygame.draw.rect(screen, (200, 150, 50), card_rect, 3, border_radius=25)

    title = font.render("TAM DUNG", True, (80, 50, 10))
    screen.blit(title, title.get_rect(center=(480, 200)))

    def draw_btn(rect, text):
        color = (255, 210, 120) if rect.collidepoint(mouse) else (240, 180, 90)
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, (160, 110, 40), rect, 2, border_radius=15)

        txt = font.render(text, True, (50, 30, 10))
        screen.blit(txt, txt.get_rect(center=rect.center))

    draw_btn(btn_continue, "Tiep tuc")
    draw_btn(btn_restart, "Choi lai")
    draw_btn(btn_quit, "Thoat")