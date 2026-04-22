from play_ui import *


if __name__ == "__main__":
    while True:
        choice = run_menu(screen)

        if choice == "quit":
            pygame.quit()
            sys.exit()

        elif choice == "pvp":
            play(play_with_ai=False)

        elif choice == "ai":
            play(play_with_ai=True)