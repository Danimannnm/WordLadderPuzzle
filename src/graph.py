# src/graph.py

import networkx as nx
import random

def load_dictionary(file_path):
    """
    Loads a dictionary file where each word is on a new line.
    Returns a list of words.
    """
    with open(file_path, 'r') as file:
        # Remove any extra spaces and ignore empty lines.
        words = [line.strip().lower() for line in file if line.strip()]
    return words

def differ_by_one(word1, word2):
    """
    Check if two words differ by exactly one letter.
    Both words must be of the same length.
    """
    if len(word1) != len(word2):
        return False
    # Count how many letters differ between the two words.
    count_diff = sum(1 for a, b in zip(word1, word2) if a != b)
    return count_diff == 1

def build_graph(words):
    """
    Build a graph where nodes are words and an edge exists between two words
    if they differ by exactly one letter.
    """
    G = nx.Graph()
    G.add_nodes_from(words)
    
    word_count = len(words)
    for i in range(word_count):
        for j in range(i + 1, word_count):
            if differ_by_one(words[i], words[j]):
                G.add_edge(words[i], words[j])
    return G

def filter_words_by_difficulty(words, difficulty):
    """
    Filter words based on difficulty.
    
    Difficulty levels:
    - Easy: words of length 3-4
    - Medium: words of length 5-6
    - Hard: words of length 7-9
    
    Returns a list of words that match the allowed lengths.
    """
    if difficulty.lower() == 'easy':
        allowed_lengths = {3}
    elif difficulty.lower() == 'medium':
        allowed_lengths = {4}
    elif difficulty.lower() == 'hard':
        allowed_lengths = {6}
    else:
        raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'")
    
    filtered = [word for word in words if len(word) in allowed_lengths]
    return filtered

def select_start_end_words(words, difficulty):
    """
    Choose a random start word based on the chosen difficulty.
    Then choose another random end word of the same length.
    
    Returns a tuple:
        (start_word, end_word, same_length_words)
    where same_length_words is the list of words having the same length as start_word.
    """
    # First, filter the dictionary based on the difficulty level.
    filtered = filter_words_by_difficulty(words, difficulty)
    if not filtered:
        raise ValueError("No words available for the chosen difficulty.")
    
    # Choose a random start word from the filtered list.
    start_word = random.choice(filtered)
    
    # Filter to get only words with the same length as the start word.
    same_length_words = [word for word in filtered if len(word) == len(start_word)]
    if len(same_length_words) < 2:
        raise ValueError("Not enough words of the same length to form a ladder.")
    
    # Choose a random end word ensuring it's different from the start word.
    end_word = start_word
    while end_word == start_word:
        end_word = random.choice(same_length_words)
    
    return start_word, end_word, same_length_words

if __name__ == "__main__":
    # Load the dictionary from the file.
    words = load_dictionary("data/oxford_words.txt")
    
    # Choose the difficulty level (change this value as desired).
    difficulty = "easy"  # Options: "easy", "medium", "hard"
    
    # Select the start and end words based on the difficulty.
    start_word, end_word, same_length_words = select_start_end_words(words, difficulty)
    print("Start word:", start_word)
    print("End word:", end_word)
    
    # Build a graph using only words of the same length as the chosen start word.
    graph = build_graph(same_length_words)
    print("Graph built with {} nodes and {} edges".format(graph.number_of_nodes(), graph.number_of_edges()))
