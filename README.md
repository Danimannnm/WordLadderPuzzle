# Word Ladder Adventure – A Game-Based Implementation Using Search Algorithms
## Project Overview

Word Ladder Adventure is a game-based application that challenges players to transform one word into another by changing a single letter at a time. Every intermediate step must be a valid word from a predefined dictionary. The game integrates multiple search algorithms to compute the optimal transformation path, giving players the choice to solve puzzles manually or request AI-powered hints for the best next move.
## Game Concept & Features

- **Puzzle Solving:** Transform a given starting word into a target word, with each step requiring a valid dictionary word.
- **Manual & AI-Assisted Play:** Choose to solve the word ladder manually or get hints from an AI assistant that computes the shortest transformation path.
- **Graph-Based Visualization:** Words are displayed as nodes, and valid transformations are represented as edges connecting them.
- **Scoring System:** Complete the transformation in as few moves as possible—the fewer the moves, the higher your score.
- **Custom Challenges:** Players can choose from predefined challenges or set custom start and target words (provided a valid transformation exists).
## AI Assistance & Search Algorithms

The game features an AI hint system that employs at least three different search algorithms to find the optimal word transformation sequence. The integrated algorithms include:

- **Uniform Cost Search (UCS)**
- **A\* Search Algorithm**
- **Breadth-First Search (BFS)** or **Greedy Best-First Search (GBFS)**

Each algorithm uses:
- **g(n):** The cost function, representing the cumulative effort to reach the current word.
- **h(n):** A heuristic function estimating how many more transformations are needed.
- **f(n):** The combined function where `f(n) = g(n) + h(n)`, used to prioritize the next best move in the sequence.

## Game Modes & Difficulty Levels

Word Ladder Adventure offers multiple game modes to cater to different players:

1. **Beginner Mode:** Simple word ladders with short transformation paths (e.g., changing "cat" to "bat").
2. **Advanced Mode:** More complex puzzles involving longer word ladders that require deeper strategic thinking.
3. **Challenge Mode:** Features additional constraints such as banned words or restricted letters to increase difficulty and add strategic depth.
## Technical Requirements

- **Programming Language:** Python
- **Data Structures:** Utilizes graph-based representations where words are nodes, and valid transformations are edges.
- **Algorithms:** Implements three different search algorithms for finding the shortest path between words.
- **Dictionary Source:** The game uses a predefined dictionary from a text file or an external API to validate words.
## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
    ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
    ```

3. **Prepare the Dictionary:**

If using a local dictionary file, ensure it is placed in the designated folder (e.g., data/dictionary.txt).
Alternatively, configure the external API settings if using an API-based dictionary.

4. **Run the Application:**
   ```
   python main.py
    ```

  ## Usage

- **Manual Play:** Start a new game, choose your starting and target words, then proceed to transform one letter at a time.
- **AI Hint Mode:** Request hints if you're stuck. The game will display the optimal move based on the selected search algorithm.
- **Graph Visualization:** Watch the word network and see how each valid transformation connects in real-time.
- **Scoring:** Your final score is determined by the number of moves taken—the fewer the moves, the better the score!

  ## Contributing

Contributions are welcome! To get started:
1. Fork the repository and create a new branch for your feature or bug fix.
2. Follow the existing code style and file structure.
3. Ensure your changes are well tested.
4. Submit a pull request with a detailed explanation of your changes.

## License

This project is licensed under the MIT License.




