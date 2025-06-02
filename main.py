# main.py
from board import Board
from piece import Piece
from move import Move
from game_controller import GameController # Import GameController

def run_test_scenario(fen_string, description):
    print(f"\n--- Testing Scenario: {description} ---")
    board = Board(fen=fen_string)
    board.display()

    print(f"\nLegal moves for {board.turn.capitalize()}:")
    legal_moves = board.generate_legal_moves()
    
    # Sort moves for consistent output (e.g., by UCI string)
    legal_moves.sort(key=lambda m: m.to_uci())

    if not legal_moves:
        print("No legal moves found.")
        if board.is_king_in_check(board.turn):
            print(f"Result: {board.turn.capitalize()} is in CHECKMATE!")
        else:
            print(f"Result: {board.turn.capitalize()} is in STALEMATE!") 
    else:
        for move in legal_moves:
            print(f"  {move.to_uci()} ({move})")
        print(f"Total legal moves: {len(legal_moves)}")
    print("-" * (len(description) + 26))


if __name__ == "__main__":
    # --- Running all previous test scenarios ---
    run_test_scenario(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "Initial Position (White's Turn)"
    )

    run_test_scenario(
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
        "After White 1. e4 (Black's Turn)"
    )

    run_test_scenario(
        "3k4/8/8/8/8/8/R7/3K4 b - - 0 1",
        "Black King in Check (Black to Move)"
    )

    run_test_scenario(
        "8/8/8/1Pp5/8/8/8/K1k5 w - c6 0 3", 
        "En Passant Capture (White to Move, Target c6)"
    )

    run_test_scenario(
        "8/P7/8/8/8/8/8/K1k5 w - - 0 1", 
        "Pawn Promotion (White to Move, Pawn on a7)"
    )
    
    run_test_scenario(
        "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
        "Castling (White to Move, Initial Castling Rights)"
    )

    run_test_scenario(
        "r3k2r/8/8/8/8/8/6q1/R3K2R w KQkq - 0 1",
        "Castling through Check (White to Move, Queen on g2)"
    )
    
    # --- CRITICAL TEST: Checkmate Scenario (Fool's Mate) ---
    run_test_scenario(
        "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 2", # CORRECTED FEN
        "Checkmate Scenario (Fool's Mate - White to move)"
    )

    run_test_scenario(
        "8/8/8/8/8/8/7k/7K b - - 0 1",
        "Stalemate Scenario (Black King on h2, Black to move)"
    )

    print("\n--- Manual Test: Castling Rights Revocation ---")
    board_cr_test = Board(fen="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    board_cr_test.display()
    print("Initial Castling Rights:", board_cr_test.castling_rights)
    
    white_kingside_rook_move = Move((7, 7), (7, 6)) # Rh1-g1
    print(f"\nMaking move: {white_kingside_rook_move}")
    board_cr_test.make_move(white_kingside_rook_move)
    board_cr_test.display()
    print("Castling Rights after Rh1-g1:", board_cr_test.castling_rights)

    board_cr_test_q = Board(fen="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    white_queenside_rook_move = Move((7, 0), (7, 1)) # Ra1-b1
    print(f"\nMaking move: {white_queenside_rook_move}")
    board_cr_test_q.make_move(white_queenside_rook_move)
    board_cr_test_q.display()
    print("Castling Rights after Ra1-b1:", board_cr_test_q.castling_rights)
    print("-" * 50)

    # --- New section: Test Engine Capabilities ---
    print("\n\n--- Testing Engine Capabilities ---")
    game_controller = GameController()

    # Test 1: Get engine's first move
    game_controller.load_game_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print("\n--- Engine's suggested first move (White, Depth 3) ---")
    engine_move, score = game_controller.get_engine_move(depth=3)
    print(f"Engine's best move: {engine_move} with score: {score}")

    # Test 2: Analyze a specific position
    print("\n--- Analyzing a complex position (Black to move, Depth 4) ---")
    game_controller.load_game_from_fen("r3k2r/pbpq1ppp/1pnp1n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 1") # A common mid-game FEN
    game_controller.analyze_current_position(num_lines=3, depth=4)

    # Test 3: Play a simple game (optional, can comment out if too long)
    # Be prepared: A depth 3 engine might not be very strong!
    # game_controller.play_game(engine_color='black', depth=3)
    # game_controller.play_game(engine_color='white', depth=3)