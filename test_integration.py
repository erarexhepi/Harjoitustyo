
import random
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.markov import MarkovAI
from src.game import VisualGame, GameStats

class TestGameStats:
    
    def test_stats_tracking(self):
        stats = GameStats()        
        assert stats.total_games == 0
        assert stats.get_win_percentage() == 0.0
        
        test_results = [
            ("player", "kivi", "sakset"),  # Pelaaja voittaa
            ("ai", "paperi", "kivi"),      # AI voittaa
            ("tie", "kivi", "kivi"),       # Tasapeli
            ("player", "sakset", "paperi"), # Pelaaja voittaa
            ("ai", "kivi", "paperi")       # AI voittaa
        ]
        
        for result, player_move, ai_move in test_results:
            stats.add_result(result, player_move, ai_move)
        
        assert stats.total_games == 5
        assert stats.player_wins == 2
        assert stats.ai_wins == 2
        assert stats.ties == 1
        assert stats.get_win_percentage() == 40.0  # 2/5 = 40%
        
        assert len(stats.game_history) == 5
        assert stats.game_history[0]['round'] == 1
        assert stats.game_history[-1]['round'] == 5
        
        print("GameStats integraatio OK")

class TestVisualGameIntegration:
    
    def test_game_initialization(self):
        game = VisualGame()
        
        assert isinstance(game.ai, MarkovAI)
        assert isinstance(game.stats, GameStats)
        assert game.ai.max_depth == 5
        assert len(game.VALID_MOVES) == 3
        
        print("Pelin alustus OK")
    
    def test_winner_determination(self):
        game = VisualGame()
        
        test_cases = [
            # Pelaaja voittaa
            ("kivi", "sakset", "player"),
            ("paperi", "kivi", "player"), 
            ("sakset", "paperi", "player"),
            # AI voittaa
            ("sakset", "kivi", "ai"),
            ("kivi", "paperi", "ai"),
            ("paperi", "sakset", "ai"),
            # Tasapelit
            ("kivi", "kivi", "tie"),
            ("paperi", "paperi", "tie"),
            ("sakset", "sakset", "tie")
        ]
        
        for player_move, ai_move, expected_result in test_cases:
            result, message = game.determine_winner(player_move, ai_move)
            assert result == expected_result, f"Väärä tulos: {player_move} vs {ai_move}, odotettiin {expected_result}, saatiin {result}"
        
        print("Voittajan määritys OK")
    
    def test_complete_round_simulation(self):
        """Testaa kokonaisen kierroksen simulaatio"""
        game = VisualGame()
        
        with patch.object(game, 'get_player_move', return_value='kivi'):
            with patch('builtins.print'):
                success = game.play_round()
        
        assert success == True
        assert game.stats.total_games == 1
        assert len(game.ai.history) == 1
        assert game.ai.history[0] == 'kivi'
        
        print("Kierroksen simulaatio OK")


class TestAIGameInteraction:
    
    def test_ai_learning_during_game(self):
        ai = MarkovAI(max_depth=3)
        
        pattern = ["kivi", "paperi", "sakset"] * 10
        ai_moves = []
        
        for player_move in pattern:
            ai_move = ai.counter_move()
            ai_moves.append(ai_move)
            
            ai.update_win_stats(player_move, ai_move)
            ai.update_history(player_move)
        
        stats = ai.get_stats()
        learned = any(stat['total'] > 0 for stat in stats.values())
        assert learned, "AI:n pitäisi oppia jotain kuvion aikana"
        
        found_pattern = False
        for depth in ai.transition_counts:
            for sequence in ai.transition_counts[depth]:
                if ai.transition_counts[depth][sequence]:
                    found_pattern = True
                    break
            if found_pattern:
                break
        
        assert found_pattern, "AI:n pitäisi tallentaa siirtymäkuvioita"
        
        print("AI:n oppiminen pelin aikana OK")
    
    def test_model_switching_during_game(self):
        ai = MarkovAI(max_depth=3)        
        ai.win_stats[1] = {'wins': 6, 'total': 10}  # 60%
        ai.win_stats[2] = {'wins': 8, 'total': 10}  # 80%
        ai.win_stats[3] = {'wins': 4, 'total': 10}  # 40%
        
        ai.history = ["kivi", "paperi", "sakset", "kivi"]
        for depth in [1, 2, 3]:
            seq_len = min(depth, len(ai.history))
            sequence = tuple(ai.history[-seq_len:])
            ai.transition_counts[depth][sequence]["paperi"] = 1
        
        used_models = []
        
        for round_num in range(12):
            model_before = ai.get_current_model_info()['current_model']
            
            ai_move = ai.counter_move()
            ai.update_win_stats("kivi", ai_move)
            ai.update_history("kivi")
            
            model_after = ai.get_current_model_info()['current_model']
            used_models.append(model_after)
        
        first_5_models = used_models[:5]
        second_5_models = used_models[5:10]
        
        assert len(set(first_5_models)) == 1, f"Ensimmäisellä 5-kierroksen jaksolla pitäisi olla sama malli: {first_5_models}"
        
        assert len(set(second_5_models)) == 1, f"Toisella 5-kierroksen jaksolla pitäisi olla sama malli: {second_5_models}"
        
        print("Mallien vaihtuminen OK")


