"""
This is the main file of the project. It is used to handle user input and to display the game's GUI.
"""

# imports
import sys

import pygame as pg
import Engine

from utils import PIECES, IMAGES, SQUARE_SIZE, HEIGHT, WIDTH, DIMENSION, EMPTY_SQUARE, MAX_FPS, PROMOTION_TEXT


def init_images():
    """
    Initialize the IMAGES dictionary. Only needs to be called once, before the while loop.
    :return: nothing
    """
    for piece in PIECES:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def highlight_selection(screen, game_state, valid_positions, selected_square):
    """
    Function that highlights the selected square and all the valid moves from it.
    :param screen: A Pygame Display.
    :param game_state: A GameState object.
    :param valid_positions: A vector of tuples representing the valid positions in computer notation coordinates.
    :param selected_square: A tuple representing the selected square's position in computer notation coordinates.
    :return: nothing
    """
    if selected_square != ():
        row, col = selected_square
        if game_state.board[row][col][0] == ("w" if game_state.white_to_move else "b"):
            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100)
            surface.fill(pg.Color("light blue"))
            screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            surface.fill(pg.Color("yellow"))
            for position in valid_positions:
                # print((position[1], position[0]))
                screen.blit(surface, (position[1] * SQUARE_SIZE, position[0] * SQUARE_SIZE))


def draw_board(screen):
    """
    Function that draws the squares that make up the chess board.
    :param screen: A Pygame Display.
    """
    colors = [pg.Color("white"), pg.Color("dark gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    """
    Function that draws the pieces on top of the chess board.
    :param screen: A Pygame Display.
    :param board: A 8x8 2D list representing the chess board's layout, as seen from the white player's perspective.
    :return:
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != EMPTY_SQUARE:  # check if we have a piece at this position
                screen.blit(IMAGES[piece], pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_state(screen, game_state, valid_positions, selected_square):
    """
    Function that draws a given game state and highlights the selected square and it's valid moves.
    :param screen: A Pygame Display.
    :param game_state: A GameState object.
    :param valid_positions: A vector of tuples representing the valid positions in computer notation coordinates.
    :param selected_square: A tuple representing the selected square's position in computer notation coordinates.
    :return:
    """
    draw_board(screen)
    highlight_selection(screen, game_state, valid_positions, selected_square)
    draw_pieces(screen, game_state.board)


def draw_text(screen, text):
    """
    Function that draws a given text of the board.
    :param screen: A Pygame Display.
    :param text: A string representing the text to be drawn.
    :return:
    """
    font = pg.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, pg.Color("turquoise"))
    text_location = pg.Rect(0, 0, WIDTH, HEIGHT) \
        .move(WIDTH / 2 - text_object.get_width() / 2, HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, pg.Color("dark blue"))
    screen.blit(text_object, text_location.move(1, 1))


def main(computer=False):
    """
    Main function (entry point) of the program. It handles the user inputs and calls the computer to generate a move if
    needed.
    :param computer: A boolean flag that says if computer move generator must pe called.
    :return: nothing
    """
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("white"))
    clock = pg.time.Clock()
    game_state = Engine.GameState()
    init_images()
    selected_square = ()  # Tuple used to record the position a player clicked (row, column). Starts empty.
    player_move = []  # List of two tuples that represent the starting square and the final square of a move.
    valid_positions = []
    running = True
    game_over = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not game_over:
                        location = pg.mouse.get_pos()  # [X, Y] coordinates of a mouse click in the game window.
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        if selected_square == (row, col):  # player clicked the same square twice
                            selected_square = ()  # deselect the square
                            player_move = []  # reset the move
                        else:
                            selected_square = (row, col)
                            player_move.append(selected_square)
                        if len(player_move) == 2:  # the player has clicked to different squares and thus picked a move
                            if game_state.check_valid_move(player_move):
                                game_state.register_move(player_move)
                            selected_square = ()  # reset the selected_square tuple
                            player_move = []  # reset the player_move list
                            if game_state.await_promotion:
                                promotion = input(PROMOTION_TEXT + "\n")
                                game_state.promote(promotion.upper())
                        if computer:
                            game_state.make_computer_move()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    game_state.undo_move()
                    game_over = False
                if event.key == pg.K_x:
                    game_state = Engine.GameState()
                    selected_square = ()
                    player_move = []
                    game_over = False
        if selected_square != ():
            valid_moves = game_state.get_valid_moves()
            for valid_moves_index in range(len(valid_moves) - 1, -1, -1):
                if valid_moves[valid_moves_index][0] == selected_square:
                    valid_positions.append(valid_moves[valid_moves_index][1])
        draw_state(screen, game_state, valid_positions, selected_square)

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                draw_text(screen, "Black wins by checkmate!")
            else:
                draw_text(screen, "White wins by checkmate!")
        elif game_state.stale_mate:
            game_over = True
            draw_text(screen, "Stalemate!")
        valid_positions = []
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    computer_play = None
    for i, arg in enumerate(sys.argv):
        if i == 1:
            print(arg)
            if arg == "Computer":
                computer_play = True
            elif arg == "Human":
                computer_play = False
    if computer_play is None:
        print("Wrong Argument!")
    else:
        main(computer_play)
