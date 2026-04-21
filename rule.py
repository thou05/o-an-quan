import pygame

WIDTH, HEIGHT = 960, 720

# nút thoát

icon_exit = pygame.image.load("assets/icon_exit.png")
icon_exit = pygame.transform.scale(icon_exit, (40, 40))

icon_exit_rect = pygame.Rect(850, 20, 60, 60)
def draw_button(screen, rect, text, font):
    mouse = pygame.mouse.get_pos()

    color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)

    # SHADOW
    shadow = rect.copy()
    shadow.y += 3
    pygame.draw.rect(screen, (100, 70, 30), shadow, border_radius=12)

    # NỀN
    pygame.draw.rect(screen, color, rect, border_radius=12)

    # VIỀN
    pygame.draw.rect(screen, (120, 80, 30), rect, 2, border_radius=12)

    # ICON
    icon_rect = icon_exit.get_rect(center=rect.center)
    screen.blit(icon_exit, icon_rect)
def draw_rule(screen, font):
    screen.fill((50, 100, 50))
    title_font = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 50)
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

    # nút thoát


def run_rule(screen):
    font = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 35)

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
        draw_button(screen, icon_exit_rect, "", font)
        pygame.display.flip()