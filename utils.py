"""
In this file are stored constants used throughout the code.
"""

# Piece identifier strings:
BLACK_KING = "bK"  # Black King
BLACK_QUEEN = "bQ"  # Black Queen
BLACK_BISHOP = "bB"  # Black Bishop
BLACK_KNIGHT = "bN"  # Black kNight
BLACK_ROOK = "bR"  # Black Rook
BLACK_PAWN = "bP"  # Black Pawn
WHITE_KING = "wK"  # White King
WHITE_QUEEN = "wQ"  # White Queen
WHITE_BISHOP = "wB"  # White Bishop
WHITE_KNIGHT = "wN"  # White kNight
WHITE_ROOK = "wR"  # White Rook
WHITE_PAWN = "wP"  # White Pawn
# Empty board space identifier string:
EMPTY_SQUARE = "  "  # Empty Square
#
PIECES = [BLACK_PAWN, BLACK_KING, BLACK_QUEEN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK,
          WHITE_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK]

# GUI constants
MAX_FPS = 15
HEIGHT = WIDTH = 512  # Window size
DIMENSION = 8  # Dimensions of a chess board (8x8)
SQUARE_SIZE = int(HEIGHT / DIMENSION)  # Size of a board square in the GUI
IMAGES = {}
