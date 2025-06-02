# evaluation.py
class Evaluation:
    def __init__(self):
        # Piece values (material score)
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,  # Bishops are sometimes slightly more valuable than knights
            'rook': 500,
            'queen': 900,
            'king': 20000 # King value is essentially infinite for gameplay, but needs a large number for evaluation
        }
        
        # Positional piece square tables (example - these are very basic, could be improved)
        # These tables add or subtract points based on where a piece is on the board.
        # Ranks are 0-7 (8 to 1), Files are 0-7 (a to h)
        
        # Pawn Table (White's perspective, Black's is mirrored)
        self.pawn_table = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [ 50,  50,  50,  50,  50,  50,  50,  50],
            [ 10,  10,  20,  30,  30,  20,  10,  10],
            [  5,   5,  10,  25,  25,  10,   5,   5],
            [  0,   0,   0,  20,  20,   0,   0,   0],
            [  5,  -5, -10,   0,   0, -10,  -5,   5],
            [  5,  10,  10, -20, -20,  10,  10,   5],
            [  0,   0,   0,   0,   0,   0,   0,   0]
        ]

        # Knight Table
        self.knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   0,   0,   0, -20, -40],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-30,   5,  15,  20,  20,  15,   5, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-40, -20,   0,   5,   5,   0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]

        # Bishop Table
        self.bishop_table = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   5,   5,  10,  10,   5,   5, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,  10,  10,  10,  10,  10,  10, -10],
            [-10,   5,   0,   0,   0,   0,   5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ]

        # Rook Table
        self.rook_table = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [  5,  10,  10,  10,  10,  10,  10,   5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [  0,   0,   0,   5,   5,   0,   0,   0]
        ]

        # Queen Table (Often same as Bishop/Rook tables, or slightly modified)
        self.queen_table = [
            [-20, -10, -10,  -5,  -5, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [ -5,   0,   5,   5,   5,   5,   0,  -5],
            [  0,   0,   5,   5,   5,   5,   0,  -5],
            [-10,   5,   5,   5,   5,   5,   0, -10],
            [-10,   0,   5,   0,   0,   0,   0, -10],
            [-20, -10, -10,  -5,  -5, -10, -10, -20]
        ]

        # King Table (Endgame king table is different)
        self.king_table_mg = [ # Midgame King Table
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [ 20,  20,   0,   0,   0,   0,  20,  20],
            [ 20,  30,  10,   0,   0,  10,  30,  20]
        ]
        
        # A simpler approach to use piece tables: map type to table
        self.piece_tables = {
            'pawn': self.pawn_table,
            'knight': self.knight_table,
            'bishop': self.bishop_table,
            'rook': self.rook_table,
            'queen': self.queen_table,
            'king': self.king_table_mg # Use midgame table for simplicity
        }

    def evaluate(self, board):
        """
        Evaluates the given board position and returns a score.
        A positive score means White has an advantage, negative means Black.
        """
        score = 0

        # Iterate through all squares on the board
        for r in range(8):
            for c in range(8):
                piece = board.get_piece_at(r, c)
                if piece:
                    # Material score
                    material_value = self.piece_values.get(piece.type, 0)
                    
                    # Positional score (using piece square tables)
                    # For white, use table directly. For black, mirror the table vertically.
                    positional_value = 0
                    piece_table = self.piece_tables.get(piece.type)
                    if piece_table:
                        if piece.color == 'white':
                            positional_value = piece_table[r][c]
                        else: # Mirror vertically for black
                            positional_value = piece_table[7 - r][c] # 7-r flips row index

                    # Add or subtract score based on color
                    if piece.color == 'white':
                        score += (material_value + positional_value)
                    else:
                        score -= (material_value + positional_value)
        
        # Add bonus for king safety (e.g., if king is castled, or less exposed)
        # For simplicity, this initial version doesn't include complex king safety checks,
        # but a more advanced engine would check for pawn shields, open files, etc.
        
        # Penalty for being in check (small penalty, mostly handled by pruning illegal moves)
        if board.is_king_in_check(board.turn):
            # This penalty only applies if the *current player* is in check, not if an opponent is checkmated.
            # This helps the search prioritize getting out of check.
            score += (-50 if board.turn == 'white' else 50) 
            # A small penalty to encourage getting out of check. 
            # If it's mate, it's handled by finding no legal moves.

        # Consider draw conditions (50-move rule, stalemate)
        if board.is_draw():
            return 0 # Draw is 0 points

        return score