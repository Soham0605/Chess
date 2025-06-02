# Chess
# Simple Python Chess Engine

## Overview

This project is a command-line-based chess engine developed in Python. It's designed as an educational tool to understand the fundamental components of a chess AI, from board representation and move generation to basic evaluation and search algorithms. While not a world-class engine, it provides a solid foundation for exploring chess programming.

## Features

* **FEN Support:** Load and display board positions using Forsyth-Edwards Notation (FEN).
* **Legal Move Generation:** Accurately generates all legal moves for any given position, adhering to standard chess rules including:
    * Pawn pushes (single/double) and captures.
    * En passant captures.
    * Pawn promotion (to Queen, Rook, Bishop, Knight).
    * Castling (Kingside and Queenside), with checks for king safety (not moving through or into check, castling rights).
    * Standard moves for Knights, Bishops, Rooks, and Queens.
* **Game State Detection:**
    * Checks for King being in check.
    * Detects checkmate.
    * Detects stalemate.
    * Basic draw detection (50-move rule).
* **Basic Evaluation Function:** Assigns a numerical score to board positions based on:
    * Material balance (standard piece values).
    * Simple piece-square tables (basic positional scoring).
* **Alpha-Beta Pruning Search:** Implements the Minimax algorithm with Alpha-Beta Pruning to efficiently search the game tree and find the "best" move.
* **Engine Analysis:** Can analyze any given FEN position and suggest the top N moves with their calculated scores.
* **Interactive Play:** Includes a basic text-based interface to play against the engine.

## How It Works (High-Level)

The engine is structured into several interconnected Python classes:

* `Piece`: Represents individual chess pieces with their type, color, and value.
* `Move`: Encapsulates a chess move, storing origin, destination, and special flags (capture, castling, promotion, en passant).
* `Board`: The core game state manager. It handles piece placement, FEN parsing, move application (`make_move`), and all aspects of legal move generation (`generate_legal_moves`). It also determines if the King is in check, checkmate, or stalemate.
* `Evaluation`: Contains the chess "knowledge" of the engine, assigning a numerical score to a `Board` object based on material and positional factors.
* `Search`: Implements the Alpha-Beta Pruning algorithm. It uses the `Evaluation` function to score potential game states and finds the move that maximizes its own score while minimizing the opponent's score.
* `GameController`: Orchestrates the interactions between the `Board`, `Evaluation`, and `Search` components. It handles loading game states, running analyses, and managing interactive play.

## Getting Started

### Prerequisites

* Python 3.x (recommended 3.8+)
* Git (for cloning the repository)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```
    (Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub details.)

### Running the Engine

All functionalities can be tested or run via the `main.py` script.

1.  **Run All Automated Tests:**
    The `main.py` file contains a series of test scenarios that validate the core functionalities like move generation, check/mate/stalemate detection, and basic engine analysis.

    ```bash
    python main.py
    ```
    The output will show detailed results for each test, including debug prints for check detection if enabled in `board.py`.

2.  **Analyze a Specific Chess Position (FEN):**
    You can use the `test_real_game.py` script to analyze a custom position.

    ```bash
    python test_real_game.py
    ```
    To analyze a different FEN, open `test_real_game.py` and modify the `game_fen` variable.

3.  **Play an Interactive Game against the Engine:**
    To play against the engine, uncomment the `game_controller.play_game()` lines at the end of `main.py` (or add a new call to `game_controller.play_game()` in `test_real_game.py`).

    ```python
    # Example in main.py or test_real_game.py
    game_controller = GameController()
    game_controller.play_game(engine_color='black', depth=3) # Engine plays as Black at depth 3
    # OR
    # game_controller.play_game(engine_color='white', depth=3) # Engine plays as White at depth 3
    ```
    Run the script after uncommenting.

    ```bash
    python main.py # or python test_real_game.py
    ```
    Follow the prompts in the terminal to enter your moves in UCI format (e.g., `e2e4`, `g1f3`).

## Project Structure
This repository is for making a chess engine.
