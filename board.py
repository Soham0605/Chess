# board.py
import copy
from piece import Piece
from move import Move

class Board:
    def __init__(self, fen=None):
        self.board_state = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'white'
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.king_position = {'white': None, 'black': None}

        if fen:
            self.from_fen(fen)
        else:
            self.setup_initial_position()

    def setup_initial_position(self):
        initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.from_fen(initial_fen)

    def from_fen(self, fen_string):
        self.board_state = [[None for _ in range(8)] for _ in range(8)]
        self.castling_rights = {'K': False, 'Q': False, 'k': False, 'q': False}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.king_position = {'white': None, 'black': None}

        parts = fen_string.split(' ')
        if len(parts) != 6:
            raise ValueError(f"Invalid FEN string: '{fen_string}'. Expected 6 parts, got {len(parts)}.")

        # 1. Piece Placement
        piece_placement = parts[0]
        row_idx = 0
        col_idx = 0
        for char in piece_placement:
            if char == '/':
                row_idx += 1
                col_idx = 0
            elif char.isdigit():
                col_idx += int(char)
            else:
                color = 'white' if char.isupper() else 'black'
                piece_type_map = {
                    'p': 'pawn', 'n': 'knight', 'b': 'bishop',
                    'r': 'rook', 'q': 'queen', 'k': 'king'
                }
                piece_type = piece_type_map[char.lower()]
                piece = Piece(piece_type, color)
                self.board_state[row_idx][col_idx] = piece

                if piece.type == 'king':
                    self.king_position[color] = (row_idx, col_idx)
                col_idx += 1
        
        if row_idx != 7 or col_idx != 8:
            if row_idx == 7 and col_idx != 8 and parts[0].endswith('/'):
                 pass
            else:
                raise ValueError(f"Invalid FEN piece placement format: {piece_placement}")


        # 2. Active Color
        active_color = parts[1]
        if active_color == 'w':
            self.turn = 'white'
        elif active_color == 'b':
            self.turn = 'black'
        else:
            raise ValueError(f"Invalid active color in FEN: {active_color}. Expected 'w' or 'b'.")

        # 3. Castling Availability
        castling_str = parts[2]
        if castling_str != '-':
            if 'K' in castling_str: self.castling_rights['K'] = True
            if 'Q' in castling_str: self.castling_rights['Q'] = True
            if 'k' in castling_str: self.castling_rights['k'] = True
            if 'q' in castling_str: self.castling_rights['q'] = True

        # 4. En Passant Target Square
        en_passant_str = parts[3]
        if en_passant_str != '-':
            if len(en_passant_str) != 2:
                 raise ValueError(f"Invalid en passant square in FEN: {en_passant_str}")
            col = ord(en_passant_str[0]) - ord('a')
            row = 8 - int(en_passant_str[1])
            if not (0 <= row < 8 and 0 <= col < 8):
                 raise ValueError(f"En passant square out of bounds: {en_passant_str}")
            self.en_passant_target = (row, col)

        # 5. Halfmove Clock
        try:
            self.halfmove_clock = int(parts[4])
        except ValueError:
            raise ValueError(f"Invalid halfmove clock in FEN: {parts[4]}. Expected an integer.")
        if self.halfmove_clock < 0:
            raise ValueError(f"Halfmove clock cannot be negative: {self.halfmove_clock}")

        # 6. Fullmove Number
        try:
            self.fullmove_number = int(parts[5])
        except ValueError:
            raise ValueError(f"Invalid fullmove number in FEN: {parts[5]}. Expected an integer.")
        if self.fullmove_number < 1:
            raise ValueError(f"Fullmove number must be at least 1: {self.fullmove_number}")

    def to_fen(self):
        ranks = []
        for row in self.board_state:
            empty_count = 0
            rank_str = ""
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_str += str(empty_count)
                        empty_count = 0
                    rank_str += str(piece)
            if empty_count > 0:
                rank_str += str(empty_count)
            ranks.append(rank_str)
        
        piece_placement_fen = "/".join(ranks)
        
        active_color_fen = 'w' if self.turn == 'white' else 'b'
        
        castling_fen = ""
        if self.castling_rights['K']: castling_fen += 'K'
        if self.castling_rights['Q']: castling_fen += 'Q'
        if self.castling_rights['k']: castling_fen += 'k'
        if self.castling_rights['q']: castling_fen += 'q'
        if not castling_fen: castling_fen = '-'

        en_passant_fen = '-'
        if self.en_passant_target:
            row, col = self.en_passant_target
            en_passant_fen = f"{chr(ord('a') + col)}{8 - row}"
            
        return f"{piece_placement_fen} {active_color_fen} {castling_fen} {en_passant_fen} {self.halfmove_clock} {self.fullmove_number}"


    def _copy(self):
        new_board = Board(fen=self.to_fen())
        
        if new_board.king_position['white'] is None or new_board.king_position['black'] is None:
            for r in range(8):
                for c in range(8):
                    piece = new_board.board_state[r][c]
                    if piece and piece.type == 'king':
                        new_board.king_position[piece.color] = (r, c)
            
        return new_board

    def get_piece_at(self, r, c):
        if not (0 <= r < 8 and 0 <= c < 8):
            return None
        return self.board_state[r][c]

    def is_square_valid(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def is_square_empty(self, r, c):
        return self.get_piece_at(r, c) is None

    def is_square_attacked(self, r, c, by_color):
        """
        Checks if the square (r, c) is attacked by any piece of 'by_color'.
        """
        print(f"  --> is_square_attacked: Checking if ({r},{c}) attacked by {by_color}")
        
        # --- 1. Pawn attacks ---
        pawn_dir = -1 if by_color == 'white' else 1
        for dc in [-1, 1]:
            target_r, target_c = r + pawn_dir, c + dc
            if self.is_square_valid(target_r, target_c):
                piece = self.get_piece_at(target_r, target_c)
                if piece and piece.type == 'pawn' and piece.color == by_color:
                    print(f"    Pawn attack from ({target_r},{target_c}) {piece}")
                    return True

        # --- 2. Knight attacks ---
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            target_r, target_c = r + dr, c + dc
            if self.is_square_valid(target_r, target_c):
                piece = self.get_piece_at(target_r, target_c)
                if piece and piece.type == 'knight' and piece.color == by_color:
                    print(f"    Knight attack from ({target_r},{target_c}) {piece}")
                    return True

        # --- 3. King attacks ---
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dr, dc in king_moves:
            target_r, target_c = r + dr, c + dc
            if self.is_square_valid(target_r, target_c):
                piece = self.get_piece_at(target_r, target_c)
                if piece and piece.type == 'king' and piece.color == by_color:
                    print(f"    King attack from ({target_r},{target_c}) {piece}")
                    return True

        # --- 4. Sliding Piece attacks (Rook/Queen, Bishop/Queen) ---
        straight_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in straight_directions + diagonal_directions:
            current_r, current_c = r + dr, c + dc
            while self.is_square_valid(current_r, current_c):
                piece = self.get_piece_at(current_r, current_c)
                if piece:
                    if piece.color == by_color:
                        is_straight_attacker = (dr, dc) in straight_directions and (piece.type == 'rook' or piece.type == 'queen')
                        is_diagonal_attacker = (dr, dc) in diagonal_directions and (piece.type == 'bishop' or piece.type == 'queen')
                        if is_straight_attacker or is_diagonal_attacker:
                            # print(f"    Sliding piece attack from ({current_r},{current_c}) {piece} in direction ({dr},{dc})")
                            return True
                    break # A piece, either own or opponent, blocks the line of sight for further attacks in this direction
                current_r += dr
                current_c += dc
        
        print(f"  --> is_square_attacked: ({r},{c}) NOT attacked by {by_color}")
        return False

    def is_king_in_check(self, color):
        king_r, king_c = self.king_position[color]
        opponent_color = 'black' if color == 'white' else 'white'
        print(f"\nChecking if {color}'s King at ({king_r},{king_c}) is in check from {opponent_color}...")
        return self.is_square_attacked(king_r, king_c, opponent_color)

    def generate_pseudo_legal_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.get_piece_at(r, c)
                if piece and piece.color == self.turn:
                    if piece.type == 'pawn':
                        moves.extend(self._get_pawn_pseudo_moves(r, c, piece))
                    elif piece.type == 'knight':
                        moves.extend(self._get_knight_pseudo_moves(r, c, piece))
                    elif piece.type == 'bishop':
                        moves.extend(self._get_bishop_pseudo_moves(r, c, piece))
                    elif piece.type == 'rook':
                        moves.extend(self._get_rook_pseudo_moves(r, c, piece))
                    elif piece.type == 'queen':
                        moves.extend(self._get_queen_pseudo_moves(r, c, piece))
                    elif piece.type == 'king':
                        moves.extend(self._get_king_pseudo_moves(r, c, piece))
        return moves

    def _get_pawn_pseudo_moves(self, r, c, pawn):
        moves = []
        direction = -1 if pawn.color == 'white' else 1
        start_rank = 6 if pawn.color == 'white' else 1
        promotion_rank = 0 if pawn.color == 'white' else 7
        promotion_pieces = ['Q', 'R', 'B', 'N']

        # --- 1. Single Pawn Push ---
        target_r = r + direction
        if self.is_square_valid(target_r, c) and self.is_square_empty(target_r, c):
            if target_r == promotion_rank:
                for promo_p in promotion_pieces:
                    moves.append(Move((r, c), (target_r, c), promotion_piece=promo_p))
            else:
                moves.append(Move((r, c), (target_r, c)))

        # --- 2. Double Pawn Push ---
        if r == start_rank:
            double_target_r = r + 2 * direction
            if self.is_square_valid(target_r, c) and self.is_square_empty(target_r, c) and \
               self.is_square_valid(double_target_r, c) and self.is_square_empty(double_target_r, c):
                moves.append(Move((r, c), (double_target_r, c)))

        # --- 3. Captures ---
        for dc in [-1, 1]:
            target_r, target_c = r + direction, c + dc
            if self.is_square_valid(target_r, target_c):
                target_piece = self.get_piece_at(target_r, target_c)
                if target_piece and target_piece.color != pawn.color:
                    if target_r == promotion_rank:
                        for promo_p in promotion_pieces:
                            moves.append(Move((r, c), (target_r, target_c), promotion_piece=promo_p, is_capture=True, captured_piece=target_piece))
                    else:
                        moves.append(Move((r, c), (target_r, target_c), is_capture=True, captured_piece=target_piece))

        # --- 4. En Passant ---
        if self.en_passant_target:
            ep_r, ep_c = self.en_passant_target
            if ep_r == r + direction and abs(ep_c - c) == 1:
                captured_pawn_row = r
                captured_pawn_col = ep_c
                captured_piece_obj = self.get_piece_at(captured_pawn_row, captured_pawn_col)
                
                if captured_piece_obj and captured_piece_obj.type == 'pawn' and captured_piece_obj.color != pawn.color:
                    moves.append(Move((r, c), self.en_passant_target, is_en_passant=True, is_capture=True, captured_piece=captured_piece_obj))

        return moves

    def _get_knight_pseudo_moves(self, r, c, piece):
        moves = []
        knight_deltas = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_deltas:
            new_r, new_c = r + dr, c + dc
            if self.is_square_valid(new_r, new_c):
                target_piece = self.get_piece_at(new_r, new_c)
                if target_piece is None:
                    moves.append(Move((r, c), (new_r, new_c)))
                elif target_piece.color != piece.color:
                    moves.append(Move((r, c), (new_r, new_c), is_capture=True, captured_piece=target_piece))
        return moves

    def _get_bishop_pseudo_moves(self, r, c, piece):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Diagonals
        for dr, dc in directions:
            current_r, current_c = r + dr, c + dc
            while self.is_square_valid(current_r, current_c):
                target_piece = self.get_piece_at(current_r, current_c)
                if target_piece is None:
                    moves.append(Move((r, c), (current_r, current_c)))
                elif target_piece.color != piece.color:
                    moves.append(Move((r, c), (current_r, current_c), is_capture=True, captured_piece=target_piece))
                    break
                else:
                    break
                current_r += dr
                current_c += dc
        return moves

    def _get_rook_pseudo_moves(self, r, c, piece):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Straight
        for dr, dc in directions:
            current_r, current_c = r + dr, c + dc
            while self.is_square_valid(current_r, current_c):
                target_piece = self.get_piece_at(current_r, current_c)
                if target_piece is None:
                    moves.append(Move((r, c), (current_r, current_c)))
                elif target_piece.color != piece.color:
                    moves.append(Move((r, c), (current_r, current_c), is_capture=True, captured_piece=target_piece))
                    break
                else:
                    break
                current_r += dr
                current_c += dc
        return moves

    def _get_queen_pseudo_moves(self, r, c, piece):
        moves = self._get_rook_pseudo_moves(r, c, piece)
        moves.extend(self._get_bishop_pseudo_moves(r, c, piece))
        return moves

    def _get_king_pseudo_moves(self, r, c, piece):
        """Generates pseudo-legal moves for a king at (r, c)."""
        moves = []
        king_deltas = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for dr, dc in king_deltas:
            new_r, new_c = r + dr, c + dc
            if self.is_square_valid(new_r, new_c):
                target_piece = self.get_piece_at(new_r, new_c)
                
                if target_piece is None:
                    moves.append(Move((r, c), (new_r, new_c)))
                elif target_piece.color != piece.color:
                    # Addressed King-on-King issue here: A king cannot capture another king.
                    if target_piece.type == 'king':
                        pass # Do not add this move, as a king cannot capture another king.
                    else:
                        moves.append(Move((r, c), (new_r, new_c), is_capture=True, captured_piece=target_piece))
        
        # --- Castling Pseudo-Moves ---
        king_color = piece.color
        king_start_row = 7 if king_color == 'white' else 0
        
        if r == king_start_row and c == 4: # King is on its starting square
            # Kingside Castling
            if (king_color == 'white' and self.castling_rights['K']) or \
               (king_color == 'black' and self.castling_rights['k']):
                if self.get_piece_at(king_start_row, 5) is None and \
                   self.get_piece_at(king_start_row, 6) is None:
                    rook_at_h = self.get_piece_at(king_start_row, 7)
                    if rook_at_h and rook_at_h.type == 'rook' and rook_at_h.color == king_color:
                        moves.append(Move((r,c), (king_start_row, 6), is_castling=True))

            # Queenside Castling
            if (king_color == 'white' and self.castling_rights['Q']) or \
               (king_color == 'black' and self.castling_rights['q']):
                if self.get_piece_at(king_start_row, 1) is None and \
                   self.get_piece_at(king_start_row, 2) is None and \
                   self.get_piece_at(king_start_row, 3) is None:
                    rook_at_a = self.get_piece_at(king_start_row, 0)
                    if rook_at_a and rook_at_a.type == 'rook' and rook_at_a.color == king_color:
                        moves.append(Move((r,c), (king_start_row, 2), is_castling=True))
        
        return moves


    def generate_legal_moves(self):
        pseudo_legal_moves = self.generate_pseudo_legal_moves()
        legal_moves = []
        current_player_color = self.turn
        
        # print(f"\n--- Debugging {current_player_color} legal moves ---")
        # print(f"Original Board FEN: {self.to_fen()}")
        # self.display()

        for i, move in enumerate(pseudo_legal_moves):
            # print(f"\nAttempting to validate pseudo-legal move {i+1}: {move}")
            temp_board_for_check = self._copy()
            
            # print(f"Board state before make_move on temp_board (FEN: {temp_board_for_check.to_fen()}):")
            # temp_board_for_check.display()
            
            temp_board_for_check.make_move(move, is_simulated=True) 
            
            # print(f"Board state AFTER make_move on temp_board (FEN: {temp_board_for_check.to_fen()}):")
            # temp_board_for_check.display()
            
            king_in_check_after_move = temp_board_for_check.is_king_in_check(current_player_color)
            # print(f"Is {current_player_color}'s King in check after {move}? {king_in_check_after_move}")

            if not king_in_check_after_move:
                # Special check for castling: the squares the king moves through cannot be attacked
                if move.is_castling:
                    path_clear = True
                    row = move.from_square[0] # King's starting row
                    opponent_color = 'black' if current_player_color == 'white' else 'white'

                    # Check squares the king passes through (and the destination square)
                    if move.to_square[1] == 6: # Kingside castling (e.g., e1-g1 for white)
                        if self.is_square_attacked(row, 5, opponent_color) or \
                           self.is_square_attacked(row, 6, opponent_color):
                            path_clear = False
                    elif move.to_square[1] == 2: # Queenside castling (e.g., e1-c1 for white)
                        if self.is_square_attacked(row, 3, opponent_color) or \
                           self.is_square_attacked(row, 2, opponent_color):
                            path_clear = False
                    
                    if path_clear:
                        legal_moves.append(move)
                        # print(f"  --> Move {move} ADDED (Castling)")
                else:
                    legal_moves.append(move)
                    # print(f"  --> Move {move} ADDED (Not Castling)")
            # else:
                # print(f"  --> Move {move} DISCARDED (King in check)")
        return legal_moves

    def make_move(self, move, is_simulated=False):
        piece_moving = self.get_piece_at(move.from_square[0], move.from_square[1])
        if not piece_moving:
            raise ValueError(f"No piece found at {move.from_square} to move!")

        if move.is_capture:
            if move.is_en_passant:
                captured_pawn_row = move.from_square[0]
                captured_pawn_col = move.to_square[1]
                self.board_state[captured_pawn_row][captured_pawn_col] = None
            else:
                self.board_state[move.to_square[0]][move.to_square[1]] = None
            self.halfmove_clock = 0

        self.board_state[move.to_square[0]][move.to_square[1]] = piece_moving
        self.board_state[move.from_square[0]][move.from_square[1]] = None

        if piece_moving.type == 'king':
            self.king_position[piece_moving.color] = move.to_square
            if piece_moving.color == 'white':
                self.castling_rights['K'] = False
                self.castling_rights['Q'] = False
            else:
                self.castling_rights['k'] = False
                self.castling_rights['q'] = False
        
        if piece_moving.type == 'rook':
            if piece_moving.color == 'white':
                if move.from_square == (7, 0) and self.castling_rights['Q']:
                    self.castling_rights['Q'] = False
                elif move.from_square == (7, 7) and self.castling_rights['K']:
                    self.castling_rights['K'] = False
            else:
                if move.from_square == (0, 0) and self.castling_rights['q']:
                    self.castling_rights['q'] = False
                elif move.from_square == (0, 7) and self.castling_rights['k']:
                    self.castling_rights['k'] = False

        if piece_moving.type == 'pawn':
            self.halfmove_clock = 0

            if abs(move.from_square[0] - move.to_square[0]) == 2:
                ep_target_row = (move.from_square[0] + move.to_square[0]) // 2
                self.en_passant_target = (ep_target_row, move.to_square[1])
            else:
                self.en_passant_target = None

            if move.promotion_piece:
                promoted_piece = Piece(
                    {'Q': 'queen', 'R': 'rook', 'B': 'bishop', 'N': 'knight'}[move.promotion_piece],
                    piece_moving.color
                )
                self.board_state[move.to_square[0]][move.to_square[1]] = promoted_piece

        else:
            if not move.is_capture:
                self.halfmove_clock += 1
            self.en_passant_target = None

        if move.is_castling:
            king_row = move.from_square[0]
            if move.to_square[1] == 6:
                rook_from = (king_row, 7)
                rook_to = (king_row, 5)
            elif move.to_square[1] == 2:
                rook_from = (king_row, 0)
                rook_to = (king_row, 3)
            else:
                raise ValueError("Invalid castling 'to_square'")
            
            rook_moving = self.get_piece_at(rook_from[0], rook_from[1])
            self.board_state[rook_to[0]][rook_to[1]] = rook_moving
            self.board_state[rook_from[0]][rook_from[1]] = None


        if self.turn == 'black' and not is_simulated:
            self.fullmove_number += 1
        
        self.turn = 'black' if self.turn == 'white' else 'white'


    def unmake_move(self, move):
        print(f"Unmaking move {move} (Logic not implemented for full reversion)")

    def is_checkmate(self):
        return self.is_king_in_check(self.turn) and not self.generate_legal_moves()

    def is_stalemate(self):
        return not self.is_king_in_check(self.turn) and not self.generate_legal_moves()

    def is_draw(self):
        if self.halfmove_clock >= 100:
            return True
        return False

    def display(self):
        print("\n  a b c d e f g h")
        print(" +-----------------+")
        for r_idx, row in enumerate(self.board_state):
            print(f"{8 - r_idx}|", end="")
            for piece in row:
                print(f" {str(piece) if piece else '.'}", end="")
            print(f" |{8 - r_idx}")
        print(" +-----------------+")
        print(f"Turn: {self.turn.capitalize()}")
        print(f"Castling: {self.castling_rights}")
        ep_display = '-'
        if self.en_passant_target:
            ep_row, ep_col = self.en_passant_target
            ep_display = f"{chr(ord('a') + ep_col)}{8 - ep_row}"
        print(f"En Passant: {ep_display}")
        print(f"Halfmove Clock: {self.halfmove_clock}")
        print(f"Fullmove Number: {self.fullmove_number}")
        print(f"King Pos: W:{self.king_position['white']} B:{self.king_position['black']}")