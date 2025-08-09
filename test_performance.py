import time
import random
import statistics
from src.markov import MarkovAI

class PerformanceTests:
    
    def __init__(self):
        self.results = {}
    
    def test_history_update_performance(self):
        """Testaa historian päivityksen suorituskyky"""
        print("Testataan historian päivityksen suorituskyky...")
        
        ai = MarkovAI(max_depth=5)
        moves = ["kivi", "paperi", "sakset"]
        
        # Testaa eri historian pituuksilla
        test_sizes = [100, 500, 1000, 5000]
        
        for size in test_sizes:
            times = []
            
            for _ in range(10):
                test_ai = MarkovAI(max_depth=5)
                
                # Esilataa historia
                for i in range(size - 1):
                    test_ai.update_history(random.choice(moves))
                
                # Mittaa viimeisen päivityksen aika
                start_time = time.perf_counter()
                test_ai.update_history(random.choice(moves))
                end_time = time.perf_counter()
                
                times.append(end_time - start_time)
            
            avg_time = statistics.mean(times)
            max_time = max(times)
            
            print(f"  Historia {size} siirtoa: keskiarvo {avg_time*1000:.3f}ms, maksimi {max_time*1000:.3f}ms")
            
            assert avg_time < 0.001, f"Historia päivitys liian hidas: {avg_time*1000:.3f}ms"
        
        print("✓ Historian päivitys suorituskyky OK")
    
    def test_prediction_performance(self):
        """Testaa ennustuksen suorituskyky"""
        print("Testataan ennustuksen suorituskyky...")
        
        # Luo AI jossa on paljon dataa
        ai = MarkovAI(max_depth=5)
        moves = ["kivi", "paperi", "sakset"]
        
        # Täytä historia 10000 siirroilla
        for _ in range(10000):
            ai.update_history(random.choice(moves))
        
        # Mittaa ennustuksen nopeus
        times = []
        for _ in range(100):
            start_time = time.perf_counter()
            predictions = ai.predict_next()
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        print(f" Ennustus (10k historia): keskiarvo {avg_time*1000:.3f}ms, maksimi {max_time*1000:.3f}ms")
        
        assert avg_time < 0.005, f"Ennustus liian hidas: {avg_time*1000:.3f}ms"
        
        print("Ennustuksen suorituskyky OK")
    
    def test_memory_usage(self):
        """Testaa muistin käyttö"""
        print("Testataan muistin käyttöä...")
        
        ai = MarkovAI(max_depth=5)
        moves = ["kivi", "paperi", "sakset"]
        
        for i in range(50000):
            ai.update_history(random.choice(moves))
            
            if i > 1000 and len(ai.history) > 10000:
                print(f"  Varoitus: Historia kasvaa liian suureksi: {len(ai.history)} siirtoa")
        
        #Siirtymätaulujen koko
        total_transitions = 0
        for depth in ai.transition_counts:
            for sequence in ai.transition_counts[depth]:
                for move in ai.transition_counts[depth][sequence]:
                    total_transitions += ai.transition_counts[depth][sequence][move]
        
        print(f"  Historia pituus: {len(ai.history)}")
        print(f"  Siirtymiä yhteensä: {total_transitions}")
        print(f"  Siirtymätauluja: {sum(len(ai.transition_counts[d]) for d in ai.transition_counts)}")
        
        # Suorituskykyvaatimus: kohtuullinen muistin käyttö
        assert len(ai.history) < 100000, f"Historia liian pitkä: {len(ai.history)}"
        
        print("Muistin käyttö OK")
    
    def test_game_simulation_performance(self):
        print("Testataan kokonaisen pelin suorituskykyä...")
        
        ai = MarkovAI(max_depth=5)
        moves = ["kivi", "paperi", "sakset"]
        
        start_time = time.perf_counter()
        
        for round_num in range(1000):
            # Pelaajan siirto (satunnainen)
            player_move = random.choice(moves)
            
            # AI:n siirto
            ai_move = ai.counter_move()
            
            # Päivitä tilastot
            ai.update_win_stats(player_move, ai_move)
            ai.update_history(player_move)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        time_per_round = total_time / 1000
        
        print(f"  1000 kierrosta: {total_time:.3f}s yhteensä")
        print(f"  Aikaa per kierros: {time_per_round*1000:.3f}ms")
        
        assert time_per_round < 0.01, f"Peli liian hidas: {time_per_round*1000:.3f}ms per kierros"
        
        print("Pelin suorituskyky OK")
    
    def test_scalability(self):
        """Testaa skaalautuvuus eri syvyyksillä"""
        print("Testataan skaalautuvuutta...")
        
        max_depths = [1, 2, 3, 5, 8]
        moves = ["kivi", "paperi", "sakset"]
        
        for depth in max_depths:
            ai = MarkovAI(max_depth=depth)
            
            # Täytä historia
            for _ in range(1000):
                ai.update_history(random.choice(moves))
            
            # Mittaa suorituskyky
            times = []
            for _ in range(50):
                start_time = time.perf_counter()
                ai.counter_move()
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            avg_time = statistics.mean(times)
            print(f" Syvyys {depth}: {avg_time*1000:.3f}ms keskimäärin")
            
            max_allowed_time = 0.002 * depth 
            assert avg_time < max_allowed_time, f"Syvyys {depth} liian hidas: {avg_time*1000:.3f}ms"
        
        print("Skaalautuvuus OK")