class TestErrorHandling:
    
    def test_invalid_moves_handling(self):
        ai = MarkovAI()
        
        for _ in range(100):
            move = ai.counter_move()
            assert move in ["kivi", "paperi", "sakset"], f"AI teki virheellisen siirron: {move}"
        
        print("Virheellisten siirtojen käsittely OK")
    
    def test_empty_history_handling(self):
        ai = MarkovAI()
        
        move = ai.counter_move()
        assert move in ["kivi", "paperi", "sakset"]
        
        stats = ai.get_stats()
        for stat in stats.values():
            assert stat['total'] == 0
            assert stat['win_rate'] == 0
        
        print("Tyhjän historian käsittely OK")
    
    def test_extreme_values(self):
        ai_deep = MarkovAI(max_depth=20)
        assert ai_deep.max_depth == 20
        
        ai_shallow = MarkovAI(max_depth=1)
        assert ai_shallow.max_depth == 1
        
        move_deep = ai_deep.counter_move()
        move_shallow = ai_shallow.counter_move()
        
        assert move_deep in ["kivi", "paperi", "sakset"]
        assert move_shallow in ["kivi", "paperi", "sakset"]
        
        print("Ääriarvojen käsittely OK")


class TestLongGameSimulation:    
    def test_1000_round_game(self):
        print("Simuloidaan 1000 kierroksen peli...")
        
        ai = MarkovAI(max_depth=5)
        stats = GameStats()
        
        # Eri pelaajatyypit
        strategies = {
            'random': lambda r: random.choice(["kivi", "paperi", "sakset"]),
            'pattern': lambda r: ["kivi", "paperi", "sakset"][r % 3],
            'counter_rock': lambda r: "paperi",  # Vastaa aina kiviä vastaan
            'adaptive': lambda r: random.choice(["kivi", "paperi"]) if r < 500 else "sakset"
        }
        
        for strategy_name, strategy_func in strategies.items():
            print(f"  Testataan strategiaa: {strategy_name}")
            
            test_ai = MarkovAI(max_depth=5)
            test_stats = GameStats()
            
            for round_num in range(250):
                player_move = strategy_func(round_num)
                ai_move = test_ai.counter_move()
                
                if player_move == ai_move:
                    result = "tie"
                elif ((player_move == "kivi" and ai_move == "sakset") or
                      (player_move == "paperi" and ai_move == "kivi") or
                      (player_move == "sakset" and ai_move == "paperi")):
                    result = "player"
                else:
                    result = "ai"
                
                test_stats.add_result(result, player_move, ai_move)
                test_ai.update_win_stats(player_move, ai_move)
                test_ai.update_history(player_move)
            
            ai_win_rate = (test_stats.ai_wins / test_stats.total_games) * 100
            print(f"    AI voittoprosentti: {ai_win_rate:.1f}%")
            print(f"    AI oppimistilastot: {test_ai.get_stats()}")
            
            learned = any(stat['total'] > 0 for stat in test_ai.get_stats().values())
            assert learned, f"AI ei oppinut mitään strategiaa '{strategy_name}' vastaan"
        
        print("Pitkän pelin simulaatio OK")


def run_integration_tests():
    print("INTEGRAATIOTESTIT")
    print("=" * 50)
    
    test_classes = [
        ("GameStats", TestGameStats()),
        ("VisualGame", TestVisualGameIntegration()),
        ("AI-Game vuorovaikutus", TestAIGameInteraction()),
        ("Virhetilanteet", TestErrorHandling()),
        ("Pitkä peli", TestLongGameSimulation())
    ]
    
    passed_classes = 0
    total_classes = len(test_classes)
    
    for class_name, test_instance in test_classes:
        print(f"\n{class_name.upper()}")
        print("-" * 30)
        
        test_methods = [method for method in dir(test_instance) 
                       if method.startswith('test_') and callable(getattr(test_instance, method))]
        
        passed_methods = 0
        
        for method_name in test_methods:
            try:
                method = getattr(test_instance, method_name)
                method()
                passed_methods += 1
            except Exception as e:
                print(f"✗ {method_name}: {e}")
        
        if passed_methods == len(test_methods):
            passed_classes += 1
            print(f"✓ {class_name}: {passed_methods}/{len(test_methods)} testiä onnistui")
        else:
            print(f"✗ {class_name}: {passed_methods}/{len(test_methods)} testiä onnistui")
    
    print(f"\n" + "=" * 50)
    print(f"INTEGRAATIOTESTIEN YHTEENVETO:")
    print(f"Onnistuneet luokat: {passed_classes}/{total_classes}")
    
    if passed_classes == total_classes:
        print("KAIKKI INTEGRAATIOTESTIT ONNISTUIVAT!")
        return True
    else:
        print("Jotkut integraatiotestit epäonnistuivat")
        return False


if __name__ == "__main__":
    run_integration_tests()