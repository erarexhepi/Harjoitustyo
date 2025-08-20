
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from src.markov import MarkovAI
except ImportError:
    print("Ei voitu tuoda MarkovAI. Tarkista että src/markov.py löytyy.")
    sys.exit(1)

class TestRunner:    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.current_test = ""
    
    def run_test(self, test_name, test_func):
        self.current_test = test_name
        try:
            test_func()
            print(f"✓ {test_name}")
            self.passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {str(e)}")
            self.failed += 1
    
    def assert_equal(self, actual, expected, message=""):
        if actual != expected:
            raise AssertionError(f"{message} - Odotettiin {expected}, saatiin {actual}")
    
    def assert_true(self, condition, message=""):
        if not condition:
            raise AssertionError(f"{message} - Ehto oli False")
    
    def assert_in(self, item, container, message=""):
        if item not in container:
            raise AssertionError(f"{message} - {item} ei löytynyt kohdasta {container}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\nYhteenveto: {self.passed}/{total} testiä onnistui")
        return self.failed == 0

runner = TestRunner()

def test_basic_initialization():
    ai = MarkovAI(max_depth=3)
    
    runner.assert_equal(ai.max_depth, 3, "Max depth")
    runner.assert_equal(len(ai.history), 0, "Historia tyhjä")
    runner.assert_equal(ai.current_model, None, "Ei aktiivista mallia")
    runner.assert_equal(ai.model_games_left, 0, "Ei pelejä jäljellä")
    
    for depth in range(1, 4):
        runner.assert_true(depth in ai.transition_counts, f"Syvyys {depth} transition_counts:issa")
        runner.assert_true(depth in ai.win_stats, f"Syvyys {depth} win_stats:issa")

def test_history_updates():
    ai = MarkovAI(max_depth=3)
    
    ai.update_history("kivi")
    runner.assert_equal(len(ai.history), 1, "Historia koko 1")
    runner.assert_equal(ai.history[0], "kivi", "Ensimmäinen siirto")
    
    ai.update_history("paperi")
    runner.assert_equal(len(ai.history), 2, "Historia koko 2")
    runner.assert_equal(ai.transition_counts[1][("kivi",)]["paperi"], 1, "Siirtymä kivi->paperi")
    
    ai.update_history("sakset")
    runner.assert_equal(ai.transition_counts[1][("paperi",)]["sakset"], 1, "Siirtymä paperi->sakset")
    runner.assert_equal(ai.transition_counts[2][("kivi", "paperi")]["sakset"], 1, "Aste 2 siirtymä")

def test_counter_move_validity():
    ai = MarkovAI(max_depth=2)
    valid_moves = ["kivi", "paperi", "sakset"]
    
    # Testaa tyhjällä historialla
    for _ in range(10):
        move = ai.counter_move()
        runner.assert_in(move, valid_moves, "Vastaliike validi")
    
    # Testaa historian kanssa
    ai.update_history("kivi")
    ai.update_history("paperi")
    
    for _ in range(10):
        move = ai.counter_move()
        runner.assert_in(move, valid_moves, "Vastaliike validi historialla")

def test_prediction_logic():
    ai = MarkovAI(max_depth=3)
    
    moves = ["kivi", "paperi", "sakset", "kivi"]
    for move in moves:
        ai.update_history(move)
    
    predictions = ai.predict_next()
    
    for depth, prediction in predictions.items():
        runner.assert_in(prediction, ["kivi", "paperi", "sakset"], f"Ennuste syvyydellä {depth}")
        runner.assert_true(depth >= 1 and depth <= 3, f"Syvyys {depth} validissa välissä")

def test_win_calculation():
    ai = MarkovAI()
    
    # AI voittaa
    runner.assert_true(ai._ai_wins("kivi", "paperi"), "Paperi voittaa kiven")
    runner.assert_true(ai._ai_wins("paperi", "sakset"), "Sakset voittaa paperin")
    runner.assert_true(ai._ai_wins("sakset", "kivi"), "Kivi voittaa sakset")
    
    # Pelaaja voittaa
    runner.assert_true(not ai._ai_wins("kivi", "sakset"), "Kivi voittaa sakset")
    runner.assert_true(not ai._ai_wins("paperi", "kivi"), "Paperi voittaa kiven")
    runner.assert_true(not ai._ai_wins("sakset", "paperi"), "Sakset voittaa paperin")
    
    # Tasapelit
    runner.assert_true(not ai._ai_wins("kivi", "kivi"), "Tasapeli kivi")
    runner.assert_true(not ai._ai_wins("paperi", "paperi"), "Tasapeli paperi")
    runner.assert_true(not ai._ai_wins("sakset", "sakset"), "Tasapeli sakset")