class AccuracyTests:   
    def test_pattern_learning_accuracy(self):
        print("Testataan kuvioiden oppimista...")
        
        ai = MarkovAI(max_depth=3)
        pattern = ["kivi", "paperi", "sakset"] * 20  # 60 siirtoa
        
        for move in pattern:
            ai.update_history(move)
        
        correct_predictions = 0
        total_predictions = 0
        
        test_sequences = [
            (["kivi"], "paperi"),
            (["paperi"], "sakset"), 
            (["sakset"], "kivi"),
            (["paperi", "sakset"], "kivi"),
            (["sakset", "kivi"], "paperi"),
            (["kivi", "paperi"], "sakset")
        ]
        
        for sequence, expected in test_sequences:
            ai.history = ai.history[:-len(sequence)] + sequence
            
            predictions = ai.predict_next()
            
            for depth in predictions:
                if predictions[depth] == expected:
                    correct_predictions += 1
                total_predictions += 1
                break  #Vaan paras ennuste
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        print(f"  Deterministisen kuvion tarkkuus: {accuracy:.1%} ({correct_predictions}/{total_predictions})")
        
        assert accuracy >= 0.8, f"AI:n tarkkuus liian matala deterministiselle kuviolle: {accuracy:.1%}"
        
        print("Kuvioiden oppiminen OK")
    
    def test_random_performance(self):
        print("Testataan suoritusta satunnaista vastustajaa vastaan...")
        
        ai = MarkovAI(max_depth=3)
        moves = ["kivi", "paperi", "sakset"]
        
        ai_wins = 0
        total_games = 1000
        
        for _ in range(total_games):
            player_move = random.choice(moves)
            
            ai_move = ai.counter_move()
            
            if ai._ai_wins(player_move, ai_move):
                ai_wins += 1            
            ai.update_win_stats(player_move, ai_move)
            ai.update_history(player_move)
        
        win_rate = ai_wins / total_games
        print(f"  AI voitit {ai_wins}/{total_games} peliä ({win_rate:.1%})")

        assert 0.2 <= win_rate <= 0.5, f"AI:n voittoprosentti satunnaista vastaan epäilyttävä: {win_rate:.1%}"
        
        print("Satunnainen vastustaja OK")


def run_performance_tests():
    print("SUORITUSKYKYTESTIT")
    print("=" * 50)
    
    perf_tests = PerformanceTests()
    accuracy_tests = AccuracyTests()
    
    tests = [
        ("Historia päivitys", perf_tests.test_history_update_performance),
        ("Ennustuksen nopeus", perf_tests.test_prediction_performance),
        ("Muistin käyttö", perf_tests.test_memory_usage),
        ("Pelin nopeus", perf_tests.test_game_simulation_performance),
        ("Skaalautuvuus", perf_tests.test_scalability),
        ("Kuvioiden oppiminen", accuracy_tests.test_pattern_learning_accuracy),
        ("Satunnainen vastustaja", accuracy_tests.test_random_performance)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n{test_name}:")
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} epäonnistui: {e}")
            failed += 1
    
    print(f"\n" + "=" * 50)
    print(f"SUORITUSKYKYTESTIEN YHTEENVETO:")
    print(f"Onnistuneet: {passed}")
    print(f"Epäonnistuneet: {failed}")
    print(f"Yhteensä: {passed + failed}")
    
    if failed == 0:
        print("KAIKKI SUORITUSKYKYTESTIT ONNISTUIVAT!")
        return True
    else:
        print("Jotkut suorituskykytestit epäonnistuivat :(")
        return False


