"""
This file contains elements of functionality and game logic of Chess.
"""
# imports
from utils import BLACK_BISHOP, BLACK_KING, BLACK_KNIGHT, BLACK_PAWN, BLACK_QUEEN, BLACK_ROOK, WHITE_BISHOP, \
    WHITE_KING, WHITE_KNIGHT, WHITE_PAWN, WHITE_QUEEN, WHITE_ROOK, EMPTY_SQUARE, COLUMNS_TO_FILES, ROWS_TO_RANKS, \
    RANKS_TO_ROWS, FILES_TO_COLUMNS, BLACK_PIECES, WHITE_PIECES, KING_ROW_MODIFIERS, KING_COL_MODIFIERS, \
    KNIGHT_ROW_MODIFIERS, KNIGHT_COL_MODIFIERS, EN_PASSANT, PAWN_SKIP, PAWN_PROMOTION, KING_CASTLING, QUEEN_CASTLING


# Useful functions:
def get_chess_notation_for_position(square_row, square_col):
    """
    Function that returns the chess notation for given computer notation board coordinates.
    :param square_row: The row of the square in computer coordinates.
    :param square_col: The column of the square in computer coordinates.
    :return: A string representing the position in chess notation: "A7", "C3", etc.
    """
    return COLUMNS_TO_FILES[square_col] + ROWS_TO_RANKS[square_row]


def get_computer_notation_for_position(chess_notation_position):
    """
    Function that returns the computer notation for given chess notation board coordinates.
    :param chess_notation_position: A string representing the position in chess notation: "A7", "C3", etc.
    :return: A tuple representing the position in computer notation coordinates: (1, 0), (5, 2), etc.
    """
    return RANKS_TO_ROWS[chess_notation_position[1]], FILES_TO_COLUMNS[chess_notation_position[0]]


def get_move_dictionary(start_square_row, start_square_col, final_square_row, final_square_col,
                        moved_piece, captured_piece, additional_info):
    """
    Function that creates a dictionary documenting a move.
    :param additional_info: Additional information regarding the move: en passant, castling
    :param start_square_row: The starting row of the move in computer coordinates.
    :param start_square_col: The starting column of the move in computer coordinates.
    :param final_square_row: The final row of the move in computer coordinates.
    :param final_square_col: The final column of the move in computer coordinates.
    :param moved_piece: The piece that was moved.
    :param captured_piece: The piece that was captured or EMPTY_SQUARE in case of no capture.
    :return: A dictionary object of this form
    {'start_position': 'D7', 'final_position': 'D5', 'moved_piece': 'bP', 'captured_piece': '  '}
    """
    return {
        "start_position": get_chess_notation_for_position(start_square_row, start_square_col),
        "final_position": get_chess_notation_for_position(final_square_row, final_square_col),
        "moved_piece": moved_piece,
        "captured_piece": captured_piece,
        "additional_info": additional_info
    }


def get_castling_rights_dictionary(white_king_right, white_queen_right, black_king_right, black_queen_right):
    """

    :param white_king_right:
    :param white_queen_right:
    :param black_king_right:
    :param black_queen_right:
    :return: A dictionary object of this form
    {"white_king_right": True, "white_queen_right": True, "black_king_right": True, "black_queen_right": True}
    """
    return {
        "white_king_right": white_king_right,
        "white_queen_right": white_queen_right,
        "black_king_right": black_king_right,
        "black_queen_right": black_queen_right
    }


def get_castling_rights(castling_rights_dictionary):
    """

    :param castling_rights_dictionary: A dictionary object of this form
    {"white_king_right": True, "white_queen_right": True, "black_king_right": True, "black_queen_right": True}
    :return: A (bool, bool, bool, bool) tuple.
    """
    return castling_rights_dictionary["white_king_right"], castling_rights_dictionary["white_queen_right"], \
        castling_rights_dictionary["black_king_right"], castling_rights_dictionary["black_queen_right"]


def is_king_castle(start_position, final_position, moved_piece):
    if moved_piece == WHITE_KING or moved_piece == BLACK_KING:
        if final_position[1] - start_position[1] == 2:
            return True
    return False


def is_queen_castle(start_position, final_position, moved_piece):
    if moved_piece == WHITE_KING or moved_piece == BLACK_KING:
        if start_position[1] - final_position[1] == 2:
            return True
    return False


