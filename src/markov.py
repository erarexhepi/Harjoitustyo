import random
from collections import defaultdict

class MarkovAI:
    def __init__(self, max_depth=5):
        self.transition_counts = {}
        self.win_stats = {}
        
        for depth in range(1, max_depth + 1):
            self.transition_counts[depth] = defaultdict(lambda: defaultdict(int))
            self.win_stats[depth] = {'wins': 0, 'total': 0}
        
        self.history = []
        self.max_depth = max_depth

    def update_history(self, player_move: str):
        self.history.append(player_move)
        
        #päivitä siirtymälaskurit kaikille asteille
        for depth in range(1, min(len(self.history), self.max_depth) + 1):
            if len(self.history) > depth:
                #depth-pituinen sekvenssi historiasta
                sequence = tuple(self.history[-depth-1:-1])
                next_move = self.history[-1]
                self.transition_counts[depth][sequence][next_move] += 1

    def predict_next(self):
        predictions = {}
        
        # Kokeile kaikkia asteita syvimmästä pinnallisimpaan
        for depth in range(min(len(self.history), self.max_depth), 0, -1):
            if len(self.history) >= depth:
                sequence = tuple(self.history[-depth:])
                next_moves = self.transition_counts[depth][sequence]
                
                if next_moves:
                    # Löytyi ennuste tälle asteelle
                    predicted_move = max(next_moves, key=next_moves.get)
                    predictions[depth] = predicted_move
                    
        return predictions

    def counter_move(self):
        predictions = self.predict_next()
        
        if not predictions:
            return random.choice(["kivi", "sakset", "paperi"])
        
        # Käytä syvintä ennustetta
        depth = max(predictions.keys())
        prediction = predictions[depth]
        
        counters = {
            "kivi": "paperi",
            "paperi": "sakset",
            "sakset": "kivi"
        }
        return counters[prediction]

    def update_win_stats(self, player_move: str, ai_move: str):
        predictions = self.predict_next()
        
        # Määritä voittiko AI
        ai_won = self._ai_wins(player_move, ai_move)
        
        for depth in predictions.keys():
            self.win_stats[depth]['total'] += 1
            if ai_won:
                self.win_stats[depth]['wins'] += 1
            
            break

    def _ai_wins(self, player_move: str, ai_move: str) -> bool:
        if player_move == ai_move:
            return False  # Tasapeli
        
        winning_combinations = {
            ("kivi", "sakset"): False,    # Pelaaja voittaa
            ("sakset", "paperi"): False,  # Pelaaja voittaa  
            ("paperi", "kivi"): False,    # Pelaaja voittaa
            ("sakset", "kivi"): True,     # AI voittaa
            ("paperi", "sakset"): True,   # AI voittaa
            ("kivi", "paperi"): True      # AI voittaa
        }
        
        return winning_combinations.get((player_move, ai_move), False)

    def get_stats(self):
        stats = {}
        for depth in range(1, self.max_depth + 1):
            total = self.win_stats[depth]['total']
            wins = self.win_stats[depth]['wins']
            win_rate = wins / total if total > 0 else 0
            stats[depth] = {
                'win_rate': win_rate,
                'wins': wins,
                'total': total
            }
        return stats