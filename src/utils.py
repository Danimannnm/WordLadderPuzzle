# src/utils.py

import networkx as nx
from graph import select_start_end_words, build_graph

def select_valid_word_pair(words, difficulty, max_attempts=10):
    """
    Attempts to select a valid word pair (start and end words) based on the chosen difficulty,
    ensuring that there exists a valid transformation path between them in the generated graph.

    Parameters:
        words (list): The full dictionary of words.
        difficulty (str): The chosen difficulty level ('easy', 'medium', 'hard').
        max_attempts (int): Maximum number of attempts to find a valid pair.

    Returns:
        tuple: (start_word, end_word, same_length_words, graph) if a valid pair is found.

    Raises:
        ValueError: If no valid pair is found after max_attempts.
    """
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        # Select a random start and end word based on difficulty.
        start_word, end_word, same_length_words = select_start_end_words(words, difficulty)
        # Build the graph using only words of the same length.
        graph = build_graph(same_length_words)
        print(f"Attempt {attempts}: Testing word pair {start_word} -> {end_word}")
        
        # Verify if a transformation path exists between start and end words.
        if nx.has_path(graph, start_word, end_word):
            print("✓ A path exists between these words!")
            return start_word, end_word, same_length_words, graph
        else:
            print("✗ No path exists between these words. Retrying...")

    raise ValueError(f"Failed to find a valid word pair after {max_attempts} attempts.")
