

import pygame
import sys

pygame.init()
bg_image = pygame.image.load('background.png')
screen = pygame.display.set_mode(bg_image.get_size())
pygame.display.set_caption("Tool Lấy Tọa Độ Rect")

clicks = []

print("HƯỚNG DẪN:")
print("- Để lấy Rect 1 ô dân: Click góc trên-trái, sau đó click góc dưới-phải của ô đó.")
print("- Tool sẽ tự tính width, height và in ra code cho bạn copy.\n")

while True:
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicks.append(event.pos)
            print(f"Chấm điểm {len(clicks)}: {event.pos}")

            # Cứ mỗi 2 lần click, tạo ra 1 Rect
            if len(clicks) == 2:
                x1, y1 = clicks[0]
                x2, y2 = clicks[1]

                # Tự động tính Width, Height và tọa độ góc trên cùng
                w = abs(x2 - x1)
                h = abs(y2 - y1)
                top_x = min(x1, x2)
                top_y = min(y1, y2)

                print(f"--> HÃY COPY DÒNG NÀY: pygame.Rect({top_x}, {top_y}, {w}, {h})\n")
                clicks = []  # Reset lại để đo ô tiếp theo

    pygame.display.flip()