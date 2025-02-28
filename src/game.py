# src/game.py

from algorithms import search_path
from utils import select_valid_word_pair

class WordLadderGame:
    def __init__(self, start_word, goal_word, words, graph, max_moves=20):
        """
        Initializes the game state.
        
        Parameters:
            start_word (str): The starting word.
            goal_word (str): The target word.
            words (list): List of valid words (all of the same length).
            graph (networkx.Graph): Graph of valid transformations.
            max_moves (int): Maximum allowed moves.
        """
        self.start_word = start_word
        self.goal_word = goal_word
        self.words = words
        self.graph = graph
        self.current_word = start_word
        self.moves_taken = [start_word]
        self.max_moves = max_moves
        self.score = 0  # initial score
        
        # Compute initial best remaining path length using A* search.
        # Here, we use len(path) - 1 to represent the number of transformations.
        initial_path = search_path(graph, start_word, goal_word, algorithm="astar")
        if initial_path:
            self.prev_remaining = len(initial_path) - 1
        else:
            self.prev_remaining = float('inf')

    def is_valid_move(self, next_word):
        """
        Checks if the next_word is a valid move from the current word.
        A move is valid if the next_word is a neighbor of the current word in the graph.
        """
        return next_word in self.graph[self.current_word]

    def make_move(self, next_word):
        """
        Makes a move if valid. Updates the current word and the move history.
        After the move, calculates the new A* path from the current word to the goal
        and updates the score:
          - +10 points if the new path is shorter than the previous remaining path.
          - -5 points if it is longer (score is not allowed to go below 0).
        Returns True if the move is accepted, False otherwise.
        """
        if self.is_valid_move(next_word):
            self.current_word = next_word
            self.moves_taken.append(next_word)
            
            # Calculate the new remaining path using A* search.
            new_path = search_path(self.graph, self.current_word, self.goal_word, algorithm="astar")
            if new_path:
                new_remaining = len(new_path) - 1  # number of transformations
                if new_remaining < self.prev_remaining:
                    self.score += 10
                    print("Good move! Path improved. +10 points.")
                elif new_remaining > self.prev_remaining:
                    self.score = max(self.score - 5, 0)
                    print("Not optimal move. -5 points.")
                else:
                    print("Move did not change the estimated path length. No points.")
                # Update the previous remaining path length.
                self.prev_remaining = new_remaining
            else:
                print("Warning: No path found from the new word to the goal. (This should not happen)")
            return True
        else:
            return False

    def request_hint(self, algorithm="astar"):
        """
        Provides a hint using the specified search algorithm.
        Returns the next recommended word in the transformation path.
        """
        path = search_path(self.graph, self.current_word, self.goal_word, algorithm)
        if path and len(path) >= 2:
            return path[1]  # Next word after the current word.
        else:
            return None

    def game_status(self):
        """
        Checks the current game status.
        Returns:
            "win" if the goal is reached,
            "lose" if maximum moves are reached,
            "ongoing" otherwise.
        """
        if self.current_word == self.goal_word:
            return "win"
        elif len(self.moves_taken) - 1 >= self.max_moves:
            return "lose"
        else:
            return "ongoing"

    def display_status(self):
        """
        Displays the current game state.
        """
        print(f"\nCurrent word: {self.current_word}")
        print(f"Goal word: {self.goal_word}")
        print(f"Moves taken: {len(self.moves_taken)-1}/{self.max_moves}")
        print("Path so far:", " -> ".join(self.moves_taken))
        print(f"Current score: {self.score}")


def play_game(game):
    """
    Runs the game loop for manual play.
    The player can input a new word or request a hint by typing 'hint'.
    """
    print("Welcome to the Word Ladder Adventure Game!")
    while True:
        game.display_status()
        status = game.game_status()
        if status == "win":
            print("\nCongratulations! You've reached the goal word!")
            break
        elif status == "lose":
            print("\nGame over! You've reached the maximum number of moves.")
            break

        user_input = input("Enter your next word (or type 'hint' for a suggestion): ").strip().lower()
        if user_input == "hint":
            hint = game.request_hint(algorithm="astar")
            if hint:
                print("Hint: Try", hint)
            else:
                print("No hint available at this time.")
        else:
            if user_input not in game.words:
                print("Invalid word. Make sure it exists in the dictionary and matches the required length.")
                continue
            if not game.make_move(user_input):
                print("Invalid move. Ensure you change only one letter from the current word.")
            else:
                print("Move accepted.")


if __name__ == "__main__":
    # Import the load_dictionary function to load the word list.
    from graph import load_dictionary

    # Set the path to your dictionary file.
    dictionary_file = "data/oxford_words.txt"  # Adjust the path as needed.
    words = load_dictionary(dictionary_file)
    
    # Ask the user for a difficulty level.
    difficulty = input("Enter difficulty level (easy, medium, hard): ").strip().lower()
    
    # Use the helper function to select a valid word pair and build the graph.
    try:
        start_word, goal_word, same_length_words, graph = select_valid_word_pair(words, difficulty)
    except ValueError as e:
        print("Error:", e)
        exit(1)
    
    print(f"\nValid word pair selected:")
    print(f"Start word: {start_word}")
    print(f"Goal word: {goal_word}")
    print("Graph built with {} nodes and {} edges".format(graph.number_of_nodes(), graph.number_of_edges()))
    
    # Create a game instance and start the game loop.
    game = WordLadderGame(start_word, goal_word, same_length_words, graph, max_moves=20)
    play_game(game)
