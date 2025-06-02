# search.py
import math

class Search:
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.nodes_searched = 0
        self.max_depth = 0

    def find_best_move(self, board, depth):
        """
        Initiates the Alpha-Beta search to find the best move.
        Returns the best Move object and its associated score.
        """
        self.nodes_searched = 0 # Reset node count for each new search
        self.max_depth = depth # Store the initial search depth

        best_move = None
        
        # Determine initial alpha and beta bounds
        alpha = float('-inf')
        beta = float('inf')

        # Get all legal moves for the current board state
        legal_moves = board.generate_legal_moves()
        
        # Basic move ordering: try captures first (simple heuristic)
        # More advanced engines use history heuristics, killer moves, MVV-LVA, etc.
        legal_moves.sort(key=lambda move: move.is_capture, reverse=True)

        if board.turn == 'white':
            best_score = float('-inf')
            for move in legal_moves:
                temp_board = board._copy()
                temp_board.make_move(move) # Make the move on the temporary board

                # Call alpha_beta for the opponent's turn (minimizing player)
                score = self.alpha_beta(temp_board, depth - 1, alpha, beta, False) # False = is_maximizing_player (for next turn)

                if score > best_score:
                    best_score = score
                    best_move = move
                
                alpha = max(alpha, best_score) # Update alpha
                if beta <= alpha:
                    break # Alpha-beta cutoff (beta represents opponent's best score)
        else: # Black's turn (minimizing player)
            best_score = float('inf')
            for move in legal_moves:
                temp_board = board._copy()
                temp_board.make_move(move) # Make the move on the temporary board

                # Call alpha_beta for our turn (maximizing player for next turn)
                score = self.alpha_beta(temp_board, depth - 1, alpha, beta, True) # True = is_maximizing_player (for next turn)

                if score < best_score:
                    best_score = score
                    best_move = move
                
                beta = min(beta, best_score) # Update beta
                if beta <= alpha:
                    break # Alpha-beta cutoff (alpha represents our best score)
        
        return best_move, best_score

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing_player):
        """
        The Alpha-Beta Pruning search algorithm.
        board: The current board state.
        depth: Current search depth (decrements with each recursive call).
        alpha: Best score found so far for the maximizing player.
        beta: Best score found so far for the minimizing player.
        is_maximizing_player: True if it's the maximizing player's turn (White), False for minimizing (Black).
        """
        self.nodes_searched += 1

        # Base case: if depth is 0 or game is over (checkmate/stalemate)
        if depth == 0:
            return self.evaluator.evaluate(board) # Evaluate the leaf node

        # Check for terminal nodes (checkmate or stalemate)
        # Note: If it's checkmate, the score should be very high/low to indicate win/loss.
        # This is typically handled by the evaluation function if it detects mate.
        # Our `is_checkmate` and `is_stalemate` are called in `evaluate` when game ends.
        
        # If no legal moves, it's either checkmate or stalemate
        legal_moves = board.generate_legal_moves()
        if not legal_moves:
            if board.is_checkmate():
                # Score depends on who is checkmated. If White is checkmated, Black wins (negative score).
                # If Black is checkmated, White wins (positive score).
                # Score should reflect a winning/losing position from White's perspective.
                # A very large (positive or negative) score indicates a decisive outcome.
                if board.turn == 'white': # White is checkmated, Black wins
                    return float('-inf') + (self.max_depth - depth) # Smaller value for quicker mate
                else: # Black is checkmated, White wins
                    return float('inf') - (self.max_depth - depth) # Larger value for quicker mate
            elif board.is_stalemate() or board.is_draw():
                return 0 # Stalemate is a draw

        # Sort moves for better pruning (captures first, then other heuristics if added)
        # This is important for alpha-beta efficiency.
        legal_moves.sort(key=lambda move: move.is_capture, reverse=True)


        if is_maximizing_player: # Maximizing player (White)
            max_eval = float('-inf')
            for move in legal_moves:
                temp_board = board._copy()
                temp_board.make_move(move)
                eval = self.alpha_beta(temp_board, depth - 1, alpha, beta, False) # Opponent's turn
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval) # Update alpha
                if beta <= alpha:
                    break # Beta cutoff
            return max_eval
        else: # Minimizing player (Black)
            min_eval = float('inf')
            for move in legal_moves:
                temp_board = board._copy()
                temp_board.make_move(move)
                eval = self.alpha_beta(temp_board, depth - 1, alpha, beta, True) # Our turn
                min_eval = min(min_eval, eval)
                beta = min(beta, eval) # Update beta
                if beta <= alpha:
                    break # Alpha cutoff
            return min_eval