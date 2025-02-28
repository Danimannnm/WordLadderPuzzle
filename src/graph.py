# src/graph.py

import networkx as nx

def load_dictionary(file_path):
    """
    Loads a dictionary file where each word is on a new line.
    Returns a list of words.
    """
    with open(file_path, 'r') as file:
        # Read each line, remove extra spaces, and ignore empty lines.
        words = [line.strip() for line in file if line.strip()]
    return words

def differ_by_one(word1, word2):
    """
    Check if two words differ by exactly one letter.
    Both words must be of the same length.
    """
    # If the words are not the same length, we cannot compare them.
    if len(word1) != len(word2):
        return False
    # Count the number of letters that are different.
    count_diff = sum(1 for a, b in zip(word1, word2) if a != b)
    return count_diff == 1

def build_graph(words):
    """
    Build a graph where nodes are words and an edge exists between two words
    if they differ by exactly one letter.
    """
    G = nx.Graph()               # Create an empty graph
    G.add_nodes_from(words)      # Add each word as a node
    
    # Compare every pair of words. For each pair, add an edge if they differ by one letter.
    word_count = len(words)
    for i in range(word_count):
        for j in range(i + 1, word_count):
            if differ_by_one(words[i], words[j]):
                G.add_edge(words[i], words[j])
    return G

if __name__ == "__main__":
    # For testing purposes: load the dictionary and build the graph.
    # Make sure you have a file at "data/dictionary.txt" with a list of words.
    words = load_dictionary("data/oxford_words.txt")
    graph = build_graph(words)
    print("Graph built with {} nodes and {} edges".format(graph.number_of_nodes(), graph.number_of_edges()))
