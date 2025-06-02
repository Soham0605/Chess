# move.py
class Move:
    def __init__(self, from_sq, to_sq, promotion_piece=None,
                 is_capture=False, is_castling=False, is_en_passant=False,
                 captured_piece=None):
        """
        Initializes a Move object.
        from_sq: (row, col) tuple of the starting square.
        to_sq: (row, col) tuple of the ending square.
        promotion_piece: A single character ('Q', 'R', 'B', 'N') for promotion, or None.
        is_capture: Boolean, True if the move is a capture.
        is_castling: Boolean, True if the move is castling.
        is_en_passant: Boolean, True if the move is an en passant capture.
        captured_piece: The Piece object that was captured (if any).
        """
        self.from_square = from_sq
        self.to_square = to_sq
        self.promotion_piece = promotion_piece
        self.is_capture = is_capture
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.captured_piece = captured_piece

    def __eq__(self, other):
        """Compares two Move objects for equality."""
        if not isinstance(other, Move):
            return NotImplemented
        return (self.from_square == other.from_square and
                self.to_square == other.to_square and
                self.promotion_piece == other.promotion_piece)

    def __hash__(self):
        """Enables Move objects to be used in sets or as dictionary keys."""
        return hash((self.from_square, self.to_square, self.promotion_piece))

    def __repr__(self):
        """Developer-friendly string representation of the move."""
        from_str = f"{chr(ord('a') + self.from_square[1])}{8 - self.from_square[0]}"
        to_str = f"{chr(ord('a') + self.to_square[1])}{8 - self.to_square[0]}"
        promo_str = f"={self.promotion_piece}" if self.promotion_piece else ""
        move_type_flags = []
        if self.is_capture: move_type_flags.append('C')
        if self.is_castling: move_type_flags.append('O')
        if self.is_en_passant: move_type_flags.append('EP')
        flags_str = f" [{','.join(move_type_flags)}]" if move_type_flags else ""
        return f"<Move: {from_str}{to_str}{promo_str}{flags_str}>"

    def to_uci(self):
        """Converts the move to UCI (Universal Chess Interface) format."""
        from_str = f"{chr(ord('a') + self.from_square[1])}{8 - self.from_square[0]}"
        to_str = f"{chr(ord('a') + self.to_square[1])}{8 - self.to_square[0]}"
        promo_str = self.promotion_piece.lower() if self.promotion_piece else ""
        return f"{from_str}{to_str}{promo_str}"

    def __str__(self):
        """User-friendly string representation (defaults to UCI)."""
        return self.to_uci()