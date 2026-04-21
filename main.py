import pygame
import sys
from menu import run_menu
import gamegame

def main():
    pygame.init()
    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption("Ô Ăn Quan")

    while True:
        choice = run_menu(screen)

        if choice == "quit":
            pygame.quit()
            sys.exit()

        elif choice == "pvp":
            gamegame.run_game(screen, play_with_ai=False)

        elif choice == "ai":
            gamegame.run_game(screen, play_with_ai=True)


if __name__ == "__main__":
    main()