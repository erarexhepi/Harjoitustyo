
def main():
    try:
        from src.game import VisualGame
        game = VisualGame()
        game.main_game_loop()
    except ImportError as e:
        print(f"Virhe: {e}")
    except KeyboardInterrupt:
        print("\nPeli keskeytetty.")

if __name__ == "__main__":
    main()