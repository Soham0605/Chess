# game_controller.py
from board import Board
from evaluation import Evaluation
from search import Search
# from pgn_parser import PGNParser # PGNParser is highly complex to do from scratch, keep commented for now if not implemented.

class GameController:
    def __init__(self):
        self.board = Board()
        self.evaluator = Evaluation()
        self.engine = Search(self.evaluator)
        # self.pgn_parser = PGNParser() # Keep commented unless implemented.

    def load_game_from_fen(self, fen_string):
        """Loads a board state from a FEN string."""
        self.board.from_fen(fen_string)
        print(f"Board loaded from FEN: {fen_string}")
        self.board.display()

    # def load_game_from_pgn(self, file_path, game_index=0):
    #     """
    #     Loads a game from a PGN file and sets the board to its final state.
    #     Requires a robust PGNParser and SAN-to-Move conversion.
    #     """
    #     print("PGN parsing is complex and not fully implemented from scratch.")
    #     print("Consider using 'python-chess' library for PGN parsing.")
    #     # Example if you were to use python-chess
    #     # import chess.pgn
    #     # with open(file_path) as pgn_file:
    #     #     game = chess.pgn.read_game(pgn_file) # Reads the first game
    #     #     board_lib = game.board()
    #     #     for move in game.mainline_moves():
    #     #         board_lib.push(move)
    #     #     self.board.from_fen(board_lib.fen()) # Convert python-chess board to your board
    #     return False

    def get_engine_move(self, depth=3):
        """
        Calculates and returns the best move found by the engine.
        """
        print(f"\nEngine thinking for {self.board.turn}'s turn (Depth: {depth})...")
        best_move, best_score = self.engine.find_best_move(self.board, depth)
        print(f"Engine chose: {best_move} (Score: {best_score})")
        print(f"Nodes searched: {self.engine.nodes_searched}")
        return best_move, best_score

    def make_player_move(self, uci_move_str):
        """
        Makes a player's move on the board (if legal).
        uci_move_str: Move in UCI format (e.g., "e2e4", "g1f3").
        """
        legal_moves = self.board.generate_legal_moves()
        found_move = None
        for move in legal_moves:
            if move.to_uci() == uci_move_str:
                found_move = move
                break
        
        if found_move:
            self.board.make_move(found_move)
            print(f"Player made move: {found_move}")
            self.board.display()
            if self.board.is_checkmate():
                print(f"Game Over! {self.board.turn.capitalize()} is in CHECKMATE!")
                return False
            if self.board.is_stalemate():
                print("Game Over! STALEMATE!")
                return False
            if self.board.is_draw():
                print("Game Over! DRAW by 50-move rule (or other rule).")
                return False
            return True
        else:
            print(f"Illegal move: {uci_move_str}. Please enter a legal UCI move.")
            return True # Continue game loop

    def analyze_current_position(self, num_lines=3, depth=5):
        """
        Analyzes the current board position and suggests the top 'num_lines' moves.
        """
        print(f"\nAnalyzing current position for {self.board.turn}'s turn (Depth: {depth})...")
        
        legal_moves = self.board.generate_legal_moves()
        if not legal_moves:
            print("No legal moves available. Position is checkmate or stalemate.")
            return []

        move_scores = []
        # For each legal move, make it, then evaluate the resulting position
        # from the perspective of the *opponent's best response*.
        
        original_turn = self.board.turn
        
        for i, move in enumerate(legal_moves):
            # print(f"Evaluating line for move {i+1}/{len(legal_moves)}: {move.to_uci()}")
            temp_board = self.board._copy()
            temp_board.make_move(move) # Make the initial move
            
            # Evaluate the resulting position.
            # The search function should find the best move for the *current* turn on temp_board
            # which is now the opponent's turn.
            
            # Use a slightly shallower depth for evaluation during line analysis to save time.
            # The score we get back is the value of the position *after* this move,
            # assuming optimal play from the opponent.
            
            # The is_maximizing_player parameter for alpha_beta should be based on `temp_board.turn`
            # which is now the opponent's turn.
            
            score_after_move = self.engine.alpha_beta(
                temp_board, depth - 1, float('-inf'), float('inf'), temp_board.turn == 'white'
            )
            
            move_scores.append({'move': move, 'score': score_after_move})

        # Sort by score. If White's turn, higher score is better. If Black's turn, lower score is better.
        if original_turn == 'white': # White wants to maximize score
            move_scores.sort(key=lambda x: x['score'], reverse=True)
        else: # Black wants to minimize score
            move_scores.sort(key=lambda x: x['score'], reverse=False)

        print(f"Nodes searched during analysis: {self.engine.nodes_searched}")
        
        top_lines = []
        print("\n--- Top Suggested Moves ---")
        for i in range(min(num_lines, len(move_scores))):
            best_move_info = move_scores[i]
            # For a full "line", you would recursively call search to trace the principal variation
            # (the sequence of best moves) from this position. For now, just the first move.
            print(f"Line {i+1}: {best_move_info['move'].to_uci()} (Score: {best_move_info['score']})")
            top_lines.append(best_move_info) 
            
        return top_lines

    def play_game(self, engine_color='black', depth=3):
        """
        Starts an interactive game against the AI.
        engine_color: 'white' or 'black' for the AI.
        """
        print("\n--- Starting New Game ---")
        self.board.setup_initial_position()
        self.board.display()

        while True:
            if self.board.turn == engine_color:
                print(f"\n{engine_color.capitalize()}'s turn (Engine).")
                best_move, _ = self.get_engine_move(depth)
                self.board.make_move(best_move)
                self.board.display()
            else:
                player_color = 'white' if engine_color == 'black' else 'black'
                print(f"\n{player_color.capitalize()}'s turn (You).")
                uci_input = input("Enter your move (e.g., e2e4): ").strip().lower()
                
                if uci_input == 'exit':
                    print("Exiting game.")
                    break
                
                if not self.make_player_move(uci_input):
                    # make_player_move returns True if move was made, False if illegal
                    if self.board.is_checkmate() or self.board.is_stalemate() or self.board.is_draw():
                        break # Game ended
                    continue # Ask for input again if illegal move

            if self.board.is_checkmate() or self.board.is_stalemate() or self.board.is_draw():
                break # Game ended by engine's move

        print("\nGame over!")