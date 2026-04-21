import pygame
import sys
from rule import run_rule
WIDTH, HEIGHT = 960, 720

menu_bg = pygame.image.load("assets/menu_bg.jpg")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

icon_rule = pygame.image.load("assets/icon_rule.png")
icon_rule = pygame.transform.scale(icon_rule, (40, 40))

icon_exit = pygame.image.load("assets/icon_exit.png")
icon_exit = pygame.transform.scale(icon_exit, (40, 40))

icon_rule_rect = pygame.Rect(850, 20, 60, 60)
icon_exit_rect = pygame.Rect(850, 100, 60, 60)

center_x = WIDTH // 2 - 350

btn_play_pvp = pygame.Rect(center_x, 470, 220, 50)
btn_play_ai  = pygame.Rect(center_x, 540, 220, 50)
#btn_rule = pygame.Rect(350, 390, 260, 60)
#btn_quit = pygame.Rect(350, 460, 260, 60)


def draw_button(screen, rect, text, btn_font):
    mouse = pygame.mouse.get_pos()

    color = (255, 170, 60) if rect.collidepoint(mouse) else (230, 140, 40)

    # nền nút
    pygame.draw.rect(screen, color, rect, border_radius=15)

    # viền
    pygame.draw.rect(screen, (120, 70, 20), rect, 2, border_radius=15)

    # chữ
    txt = btn_font.render(text, True, (30, 20, 10))
    screen.blit(txt, txt.get_rect(center=rect.center))

def draw_icon_button(screen, rect, icon):
    mouse = pygame.mouse.get_pos()

    # nền be vàng nâu
    color = (240, 200, 140) if rect.collidepoint(mouse) else (210, 170, 110)

    # nền
    pygame.draw.rect(screen, color, rect, border_radius=12)

    # viền nâu đậm
    pygame.draw.rect(screen, (120, 80, 30), rect, 2, border_radius=12)

    # icon ở giữa
    icon_rect = icon.get_rect(center=rect.center)
    screen.blit(icon, icon_rect)
def draw_menu(screen, font, btn_font):
    screen.blit(menu_bg, (0, 0))

    draw_button(screen, btn_play_pvp, "Choi 2 nguoi", btn_font)
    draw_button(screen, btn_play_ai, "Choi voi may", btn_font)
    draw_icon_button(screen, icon_rule_rect, icon_rule)
    draw_icon_button(screen, icon_exit_rect, icon_exit)



def run_menu(screen):
    pygame.font.init()

    font = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 60)
    btn_font = pygame.font.Font('assets/CaveatBrush-Regular.ttf', 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play_pvp.collidepoint(event.pos):
                    return "pvp"

                elif btn_play_ai.collidepoint(event.pos):
                    return "ai"

                elif icon_rule_rect.collidepoint(event.pos):
                    result = run_rule(screen)
                    if result == "quit":
                        return "quit"

                elif icon_exit_rect.collidepoint(event.pos):
                    return "quit"

        draw_menu(screen, font, btn_font)
        pygame.display.flip()