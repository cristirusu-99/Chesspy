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
# A list of all the pieces:
PIECES = [BLACK_PAWN, BLACK_KING, BLACK_QUEEN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK,
          WHITE_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK]
WHITE_PIECES = [WHITE_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK]
BLACK_PIECES = [BLACK_PAWN, BLACK_KING, BLACK_QUEEN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK]

# Mapping of locations in computer notation to chess notation: [0, 0] -> [A, 8], [0, 1] -> [B, 8], [1, 0] -> [A, 7]
COLUMNS_TO_FILES = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
ROWS_TO_RANKS = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
# Mapping of locations in chess notation to computer notation: [A, 8] -> [0, 0], [B, 8] -> [0, 1], [A, 7] -> [1, 0]
FILES_TO_COLUMNS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
RANKS_TO_ROWS = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}

# Special rules:
EN_PASSANT = "EP"
QUEEN_CASTLING = "QC"
KING_CASTLING = "KC"
PAWN_SKIP = "PS"
PAWN_PROMOTION = "PP"

KING_ROW_MODIFIERS = [-1, -1, -1, 0, 0, 1, 1, 1]
KING_COL_MODIFIERS = [-1, 0, 1, -1, 1, -1, 0, 1]

KNIGHT_ROW_MODIFIERS = [1, 2, 2, 1, -1, -2, -2, -1]
KNIGHT_COL_MODIFIERS = [2, 1, -1, -2, -2, -1, 1, 2]


# GUI constants
MAX_FPS = 15
HEIGHT = WIDTH = 512  # Window size
DIMENSION = 8  # Dimensions of a chess board (8x8)
SQUARE_SIZE = HEIGHT // DIMENSION  # Size of a board square in the GUI
IMAGES = {}
PROMOTION_TEXT = "Press R to promote to Rook\n" \
                 "Press Q to promote to Queen\n" \
                 "Press B to promote to Bishop\n" \
                 "Press N to promote to Knight"
