import random
from collections import defaultdict

class MarkovAI:
    def __init__(self):
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.prev_move = None

    def update_history(self, player_move: str):
        if self.prev_move is not None:
            self.transition_counts[self.prev_move][player_move] += 1
        self.prev_move = player_move

    def predict_next(self) -> str:
        if self.prev_move is None:
            return random.choice(["kivi", "sakset", "paperi"])

        next_moves = self.transition_counts[self.prev_move]
        if not next_moves:
            return random.choice(["kivi", "sakset", "paperi"])

        # Eniten esiintynyt
        predicted_move = max(next_moves, key=next_moves.get)
        return predicted_move

    def counter_move(self) -> str:
        prediction = self.predict_next()
        counters = {
            "kivi": "paperi",
            "paperi": "sakset",
            "sakset": "kivi"
        }
        return counters[prediction]