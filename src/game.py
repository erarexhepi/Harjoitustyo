import random
import time
import sys
import os
from typing import Dict, Tuple

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(__file__))

try:
    from markov import MarkovAI
except ImportError:
    from src.markov import MarkovAI

class GameStats:
    def __init__(self):
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.total_games = 0
        self.game_history = []
    
    def add_result(self, result: str, player_move: str, ai_move: str):
        self.total_games += 1
        self.game_history.append({
            'round': self.total_games,
            'player': player_move,
            'ai': ai_move,
            'result': result
        })
        
        if result == "player":
            self.player_wins += 1
        elif result == "ai":
            self.ai_wins += 1
        else:
            self.ties += 1
    
    def get_win_percentage(self) -> float:
        """pelaajan voittoprosentti"""
        if self.total_games == 0:
            return 0.0
        return (self.player_wins / self.total_games) * 100
    
    def get_summary(self) -> str:
        if self.total_games == 0:
            return "Ei pelejä pelattu vielä."
        
        win_pct = self.get_win_percentage()
        return f"""
📊 PELITILASTOT
{'='*50}
🎮 Pelatut kierrokset: {self.total_games}
🏆 Sinun voittosi: {self.player_wins} ({win_pct:.1f}%)
🤖 AI:n voitot: {self.ai_wins} ({(self.ai_wins/self.total_games)*100:.1f}%)
🤝 Tasapelit: {self.ties} ({(self.ties/self.total_games)*100:.1f}%)
"""