class StressTests:    
    def test_memory_leak_detection(self):
        """Testaa muistivuotojen havaitseminen"""
        print("Testataan muistivuotoja...")
        
        ai = MarkovAI(max_depth=5)
        moves = ["kivi", "paperi", "sakset"]
        
        import sys
        initial_size = len(ai.transition_counts[1])
        
        for i in range(10000):
            ai.update_history(random.choice(moves))
            
            if i % 1000 == 0 and i > 0:
                current_size = len(ai.transition_counts[1])
                growth_rate = (current_size - initial_size) / i
                
                if growth_rate > 1.0:  # Enemmän kuin 1 uusi siirtymä per kierros
                    print(f"  Varoitus kierros {i}: Nopea kasvu {growth_rate:.3f}")
        
        final_size = len(ai.transition_counts[1])
        print(f"  Siirtymätaulujen kasvu: {initial_size} → {final_size}")
        
        assert final_size < 1000, f"Siirtymätaulut kasvoivat liikaa: {final_size}"
        
        print("Muistivuototesti OK")
    
    def test_extreme_patterns(self):
        print("Testataan äärimmäisiä kuvioita...")
        
        ai = MarkovAI(max_depth=5)
        
        deterministic = ["kivi"] * 1000
        start_time = time.perf_counter()
        
        for move in deterministic:
            ai.update_history(move)
        
        det_time = time.perf_counter() - start_time
        print(f"  Deterministinen (1000 kiveä): {det_time:.3f}s")
        
        ai2 = MarkovAI(max_depth=5)
        random_moves = [random.choice(["kivi", "paperi", "sakset"]) for _ in range(1000)]
        
        start_time = time.perf_counter()
        for move in random_moves:
            ai2.update_history(move)
        
        random_time = time.perf_counter() - start_time
        print(f"  Satunnainen (1000 siirtoa): {random_time:.3f}s")
        
        # Testi 3: Monimutkainen kuvio
        ai3 = MarkovAI(max_depth=5)
        complex_pattern = []
        for i in range(1000):
            if i % 7 == 0:
                complex_pattern.append("kivi")
            elif i % 5 == 0:
                complex_pattern.append("paperi")
            else:
                complex_pattern.append("sakset")
        
        start_time = time.perf_counter()
        for move in complex_pattern:
            ai3.update_history(move)
        
        complex_time = time.perf_counter() - start_time
        print(f"  Monimutkainen kuvio: {complex_time:.3f}s")
        
        assert det_time < 1.0, f"Deterministinen liian hidas: {det_time:.3f}s"
        assert random_time < 1.0, f"Satunnainen liian hidas: {random_time:.3f}s"  
        assert complex_time < 1.0, f"Monimutkainen liian hidas: {complex_time:.3f}s"
        
        print("✓ Äärimmäiset kuviot OK")


def run_all_performance_tests():
    print("SUORITUSKYKY- JA RASITUSTESTIT")
    print("=" * 60)
    
    basic_success = run_performance_tests()
    
    if basic_success:
        print(f"\n" + "=" * 60)
        print("RASITUSTESTIT")
        print("=" * 60)
        
        stress_tests = StressTests()
        stress_methods = ['test_memory_leak_detection', 'test_extreme_patterns']
        
        stress_passed = 0
        
        for method_name in stress_methods:
            try:
                print(f"\n{method_name.replace('_', ' ').title()}:")
                getattr(stress_tests, method_name)()
                stress_passed += 1
            except Exception as e:
                print(f"✗ {method_name}: {e}")
        
        print(f"\n" + "=" * 60)
        print(f"RASITUSTESTIEN YHTEENVETO:")
        print(f"Onnistuneet: {stress_passed}/{len(stress_methods)}")
        
        if stress_passed == len(stress_methods):
            print("KAIKKI RASITUSTESTIT ONNISTUIVAT!")
            return True
        else:
            print("Jotkut rasitustestit epäonnistuivat :(")
            return False
    else:
        print("\nOhitetaan rasitustestit perussuorituskykytestien epäonnistumisen takia")
        return False


if __name__ == "__main__":
    run_all_performance_tests()