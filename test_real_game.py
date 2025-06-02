# test_real_game.py

# Import necessary classes from your engine files
from board import Board
from game_controller import GameController

def run_real_game_analysis():
    print("\n\n--- Real-life Scenario Analysis: What White should play (Move 18) ---")
    
    # Initialize the GameController
    game_controller = GameController()

    # The FEN for the position after Black's 17...Rxg6. White to move.
    game_fen = "r2qkb1r/pppbpppp/2n5/1B1pN3/3PnB2/4P3/PPP2PPP/RN1QK2R b KQkq - 4 6"

    # Load the board state from the FEN
    game_controller.load_game_from_fen(game_fen)

    # Ask the engine to analyze the top 3 moves for White from this position
    # Using a depth of 4 for initial analysis. You can try higher if you have time.
    game_controller.analyze_current_position(num_lines=3, depth=4)

if __name__ == "__main__":
    run_real_game_analysis()