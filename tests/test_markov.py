from src.markov import MarkovAI
from src.game import determine_winner

def test_update_history_adds_transitions():
    ai = MarkovAI()

    ai.update_history("kivi")      # None → ei tallennu
    ai.update_history("paperi")    # "kivi" → tallentuu: kivi → paperi
    ai.update_history("sakset")    # "paperi" → paperi → sakset

    assert ai.transition_counts["kivi"]["paperi"] == 1
    assert ai.transition_counts["paperi"]["sakset"] == 1
    assert "sakset" not in ai.transition_counts  # sakset → ? ei vielä tallennettu

def test_predict_returns_known_followup():
    ai = MarkovAI()
    ai.prev_move = "kivi"
    ai.transition_counts["kivi"]["paperi"] = 3
    ai.transition_counts["kivi"]["sakset"] = 1

    prediction = ai.predict_next()
    assert prediction == "paperi"

def test_counter_move_is_correct():
    ai = MarkovAI()
    ai.prev_move = "sakset"
    ai.transition_counts["sakset"]["kivi"] = 5  # AI ennustaa "kivi" → pelaa "paperi"

    assert ai.counter_move() == "paperi"

def test_determine_winner_logic():
    assert determine_winner("kivi", "sakset") == "Voitit!"
    assert determine_winner("paperi", "sakset") == "Hävisit."
    assert determine_winner("kivi", "kivi") == "Tasapeli!"