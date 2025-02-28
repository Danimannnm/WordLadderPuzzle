# src/main.py

import sys
from graph import load_dictionary
from utils import select_valid_word_pair
from algorithms import search_path
import networkx as nx

def main():
    # Load the dictionary from file.
    dictionary_file = "data/oxford_words.txt"
    words = load_dictionary(dictionary_file)
    
    # Ask user for a difficulty level.
    difficulty = input("Enter difficulty level (easy, medium, hard): ").strip().lower()
    
    try:
        # Use the helper to select a valid word pair and build the graph.
        start_word, end_word, same_length_words, graph = select_valid_word_pair(words, difficulty)
    except ValueError as e:
        print("Error:", e)
        sys.exit(1)
    
    print(f"Start word: {start_word}")
    print(f"End word: {end_word}")
    print("Graph built with {} nodes and {} edges".format(
        graph.number_of_nodes(), graph.number_of_edges()))
    
    # Ask the user which search algorithm they want to use.
    algorithm = input("Choose search algorithm (bfs, ucs, astar): ").strip().lower()
    
    # Find the transformation path using the selected algorithm.
    path = search_path(graph, start_word, end_word, algorithm)
    
    if path:
        print("Found path:", " -> ".join(path))
        print(f"Path length: {len(path)} words ({len(path)-1} transformations)")
    else:
        print("Unexpected error: No path found using {}.".format(algorithm))

if __name__ == "__main__":
    main()
