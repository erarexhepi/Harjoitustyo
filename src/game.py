import random
from src.markov import MarkovAI

ai = MarkovAI()

VALID_MOVES = ["kivi", "sakset", "paperi"]

def get_player_move():
    move = input("Valitse (kivi, sakset, paperi): ").strip().lower()
    while move not in VALID_MOVES:
        print("Virheellinen siirto. Yritä uudelleen.")
        move = input("Valitse (kivi, sakset, paperi): ").strip().lower()
    return move

def get_ai_move():
    return ai.counter_move()

def determine_winner(player, ai):
    if player == ai:
        return "Tasapeli!"
    elif (player == "kivi" and ai == "sakset") or \
         (player == "sakset" and ai == "paperi") or \
         (player == "paperi" and ai == "kivi"):
        return "Voitit!"
    else:
        return "Hävisit."

def play_round():
    player_move = get_player_move()
    ai_move = get_ai_move()
    
    ai.update_history(player_move)
    
    print(f"\nSinä valitsit: {player_move}")
    print(f"AI valitsi: {ai_move}")
    
    result = determine_winner(player_move, ai_move)
    print(result)

if __name__ == "__main__":
    play_round()