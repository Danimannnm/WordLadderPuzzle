# src/ui.py

import pygame
import sys
from graph import load_dictionary
from utils import select_valid_word_pair
from game import WordLadderGame

# ----- UI Configuration and Color Scheme -----

# Window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# Colors (using neutral tones and high contrast for text)
BG_COLOR      = (245, 245, 245)   # very light grey background
GRID_COLOR    = (220, 220, 220)   # subtle grid lines for a "graph" look
TEXT_COLOR    = (50, 50, 50)      # dark grey for text
INPUT_BG      = (255, 255, 255)   # white input box
BORDER_COLOR  = (200, 200, 200)   # light grey border

# ----- Helper Drawing Functions -----

def draw_background(surface):
    """Fill the background with a neutral color and overlay a grid."""
    surface.fill(BG_COLOR)
    # Draw vertical grid lines
    for x in range(0, WINDOW_WIDTH, 50):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    # Draw horizontal grid lines
    for y in range(0, WINDOW_HEIGHT, 50):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def render_text_center(surface, text, font, color, center):
    """Renders text centered on a given coordinate."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)

# ----- UI Main Loop -----

def ui_loop(game):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Word Ladder Adventure")
    clock = pygame.time.Clock()
    
    # Define fonts
    main_font = pygame.font.SysFont("Arial", 48)
    small_font = pygame.font.SysFont("Arial", 32)
    
    input_text = ""  # User input field
    
    # Define row positions: top, middle, bottom.
    # The current word will always appear in the middle row.
    top_y    = WINDOW_HEIGHT // 3 - 50
    middle_y = WINDOW_HEIGHT // 2
    bottom_y = 2 * WINDOW_HEIGHT // 3 + 50
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Process the input as a guess when Enter is pressed.
                    guess = input_text.strip().lower()
                    input_text = ""
                    if guess != "":
                        if guess not in game.words:
                            print("Invalid word (not in dictionary or wrong length).")
                        else:
                            if game.make_move(guess):
                                # After a valid move, check game status.
                                if game.game_status() == "win":
                                    print("You win!")
                                    running = False
                            else:
                                print("Invalid move. Must change exactly one letter.")
                else:
                    # Only accept alphabetic input
                    if event.unicode.isalpha():
                        input_text += event.unicode
        
        # Draw the background and grid.
        draw_background(screen)
        
        # Determine the words to display:
        # Top row: previous word (or start word if no move has been made yet)
        if len(game.moves_taken) > 1:
            top_word = game.moves_taken[-2]
        else:
            top_word = game.start_word
        # Middle row: if input_text is empty, show the current word (centered).
        current_display = input_text if input_text != "" else game.current_word
        # Bottom row: always show the goal word.
        goal_word = game.goal_word
        
        # Draw the rows centered horizontally.
        render_text_center(screen, top_word, main_font, TEXT_COLOR, (WINDOW_WIDTH//2, top_y))
        
        # Draw the input box for the middle row.
        input_box = pygame.Rect(WINDOW_WIDTH//2 - 200, middle_y - 30, 400, 60)
        pygame.draw.rect(screen, INPUT_BG, input_box)
        pygame.draw.rect(screen, BORDER_COLOR, input_box, 2)
        render_text_center(screen, current_display, main_font, TEXT_COLOR, input_box.center)
        
        render_text_center(screen, goal_word, main_font, TEXT_COLOR, (WINDOW_WIDTH//2, bottom_y))
        
        # Display score and instructions at the top and bottom.
        render_text_center(screen, f"Score: {game.score}", small_font, TEXT_COLOR, (WINDOW_WIDTH//2, 30))
        render_text_center(screen, "Type your guess and press Enter. BACKSPACE to delete.", small_font, TEXT_COLOR, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

# ----- Main Function to Launch the UI -----

def main():
    # Load the dictionary and select a valid word pair.
    dictionary_file = "data/oxford_words.txt"  # Adjust path as needed.
    words = load_dictionary(dictionary_file)
    difficulty = input("Enter difficulty level (easy, medium, hard): ").strip().lower()
    try:
        start_word, goal_word, same_length_words, graph = select_valid_word_pair(words, difficulty)
    except ValueError as e:
        print("Error:", e)
        sys.exit(1)
    
    print(f"\nValid word pair selected:\nStart word: {start_word}\nGoal word: {goal_word}")
    print(f"Graph built with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    
    # Initialize the game instance.
    game = WordLadderGame(start_word, goal_word, same_length_words, graph, max_moves=20)
    ui_loop(game)

if __name__ == "__main__":
    main()