def test_model_selection():
    ai = MarkovAI(max_depth=3)
    
    ai.win_stats[1] = {'wins': 6, 'total': 10}  # 60%
    ai.win_stats[2] = {'wins': 8, 'total': 10}  # 80% - paras
    ai.win_stats[3] = {'wins': 4, 'total': 10}  # 40%
    
    ai.history = ["kivi", "paperi", "sakset", "kivi"]
    for depth in [1, 2, 3]:
        seq_len = min(depth, len(ai.history))
        sequence = tuple(ai.history[-seq_len:])
        ai.transition_counts[depth][sequence]["paperi"] = 1
    
    best_model = ai.select_best_model()
    runner.assert_equal(best_model, 2, "Paras malli valittu (80% voittoprosentti)")

def test_five_game_persistence():
    """Testaa 5-pelin persistenssi"""
    ai = MarkovAI(max_depth=2)
    
    #Tilanne jossa malli voidaan valita
    ai.win_stats[1] = {'wins': 7, 'total': 10}
    ai.history = ["kivi", "paperi"]
    ai.transition_counts[1][("paperi",)]["kivi"] = 1
    
    move1 = ai.counter_move()
    runner.assert_equal(ai.current_model, 1, "Malli valittu")
    runner.assert_equal(ai.model_games_left, 4, "4 peliä jäljellä")
    
    for expected_left in [3, 2, 1, 0]:
        ai.counter_move()
        runner.assert_equal(ai.model_games_left, expected_left, f"{expected_left} peliä jäljellä")
    
    ai.counter_move()
    runner.assert_equal(ai.model_games_left, 4, "Uusi jakso alkanut")

def test_stats_consistency():
    ai = MarkovAI(max_depth=2)
    
    ai.current_model = 1
    ai.model_games_left = 3
    ai.history = ["kivi", "paperi"]
    ai.transition_counts[1][("paperi",)]["sakset"] = 1
    
    initial_stats = ai.get_stats()[1].copy()
    
    ai.update_win_stats("sakset", "kivi")
    current_stats = ai.get_stats()[1]
    
    runner.assert_equal(current_stats['total'], initial_stats['total'] + 1, "Total kasvanut")
    runner.assert_equal(current_stats['wins'], initial_stats['wins'] + 1, "Wins kasvanut")
    
    expected_rate = current_stats['wins'] / current_stats['total']
    runner.assert_equal(current_stats['win_rate'], expected_rate, "Win rate oikein")

def test_long_game_simulation():
    ai = MarkovAI(max_depth=3)
    
    for round_num in range(50):
        player_move = ["kivi", "paperi", "sakset"][round_num % 3]
        ai_move = ai.counter_move()
        
        runner.assert_in(ai_move, ["kivi", "paperi", "sakset"], f"AI siirto kierros {round_num}")
        
        ai.update_win_stats(player_move, ai_move)
        ai.update_history(player_move)
    
    runner.assert_equal(len(ai.history), 50, "Historia oikean pituinen")
    
    stats = ai.get_stats()
    learned = any(stat['total'] > 0 for stat in stats.values())
    runner.assert_true(learned, "AI oppi jotain 50 kierroksessa")

def run_all_tests():
    print("MARKOV AI - YKSINKERTAISET TESTIT")
    print("=" * 50)
    print("Suoritetaan testit ilman ulkoisia riippuvuuksia...\n")
    
    # Lista testeistä
    tests = [
        ("Perusominaisuudet", test_basic_initialization),
        ("Historia päivitys", test_history_updates),
        ("Vastaliikkeen validius", test_counter_move_validity),
        ("Ennustuslogiikka", test_prediction_logic),
        ("Voittolaskenta", test_win_calculation),
        ("Mallin valinta", test_model_selection),
        ("5-pelin persistenssi", test_five_game_persistence),
        ("Tilastojen johdonmukaisuus", test_stats_consistency),
        ("Pitkä peli", test_long_game_simulation)
    ]
    
    for test_name, test_func in tests:
        runner.run_test(test_name, test_func)
    
    print("\n" + "=" * 50)
    success = runner.summary()
    
    if success:
        print("KAIKKI TESTIT ONNISTUIVAT!")
        print("\nVoit nyt ajaa pelin komennolla:")
        print("python3 main.py")
    else:
        print("Jotkut testit epäonnistuivat")
        print("Tarkista virheet ja korjaa ne ennen jatkamista")
    
    return success

if __name__ == "__main__":
    run_all_tests()