# GameState class:
class GameState:
    """
    This class is used to represent the state of the game: board layout/contents, current turn and a log with previous
    moves. It also offers functionalities related to moves.
    """

    def __init__(self):
        """
        Constructor of GameState class.
        The "board" is represented by a 8x8 2D list, as seen from the white player's perspective.
        The "white_to_move" internal variable tells us if it is the turn of the white player or not.
        The "moves_log" internal variable is a list of dictionaries that offers information about previous moves.
        :return: A GameState object.
        """
        self.board = [
            [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
            [BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN],
            [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
             EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
            [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
             EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
            [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
             EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
            [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE,
             EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
            [WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN],
            [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]]
        self.white_to_move = True
        self.moves_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.pawn_promotion = False
        self.en_passant_possible = ()
        self.white_king_right = True
        self.white_queen_right = True
        self.black_king_right = True
        self.black_queen_right = True
        self.castling_rights_log = [get_castling_rights_dictionary(self.white_king_right, self.white_queen_right,
                                                                   self.black_king_right, self.black_queen_right)]

    def register_move(self, move):
        """
        Function that marks a move in the board.
        :param move: List of two tuples that represent the start and final board coordinates of a move.
        [(start_row, start_col), (final_row, final_col)]
        :return: nothing
        """
        start_position = move[0]
        final_position = move[1]
        start_square_row = move[0][0]
        start_square_col = move[0][1]
        final_square_row = move[1][0]
        final_square_col = move[1][1]
        moved_piece = self.board[start_square_row][start_square_col]
        captured_piece = self.board[final_square_row][final_square_col]
        additional_info = ""
        self.board[start_square_row][start_square_col] = EMPTY_SQUARE
        self.board[final_square_row][final_square_col] = moved_piece

        self.white_to_move = not self.white_to_move
        if moved_piece == WHITE_KING:
            self.white_king_location = (final_square_row, final_square_col)
        elif moved_piece == BLACK_KING:
            self.black_king_location = (final_square_row, final_square_col)

        if self.is_en_passant(final_position, moved_piece):
            additional_info = EN_PASSANT
            captured_piece = self.board[start_square_row][final_square_col]
            self.board[start_square_row][final_square_col] = EMPTY_SQUARE
        if self.is_pawn_skip(start_position, final_position, moved_piece):
            additional_info = PAWN_SKIP
        if self.is_pawn_promotion(final_position, moved_piece):
            additional_info = PAWN_PROMOTION
            self.board[final_square_row][final_square_col] = str(moved_piece[0]) + "Q"
        if is_king_castle(start_position, final_position, moved_piece):
            self.board[final_square_row][final_square_col - 1] = self.board[final_square_row][final_square_col + 1]
            self.board[final_square_row][final_square_col + 1] = EMPTY_SQUARE
            additional_info = KING_CASTLING
        if is_queen_castle(start_position, final_position, moved_piece):
            self.board[final_square_row][final_square_col + 1] = self.board[final_square_row][final_square_col - 2]
            self.board[final_square_row][final_square_col - 2] = EMPTY_SQUARE
            additional_info = QUEEN_CASTLING

        self.moves_log.append(get_move_dictionary(start_square_row, start_square_col,
                                                  final_square_row, final_square_col,
                                                  moved_piece, captured_piece, additional_info))

        self.update_castling_rights(start_position, moved_piece)
        self.castling_rights_log.append(get_castling_rights_dictionary(self.white_king_right, self.white_queen_right,
                                                                       self.black_king_right, self.black_queen_right))

    def undo_move(self):
        """
        Function that undoes the last move in the "moves_log" list.
        :return: nothing
        """
        if len(self.moves_log) != 0:  # check if there are moves made
            last_move = self.moves_log.pop()
            start_position = get_computer_notation_for_position(last_move["start_position"])
            final_position = get_computer_notation_for_position(last_move["final_position"])
            moved_piece = last_move["moved_piece"]
            captured_piece = last_move["captured_piece"]
            additional_info = last_move["additional_info"]
            self.board[start_position[0]][start_position[1]] = moved_piece
            self.board[final_position[0]][final_position[1]] = captured_piece
            self.white_to_move = not self.white_to_move
            if moved_piece == WHITE_KING:
                self.white_king_location = start_position
            elif moved_piece == BLACK_KING:
                self.black_king_location = start_position
            if additional_info == EN_PASSANT:
                self.board[final_position[0]][final_position[1]] = EMPTY_SQUARE
                self.board[start_position[0]][final_position[1]] = captured_piece
                self.en_passant_possible = (final_position[0], final_position[1])
            if additional_info == PAWN_SKIP:
                self.en_passant_possible = ()
            if additional_info == KING_CASTLING:
                self.board[final_position[0]][final_position[1] + 1] = \
                    self.board[final_position[0]][final_position[1] - 1]
                self.board[final_position[0]][final_position[1] - 1] = EMPTY_SQUARE
            if additional_info == QUEEN_CASTLING:
                self.board[final_position[0]][final_position[1] - 2] = \
                    self.board[final_position[0]][final_position[1] + 1]
                self.board[final_position[0]][final_position[1] + 1] = EMPTY_SQUARE
            self.castling_rights_log.pop()
            self.white_king_right, self.white_queen_right, self.black_king_right, self.black_queen_right \
                = get_castling_rights(self.castling_rights_log[-1])

    def check_valid_move(self, move):
        if self.board[move[0][0]][move[0][1]][0] != "w" and self.white_to_move \
                or self.board[move[0][0]][move[0][1]][0] != "b" and not self.white_to_move:
            return False
        if move not in self.get_valid_moves():
            return False
        return True

    def get_valid_moves(self):
        temp_en_passant_possible = self.en_passant_possible
        temp_castling_rights_dictionary = get_castling_rights_dictionary(self.white_king_right, self.white_queen_right,
                                                                         self.black_king_right, self.black_queen_right)
        moves = self.get_all_moves()
        if self.white_to_move:
            moves.extend(self.get_castle_moves(self.white_king_location[0], self.white_king_location[1]))
        else:
            moves.extend(self.get_castle_moves(self.black_king_location[0], self.black_king_location[1]))
        for move_index in range(len(moves) - 1, -1, -1):
            self.register_move(moves[move_index])
            self.white_to_move = not self.white_to_move
            check = self.in_check()
            if check:
                moves.remove(moves[move_index])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = True
            self.stale_mate = True
        self.en_passant_possible = temp_en_passant_possible
        self.white_king_right, self.white_queen_right, self.black_king_right, self.black_queen_right \
            = get_castling_rights(temp_castling_rights_dictionary)
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location)
        else:
            return self.square_under_attack(self.black_king_location)

    def square_under_attack(self, square_location):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move[1][0] == square_location[0] and move[1][1] == square_location[1]:
                return True
        return False

    def get_all_moves(self):
        moves = []
        color = "w" if self.white_to_move else "b"
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col][0] == color:
                    start_position = (row, col)
                    for final_position in self.get_available_positions(row, col):
                        moves.append([start_position, final_position])
        return moves

    def get_available_positions(self, row, col):
        available_positions = []
        if self.board[row][col] == BLACK_PAWN or self.board[row][col] == WHITE_PAWN:
            available_positions = self.get_pawn_available_positions(row, col, self.board[row][col][0])
        elif self.board[row][col] == BLACK_ROOK or self.board[row][col] == WHITE_ROOK:
            available_positions = self.get_rook_available_positions(row, col, self.board[row][col][0])
        elif self.board[row][col] == BLACK_KNIGHT or self.board[row][col] == WHITE_KNIGHT:
            available_positions = self.get_king_or_knight_available_positions(
                row, col, self.board[row][col][0], KNIGHT_ROW_MODIFIERS, KNIGHT_COL_MODIFIERS)
        elif self.board[row][col] == BLACK_BISHOP or self.board[row][col] == WHITE_BISHOP:
            available_positions = self.get_bishop_available_positions(row, col, self.board[row][col][0])
        elif self.board[row][col] == BLACK_QUEEN or self.board[row][col] == WHITE_QUEEN:
            available_positions = self.get_queen_available_positions(row, col, self.board[row][col][0])
        elif self.board[row][col] == BLACK_KING or self.board[row][col] == WHITE_KING:
            enemy_queen = BLACK_QUEEN if self.white_to_move else WHITE_QUEEN
            available_positions = self.get_king_or_knight_available_positions(row, col, self.board[row][col][0],
                                                                              KING_ROW_MODIFIERS, KING_COL_MODIFIERS)
            for position_index in range(len(available_positions) - 1, -1, -1):
                print(available_positions[position_index])
                if self.board[available_positions[position_index][0]][available_positions[position_index][1]] \
                        == enemy_queen:
                    available_positions.remove(available_positions[position_index])
        return available_positions

    def get_pawn_available_positions(self, row, col, color):
        """

        :param row:
        :param col:
        :param color:
        :return:
        """
        positions = []
        direction = -1 if color == "w" else 1
        enemy_pieces = BLACK_PIECES if color == "w" else WHITE_PIECES
        start_row = 6 if color == "w" else 1
        if 0 <= row + direction <= 7:
            if self.board[row + direction][col] == EMPTY_SQUARE:
                positions.append((row + direction, col))
                if row == start_row and self.board[row + 2 * direction][col] == EMPTY_SQUARE:
                    positions.append((row + 2 * direction, col))
            if 0 <= col - 1 and (self.board[row + direction][col - 1] in enemy_pieces
                                 or (row + direction, col - 1) == self.en_passant_possible):
                positions.append((row + direction, col - 1))
            if col + 1 <= 7 and (self.board[row + direction][col + 1] in enemy_pieces
                                 or (row + direction, col + 1) == self.en_passant_possible):
                positions.append((row + direction, col + 1))
        return positions

    def get_rook_available_positions(self, row, col, color):
        positions = []
        enemy_pieces = BLACK_PIECES if color == "w" else WHITE_PIECES
        row_i = 1
        while row + row_i <= 7 and self.board[row + row_i][col] == EMPTY_SQUARE:
            positions.append((row + row_i, col))
            row_i += 1
        if row + row_i <= 7 and self.board[row + row_i][col] in enemy_pieces:
            positions.append((row + row_i, col))
        row_i = 1
        while 0 <= row - row_i and self.board[row - row_i][col] == EMPTY_SQUARE:
            positions.append((row - row_i, col))
            row_i += 1
        if 0 <= row - row_i and self.board[row - row_i][col] in enemy_pieces:
            positions.append((row - row_i, col))
        col_i = 1
        while col + col_i <= 7 and self.board[row][col + col_i] == EMPTY_SQUARE:
            positions.append((row, col + col_i))
            col_i += 1
        if col + col_i <= 7 and self.board[row][col + col_i] in enemy_pieces:
            positions.append((row, col + col_i))
        col_i = 1
        while 0 <= col - col_i and self.board[row][col - col_i] == EMPTY_SQUARE:
            positions.append((row, col - col_i))
            col_i += 1
        if 0 <= col - col_i and self.board[row][col - col_i] in enemy_pieces:
            positions.append((row, col - col_i))
        return positions

    def get_bishop_available_positions(self, row, col, color):
        positions = []
        enemy_pieces = BLACK_PIECES if color == "w" else WHITE_PIECES
        iterator = 1
        while 0 <= row - iterator and 0 <= col - iterator \
                and self.board[row - iterator][col - iterator] == EMPTY_SQUARE:
            positions.append((row - iterator, col - iterator))
            iterator += 1
        if 0 <= row - iterator and 0 <= col - iterator and self.board[row - iterator][col - iterator] in enemy_pieces:
            positions.append((row - iterator, col - iterator))
        iterator = 1
        while 0 <= row - iterator and col + iterator <= 7 \
                and self.board[row - iterator][col + iterator] == EMPTY_SQUARE:
            positions.append((row - iterator, col + iterator))
            iterator += 1
        if 0 <= row - iterator and col + iterator <= 7 and self.board[row - iterator][col + iterator] in enemy_pieces:
            positions.append((row - iterator, col + iterator))
        iterator = 1
        while row + iterator <= 7 and 0 <= col - iterator \
                and self.board[row + iterator][col - iterator] == EMPTY_SQUARE:
            positions.append((row + iterator, col - iterator))
            iterator += 1
        if row + iterator <= 7 and 0 <= col - iterator and self.board[row + iterator][col - iterator] in enemy_pieces:
            positions.append((row + iterator, col - iterator))
        iterator = 1
        while row + iterator <= 7 and col + iterator <= 7 \
                and self.board[row + iterator][col + iterator] == EMPTY_SQUARE:
            positions.append((row + iterator, col + iterator))
            iterator += 1
        if row + iterator <= 7 and col + iterator <= 7 and self.board[row + iterator][col + iterator] in enemy_pieces:
            positions.append((row + iterator, col + iterator))
        return positions

    def get_queen_available_positions(self, row, col, color):
        positions = []
        positions.extend(self.get_rook_available_positions(row, col, color))
        positions.extend(self.get_bishop_available_positions(row, col, color))
        return positions

    def get_king_or_knight_available_positions(self, row, col, color, row_modifiers, col_modifiers):
        positions = []
        enemy_pieces = BLACK_PIECES if color == "w" else WHITE_PIECES
        for row_modifier, col_modifier in zip(row_modifiers, col_modifiers):
            new_row = row + row_modifier
            new_col = col + col_modifier
            if 0 <= new_row <= 7 and 0 <= new_col <= 7 \
                    and (self.board[new_row][new_col] == EMPTY_SQUARE or self.board[new_row][new_col] in enemy_pieces):
                positions.append((new_row, new_col))
        return positions

    def get_castle_moves(self, row, col):
        moves = []
        if self.square_under_attack((row, col)):
            return moves
        if (self.white_to_move and self.white_king_right) or (not self.white_to_move and self.black_king_right):
            moves.extend(self.get_king_castle_moves(row, col))
        if (self.white_to_move and self.white_queen_right) or (not self.white_to_move and self.black_queen_right):
            moves.extend(self.get_queen_castle_moves(row, col))
        return moves

    def get_king_castle_moves(self, row, col):
        moves = []
        if self.board[row][col + 1] == EMPTY_SQUARE and self.board[row][col + 2] == EMPTY_SQUARE:
            if not self.square_under_attack((row, col + 1)) and not self.square_under_attack((row, col + 2)):
                moves.append([(row, col), (row, col + 2)])
        return moves

    def get_queen_castle_moves(self, row, col):
        moves = []
        if self.board[row][col - 1] == EMPTY_SQUARE and self.board[row][col - 2] == EMPTY_SQUARE \
                and self.board[row][col - 3] == EMPTY_SQUARE:
            if not self.square_under_attack((row, col - 1)) and not self.square_under_attack((row, col - 2)) \
                    and not self.square_under_attack((row, col - 3)):
                moves.append([(row, col), (row, col - 2)])
        return moves

    def is_en_passant(self, final_position, moved_piece):
        if moved_piece == BLACK_PAWN or moved_piece == WHITE_PAWN:
            if final_position == self.en_passant_possible:
                return True
        return False

    def is_pawn_skip(self, start_position, final_position, moved_piece):
        self.en_passant_possible = ()
        if moved_piece == BLACK_PAWN or moved_piece == WHITE_PAWN:
            if abs(start_position[0] - final_position[0]) == 2:
                self.en_passant_possible = ((start_position[0] + final_position[0]) // 2, final_position[1])
                return True
        return False

    def is_pawn_promotion(self, final_position, moved_piece):
        self.pawn_promotion = False
        if (moved_piece == BLACK_PAWN and final_position[0] == 7) \
                or (moved_piece == WHITE_PAWN and final_position[0] == 0):
            self.pawn_promotion = True
            return True
        return False

    def undo_en_passant(self, captured_piece, final_position):
        direction = 1 if self.white_to_move else -1
        self.board[final_position[0]][final_position[1]] = EMPTY_SQUARE
        self.board[final_position[0] + direction][final_position[1]] = captured_piece

    def update_castling_rights(self, start_position, moved_piece):
        if moved_piece == WHITE_KING:
            self.white_king_right = False
            self.white_queen_right = False
        if moved_piece == BLACK_KING:
            self.black_king_right = False
            self.black_queen_right = False
        if moved_piece == WHITE_ROOK:
            if start_position[0] == 7:
                if start_position[1] == 0:
                    self.white_queen_right = False
                elif start_position[1] == 7:
                    self.white_king_right = False
        elif moved_piece == BLACK_ROOK:
            if start_position[0] == 0:
                if start_position[1] == 0:
                    self.black_queen_right = False
                elif start_position[1] == 7:
                    self.black_king_right = False
