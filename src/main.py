# src/main.py

import sys
import networkx as nx
from graph import load_dictionary, select_start_end_words, build_graph
from algorithms import search_path

def main():
    # Load the dictionary from file.
    dictionary_file = "data/oxford_words.txt"
    words = load_dictionary(dictionary_file)
    
    # Ask user for a difficulty level.
    difficulty = input("Enter difficulty level (easy, medium, hard): ").strip().lower()
    
    # Keep trying until we find a valid word pair with a path
    valid_path_exists = False
    attempts = 0
    max_attempts = 10  # Prevent infinite loops
    
    while not valid_path_exists and attempts < max_attempts:
        attempts += 1
        try:
            # Select start and end words based on the chosen difficulty.
            start_word, end_word, same_length_words = select_start_end_words(words, difficulty)
        except ValueError as e:
            print("Error:", e)
            sys.exit(1)
        
        print(f"Attempt {attempts}: Testing word pair...")
        print("Start word:", start_word)
        print("End word:", end_word)
        
        # Build the graph using only words of the same length.
        graph = build_graph(same_length_words)
        print("Graph built with {} nodes and {} edges".format(
            graph.number_of_nodes(), graph.number_of_edges()))
        
        # Check if a path exists using networkx's has_path function
        if nx.has_path(graph, start_word, end_word):
            valid_path_exists = True
            print("✓ A path exists between these words!")
        else:
            print("✗ No path exists between these words. Selecting new words...")
    
    if not valid_path_exists:
        print(f"Failed to find a valid word pair after {max_attempts} attempts.")
        sys.exit(1)
    
    # Ask the user which search algorithm they want to use.
    algorithm = input("Choose search algorithm (bfs, ucs, astar): ").strip().lower()
    
    # Find the transformation path using the selected algorithm.
    path = search_path(graph, start_word, end_word, algorithm)
    
    if path:
        print("Found path:", " -> ".join(path))
        print(f"Path length: {len(path)} words ({len(path)-1} transformations)")
    else:
        # This shouldn't happen since we already verified a path exists
        print("Unexpected error: No path found between {} and {} using {}.".format(
            start_word, end_word, algorithm))

if __name__ == "__main__":
    main()