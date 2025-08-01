
from src.markov import MarkovAI

def determine_winner(player, ai):
    if player == ai:
        return "Tasapeli!"
    elif (player == "kivi" and ai == "sakset") or \
         (player == "sakset" and ai == "paperi") or \
         (player == "paperi" and ai == "kivi"):
        return "Voitit!"
    else:
        return "Hävisit."

def test_basic_functionality():
    print("Testing basic functionality...")
    ai = MarkovAI(max_depth=3)
    
    assert ai.max_depth == 3
    assert len(ai.history) == 0
    
    # Testaa historian päivitys
    ai.update_history("kivi")
    assert len(ai.history) == 1
    assert ai.history[0] == "kivi"
    
    #Siirron teko 
    move = ai.counter_move()
    assert move in ["kivi", "paperi", "sakset"]
    
    # Tilastojen haku
    stats = ai.get_stats()
    assert len(stats) == 3 
    
    print("PASS: Basic functionality")

def test_hierarchical_learning():
    print("Testing hierarchical learning...")
    ai = MarkovAI(max_depth=3)

    ai.update_history("kivi")
    ai.update_history("paperi") 
    ai.update_history("sakset")
    ai.update_history("kivi")
    
    # Aste 1: sakset --> kivi
    assert ai.transition_counts[1][("sakset",)]["kivi"] == 1
    
    # Aste 2: (paperi, sakset) --> kivi  
    assert ai.transition_counts[2][("paperi", "sakset")]["kivi"] == 1
    
    # Aste 3: (kivi, paperi, sakset) --> kivi
    assert ai.transition_counts[3][("kivi", "paperi", "sakset")]["kivi"] == 1
    
    print("PASS: Hierarchical learning")

def test_win_stats_only_for_available_predictions():
    print("Testing win statistics updates...")
    ai = MarkovAI(max_depth=3)
    
    ai.update_win_stats("kivi", "paperi")
    assert ai.win_stats[1]['total'] == 0
    assert ai.win_stats[2]['total'] == 0

    ai.update_history("kivi")
    ai.update_history("paperi")
    
    ai.transition_counts[1][("paperi",)]["sakset"] = 1
    
    ai.update_win_stats("sakset", "kivi")  # AI voittaa
    assert ai.win_stats[1]['total'] == 1
    assert ai.win_stats[1]['wins'] == 1

    assert ai.win_stats[2]['total'] == 0
    assert ai.win_stats[3]['total'] == 0
    
    print("PASS: Win statistics")

def test_ai_wins_logic():
    """Testaa AI:n voittologiikka"""
    print("Testing AI win logic...")
    ai = MarkovAI()
    
    # AI voittaa
    assert ai._ai_wins("kivi", "paperi") == True    # paperi voittaa kiven
    assert ai._ai_wins("paperi", "sakset") == True  # sakset voittaa paperin  
    assert ai._ai_wins("sakset", "kivi") == True    # kivi voittaa sakset
    
    # Pelaaja voittaa
    assert ai._ai_wins("kivi", "sakset") == False   # kivi voittaa sakset
    assert ai._ai_wins("paperi", "kivi") == False   # paperi voittaa kiven
    assert ai._ai_wins("sakset", "paperi") == False # sakset voittaa paperin
    
    # Tasapeli
    assert ai._ai_wins("kivi", "kivi") == False
    assert ai._ai_wins("paperi", "paperi") == False
    assert ai._ai_wins("sakset", "sakset") == False
    
    print("PASS: AI win logic")

def test_simple_learning():
    """Testaa yksinkertaista oppimista"""
    print("Testing simple pattern learning...")
    ai = MarkovAI(max_depth=2)
    
    for _ in range(3):
        ai.update_history("kivi")
        ai.update_history("paperi")
    
    assert len(ai.history) == 6
    
    ai.transition_counts[1][("paperi",)]["kivi"] = 2
    
    predictions = ai.predict_next()
    
    if predictions:
        assert 1 in predictions
        counter = ai.counter_move()
        assert counter == "paperi"  # Vastaliike kiville
    
    print("PASS: Simple learning")

# Suorita kaikki testit
def run_all_tests():
    """Suorita kaikki testit"""
    print("Running MarkovAI tests")
    print("-" * 40)
    
    tests_passed = 0
    tests_total = 5
    
    try:
        test_basic_functionality()
        tests_passed += 1
        
        test_hierarchical_learning()
        tests_passed += 1
        
        test_win_stats_only_for_available_predictions()
        tests_passed += 1
        
        test_ai_wins_logic()
        tests_passed += 1
        
        test_simple_learning()
        tests_passed += 1
        
        print("-" * 40)
        print(f"Tests completed: {tests_passed}/{tests_total} passed")
        print("All tests successful.")
        
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        print(f"Tests completed: {tests_passed}/{tests_total} passed")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print(f"Tests completed: {tests_passed}/{tests_total} passed")
        return False
    
    return True

if __name__ == "__main__":
    run_all_tests()