from play_ui import *


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