class VisualGame:
    """Visuaalisesti parannettu peli"""
    
    MOVES = {
        "kivi": {"emoji": "🗿", "beats": "sakset", "loses_to": "paperi"},
        "paperi": {"emoji": "📄", "beats": "kivi", "loses_to": "sakset"},
        "sakset": {"emoji": "✂️", "beats": "paperi", "loses_to": "kivi"}
    }
    
    VALID_MOVES = list(MOVES.keys())
    
    def __init__(self):
        self.ai = MarkovAI(max_depth=5)
        self.stats = GameStats()
    
    def print_banner(self):
        """Tulosta pelin banneri"""
        banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        KIVI-SAKSET-PAPERI                    ║
    ║                        AI VASTAAN IHMINEN                    ║
    ╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_moves_guide(self):
        """Tulosta siirtojen opas"""
        print("\n SIIRROT:")
        for move, data in self.MOVES.items():
            print(f"   {data['emoji']} {move.capitalize()}")
        print()
    
    def get_player_move(self) -> str:
        while True:
            move = input("Valitse (kivi/sakset/paperi) \ntai 'help/h'/'quit/q'/'stats/s': ").strip().lower()
            
            if move == 'quit' or move == 'q':
                return 'quit'
            elif move == 'help' or move == 'h':
                self.show_help()
                continue
            elif move == 'stats' or move == 's':
                self.show_detailed_stats()
                continue
            elif move in self.VALID_MOVES:
                return move
            else:
                print("Virheellinen siirto! Kokeile uudelleen.")
    
    def show_help(self):
        """Näytä ohje"""
        help_text = """
 OHJE:
• Kivi 🗿 voittaa Sakset ✂️
• Sakset ✂️ voittaa Paperi 📄  
• Paperi 📄 voittaa Kivi 🗿

 KOMENNOT:
• help/h - Näytä tämä ohje
• stats/s - Näytä yksityiskohtaiset tilastot
• quit/q - Lopeta peli

AI oppii pelityylistäsi ja yrittää ennustaa seuraavan siirtosi!
        """
        print(help_text)
    
    def show_detailed_stats(self):
        print(self.stats.get_summary())
        
        # AI:n oppimistilastot
        ai_stats = self.ai.get_stats()
        model_info = self.ai.get_current_model_info()
        
        print("AI:N OPPIMISTILASTOT:")
        print("="*50)
        for depth, stat in ai_stats.items():
            if stat['total'] > 0:
                current_marker = " ← KÄYTÖSSÄ" if depth == model_info['current_model'] else ""
                print(f"Aste {depth} (historia {depth} siirtoa): {stat['win_rate']:.1%} ({stat['wins']}/{stat['total']}){current_marker}")
        
        if model_info['current_model']:
            print(f"\nNykyinen malli: Aste {model_info['current_model']}")
            print(f"Kierroksia jäljellä mallilla: {model_info['games_left']}")
        else:
            print("\nEi aktiivista mallia (käytetään satunnaisia siirtoja)")
        
        # Viimeisimmät pelit
        if len(self.stats.game_history) > 0:
            print("\nVIIMEISET 5 PELIÄ:")
            print("-"*50)
            recent_games = self.stats.game_history[-5:]
            for game in recent_games:
                result_emoji = "🏆" if game['result'] == 'player' else "🤖" if game['result'] == 'ai' else "🤝"
                player_emoji = self.MOVES[game['player']]['emoji']
                ai_emoji = self.MOVES[game['ai']]['emoji']
                print(f"#{game['round']}: {player_emoji} vs {ai_emoji} {result_emoji}")
        print()
    
    def show_moves(self, player_move: str, ai_move: str):
        player_emoji = self.MOVES[player_move]['emoji']
        ai_emoji = self.MOVES[ai_move]['emoji']
        
        print("\n" + "="*60)
        print(f"👤 SINÄ:  {player_emoji} {player_move.upper()}")
        print(f"🤖 AI:    {ai_emoji} {ai_move.upper()}")
        print("="*60)
    
    def determine_winner(self, player_move: str, ai_move: str) -> Tuple[str, str]:
        if player_move == ai_move:
            return "tie", f"🤝 TASAPELI! Molemmat valitsivat {self.MOVES[player_move]['emoji']}"
        elif self.MOVES[player_move]['beats'] == ai_move:
            return "player", f"🎉 VOITIT! {self.MOVES[player_move]['emoji']} voittaa {self.MOVES[ai_move]['emoji']}"
        else:
            return "ai", f"😤 HÄVISIT! {self.MOVES[ai_move]['emoji']} voittaa {self.MOVES[player_move]['emoji']}"
    
    def play_round(self) -> bool:
        print(f"\n KIERROS {self.stats.total_games + 1}")
        print("-" * 30)
        
        player_move = self.get_player_move()
        if player_move == 'quit':
            return False
        
        ai_move = self.ai.counter_move()
        
        self.show_moves(player_move, ai_move)
        
        result, message = self.determine_winner(player_move, ai_move)
        print(f"\n{message}")
        
        # Päivitä tilastot
        self.stats.add_result(result, player_move, ai_move)
        self.ai.update_win_stats(player_move, ai_move)
        self.ai.update_history(player_move)
        
        win_pct = self.stats.get_win_percentage()
        print(f"\nTilanne: Sinä {self.stats.player_wins} - {self.stats.ai_wins} AI (voitto% {win_pct:.1f}%)")
        
        model_info = self.ai.get_current_model_info()
        if model_info['current_model']:
            print(f"AI käyttää mallia: Aste {model_info['current_model']} ({model_info['games_left']} kierrosta jäljellä)")
        
        return True
    
    def show_final_stats(self):
        """Näytä lopputilastot"""
        print("\n" + "="*60)
        print("🏁 PELI PÄÄTTYI!")
        print(self.stats.get_summary())
        
        # AI:n oppimistulokset
        ai_stats = self.ai.get_stats()
        best_depth = 0
        best_rate = 0
        
        for depth, stat in ai_stats.items():
            if stat['total'] > 0 and stat['win_rate'] > best_rate:
                best_rate = stat['win_rate']
                best_depth = depth
        
        if best_depth > 0:
            print(f"🧠 AI:n paras oppimisaste: {best_depth} ({best_rate:.1%} voittoprosentti)")
  
        if self.stats.get_win_percentage() > 60:
            print("\n🏆 Mahtava suoritus! Voitit AI:n!")
        elif self.stats.get_win_percentage() > 40:
            print("\n  Tasainen taistelu!")
        else:
            print("\nAI dominoi peliä!")
        
        print("\nKiitos pelistä!")
    
    def main_game_loop(self):
        """Pelin pääsilmukka"""
        self.print_banner()
        self.print_moves_guide()
        
        print(" Kirjoita 'help' saadaksesi ohjeita tai 'quit/q' lopettaaksesi.")
        print(" AI käyttää parhaiten menestynyttä mallia 5 kierrosta kerrallaan.\n")
        
        try:
            while True:
                if not self.play_round():
                    break
                
                if self.stats.total_games > 0 and self.stats.total_games % 5 == 0:
                    continue_game = input(f"\n🤔 Jatketaanko? (y/n): ").strip().lower()
                    if continue_game in ['n', 'no', 'ei']:
                        break
        
        except KeyboardInterrupt:
            print("\n\n  Peli keskeytetty!")
        
        finally:
            self.show_final_stats()

if __name__ == "__main__":
    game = VisualGame()
    game.main_game_loop()